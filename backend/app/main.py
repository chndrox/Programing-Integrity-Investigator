from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging
import os
import asyncio
from pathlib import Path

from app.database import engine, Base, get_db, settings, SessionLocal
from app.models import (
    User, Student, Assignment, Submission, Investigation, 
    CommitHistory, AuditLog, InstructorDecision, CaseReport
)
from app.schemas import (
    UserResponse, StudentResponse, AssignmentResponse, SubmissionResponse,
    InvestigationResponse, InvestigationCreate, AuditLogResponse,
    DashboardStats, MCPServerStatus, MCPToolResponse
)
from app.api.auth import get_current_user, create_access_token, hash_password, router as auth_router
from app.orchestrator.agent_orchestrator import AgentOrchestrator
from app.mcp.submissions_mcp import SubmissionsMCP
from app.mcp.similarity_mcp import SimilarityMCP
from app.services.similarity_service import SimilarityService
from app.services.timeline_service import TimelineService
from app.services.groq_service import get_groq_service

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize demo user (disabled due to bcrypt compatibility issue)
# To initialize demo data, run: python sample_data.py
def init_demo_user():
    """Create demo instructor user if it doesn't exist."""
    # Note: Demo user initialization disabled due to bcrypt compatibility issue
    # Run 'python sample_data.py' to initialize demo data instead
    logger.info("Demo user initialization skipped. Run 'python sample_data.py' to seed data.")

# Initialize demo user on startup
init_demo_user()

# Create FastAPI app
app = FastAPI(
    title="Programming Assignment Integrity Investigator",
    description="AI-powered plagiarism detection and investigation system",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include auth router
app.include_router(auth_router)

# Create uploads directory
uploads_dir = Path(settings.upload_dir)
uploads_dir.mkdir(exist_ok=True)


# ==================== DASHBOARD ====================

@app.get("/api/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dashboard statistics."""
    
    total_submissions = db.query(Submission).count()
    active_investigations = db.query(Investigation).filter(
        Investigation.status.in_(["pending", "in_progress"])
    ).count()
    completed_investigations = db.query(Investigation).filter(
        Investigation.status == "completed"
    ).count()
    cases_requiring_review = db.query(CaseReport).filter(
        ~CaseReport.decisions.any()
    ).count()
    
    # Risk distribution (simulated)
    risk_distribution = {
        "low": completed_investigations // 3,
        "medium": completed_investigations // 3,
        "high": completed_investigations - (completed_investigations // 3) * 2
    }
    
    return DashboardStats(
        total_submissions=total_submissions,
        active_investigations=active_investigations,
        cases_requiring_review=cases_requiring_review,
        completed_investigations=completed_investigations,
        risk_distribution=risk_distribution
    )


@app.get("/api/dashboard/recent-investigations")
async def get_recent_investigations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get recent investigations."""
    
    investigations = db.query(Investigation).order_by(
        Investigation.created_at.desc()
    ).limit(10).all()
    
    result = []
    for inv in investigations:
        result.append({
            "id": inv.id,
            "assignment_id": inv.assignment_id,
            "assignment_name": inv.assignment.name if inv.assignment else "Unknown",
            "status": inv.status,
            "created_at": inv.created_at.isoformat(),
            "submission_count": len(inv.submissions)
        })
    
    return result


# ==================== SUBMISSIONS ====================

@app.post("/api/submissions/upload")
async def upload_submission(
    student_id: int = Form(...),
    assignment_id: int = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a programming assignment submission."""
    
    # Validate file size
    contents = await file.read()
    if len(contents) > settings.max_file_size:
        raise HTTPException(status_code=400, detail="File too large")
    
    # Check student exists
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check assignment exists
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    # Save file
    file_path = uploads_dir / f"submission_{int(datetime.now().timestamp())}_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # Decode source code
    try:
        source_code = contents.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Invalid file encoding")
    
    # Create submission
    submission = Submission(
        student_id=student_id,
        assignment_id=assignment_id,
        file_name=file.filename,
        file_path=str(file_path),
        source_code=source_code,
        language="python"
    )
    
    db.add(submission)
    db.commit()
    db.refresh(submission)
    
    # Log audit
    audit = AuditLog(
        user_id=current_user.id,
        action="submission_uploaded",
        details={
            "submission_id": submission.id,
            "student_name": student.name,
            "assignment_name": assignment.name
        }
    )
    db.add(audit)
    db.commit()
    
    return {
        "id": submission.id,
        "message": "Submission uploaded successfully"
    }


@app.get("/api/submissions")
async def list_submissions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    assignment_id: int = None,
    student_id: int = None
):
    """List submissions with optional filters."""
    
    query = db.query(Submission)
    
    if assignment_id:
        query = query.filter(Submission.assignment_id == assignment_id)
    
    if student_id:
        query = query.filter(Submission.student_id == student_id)
    
    submissions = query.order_by(Submission.submitted_at.desc()).all()
    
    result = []
    for submission in submissions:
        result.append({
            "id": submission.id,
            "student_id": submission.student.id,
            "student_name": submission.student.name,
            "assignment_id": submission.assignment.id,
            "assignment_name": submission.assignment.name,
            "file_name": submission.file_name,
            "language": submission.language,
            "submitted_at": submission.submitted_at.isoformat(),
            "source_code_lines": len(submission.source_code.split('\n')) if submission.source_code else 0
        })
    
    return result


@app.get("/api/submissions/{submission_id}")
async def get_submission_detail(
    submission_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get submission details including source code."""
    
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    return {
        "id": submission.id,
        "student_id": submission.student.id,
        "student_name": submission.student.name,
        "assignment_id": submission.assignment.id,
        "assignment_name": submission.assignment.name,
        "file_name": submission.file_name,
        "language": submission.language,
        "source_code": submission.source_code,
        "submitted_at": submission.submitted_at.isoformat(),
        "git_repo_url": submission.git_repo_url
    }


# ==================== INVESTIGATIONS ====================

@app.post("/api/investigations/start")
async def start_investigation(
    investigation_create: InvestigationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a new investigation."""
    
    # Validate submissions
    if len(investigation_create.submission_ids) < 2:
        raise HTTPException(status_code=400, detail="At least 2 submissions required")
    
    submissions = db.query(Submission).filter(
        Submission.id.in_(investigation_create.submission_ids)
    ).all()
    
    if len(submissions) != len(investigation_create.submission_ids):
        raise HTTPException(status_code=400, detail="One or more submissions not found")
    
    # Create investigation
    investigation = Investigation(
        created_by=current_user.id,
        assignment_id=investigation_create.assignment_id,
        status="pending"
    )
    
    for submission in submissions:
        investigation.submissions.append(submission)
    
    db.add(investigation)
    db.commit()
    db.refresh(investigation)
    
    # Log audit
    audit = AuditLog(
        user_id=current_user.id,
        investigation_id=investigation.id,
        action="investigation_created",
        details={
            "submission_count": len(submissions),
            "assignment_id": investigation_create.assignment_id
        }
    )
    db.add(audit)
    db.commit()
    
    # Start orchestration in background
    asyncio.create_task(run_investigation_async(investigation.id, db))
    
    return {
        "id": investigation.id,
        "status": investigation.status,
        "message": "Investigation started"
    }


async def run_investigation_async(investigation_id: int, db: Session):
    """Run investigation asynchronously."""
    try:
        orchestrator = AgentOrchestrator(db)
        result = await orchestrator.orchestrate_investigation(investigation_id)
        logger.info(f"Investigation {investigation_id} completed: {result['status']}")
    except Exception as e:
        logger.error(f"Investigation {investigation_id} failed: {str(e)}")


@app.get("/api/investigations")
async def list_investigations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all investigations."""
    
    investigations = db.query(Investigation).order_by(
        Investigation.created_at.desc()
    ).all()
    
    result = []
    for investigation in investigations:
        result.append({
            "id": investigation.id,
            "assignment_id": investigation.assignment_id,
            "assignment_name": investigation.assignment.name if investigation.assignment else "Unknown",
            "status": investigation.status,
            "created_at": investigation.created_at.isoformat(),
            "submission_count": len(investigation.submissions),
            "has_report": investigation.report is not None
        })
    
    return result


@app.get("/api/investigations/{investigation_id}")
async def get_investigation_detail(
    investigation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get investigation details."""
    
    investigation = db.query(Investigation).filter(
        Investigation.id == investigation_id
    ).first()
    
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")
    
    # Get agent results
    agent_results = []
    for result in investigation.agent_results:
        agent_results.append({
            "id": result.id,
            "agent_type": result.agent_type,
            "status": result.status,
            "execution_time": result.execution_time,
            "result": result.result
        })
    
    return {
        "id": investigation.id,
        "assignment_id": investigation.assignment_id,
        "status": investigation.status,
        "created_at": investigation.created_at.isoformat(),
        "started_at": investigation.started_at.isoformat() if investigation.started_at else None,
        "completed_at": investigation.completed_at.isoformat() if investigation.completed_at else None,
        "submissions": [
            {
                "id": s.id,
                "student_name": s.student.name,
                "submitted_at": s.submitted_at.isoformat()
            }
            for s in investigation.submissions
        ],
        "agent_results": agent_results
    }


@app.get("/api/investigations/{investigation_id}/report")
async def get_investigation_report(
    investigation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get investigation case report."""
    
    investigation = db.query(Investigation).filter(
        Investigation.id == investigation_id
    ).first()
    
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")
    
    if not investigation.report:
        raise HTTPException(status_code=404, detail="Report not generated yet")
    
    return investigation.report.report_content


# ==================== REPORTS ====================

@app.post("/api/reports/{investigation_id}/approve")
async def approve_report(
    investigation_id: int,
    notes: str = "",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Approve an investigation report."""
    
    investigation = db.query(Investigation).filter(
        Investigation.id == investigation_id
    ).first()
    
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")
    
    if not investigation.report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Create decision
    decision = InstructorDecision(
        report_id=investigation.report.id,
        user_id=current_user.id,
        decision="approved",
        notes=notes
    )
    
    db.add(decision)
    db.commit()
    
    # Log audit
    audit = AuditLog(
        user_id=current_user.id,
        investigation_id=investigation_id,
        action="report_approved",
        details={"notes": notes}
    )
    db.add(audit)
    db.commit()
    
    return {"message": "Report approved successfully"}


# ==================== MCP ====================

@app.get("/api/mcp/status")
async def get_mcp_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get MCP server status."""
    
    submissions_mcp = SubmissionsMCP(db)
    similarity_mcp = SimilarityMCP(db)
    
    return {
        "mode": "mock" if settings.use_mock_mcp else "live",
        "servers": [
            {
                "name": "submissions-mcp",
                "connected": True,
                "tools": submissions_mcp.get_tools()
            },
            {
                "name": "similarity-mcp",
                "connected": True,
                "tools": similarity_mcp.get_tools()
            }
        ]
    }


# ==================== SETTINGS ====================

@app.get("/api/settings")
async def get_settings(
    current_user: User = Depends(get_current_user)
):
    """Get settings (non-sensitive)."""
    
    return {
        "groq_model": settings.groq_model,
        "agent_concurrency_limit": settings.agent_concurrency_limit,
        "agent_timeout_seconds": settings.agent_timeout_seconds,
        "use_mock_mcp": settings.use_mock_mcp
    }


# ==================== AUDIT ====================

@app.get("/api/audit-logs")
async def get_audit_logs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 50
):
    """Get recent audit logs."""
    
    logs = db.query(AuditLog).order_by(
        AuditLog.created_at.desc()
    ).limit(limit).all()
    
    result = []
    for log in logs:
        result.append({
            "id": log.id,
            "user": log.user.username if log.user else "System",
            "action": log.action,
            "details": log.details,
            "created_at": log.created_at.isoformat()
        })
    
    return result


# ==================== HEALTH CHECK ====================

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
