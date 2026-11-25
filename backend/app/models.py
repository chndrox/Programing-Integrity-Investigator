from sqlalchemy import Column, String, Integer, DateTime, Float, Text, Boolean, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    role = Column(String, default="instructor")  # instructor, admin
    created_at = Column(DateTime, default=datetime.utcnow)
    
    investigations = relationship("Investigation", back_populates="created_by_user")
    decisions = relationship("InstructorDecision", back_populates="user")


class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, unique=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    department = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    submissions = relationship("Submission", back_populates="student")


class Assignment(Base):
    __tablename__ = "assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    due_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    submissions = relationship("Submission", back_populates="assignment")


class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    assignment_id = Column(Integer, ForeignKey("assignments.id"))
    file_path = Column(String)
    file_name = Column(String)
    source_code = Column(Text)
    language = Column(String, default="python")
    git_repo_url = Column(String, nullable=True)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", back_populates="submissions")
    assignment = relationship("Assignment", back_populates="submissions")
    commit_history = relationship("CommitHistory", back_populates="submission")
    investigations = relationship("Investigation", secondary="investigation_submissions", back_populates="submissions")


class CommitHistory(Base):
    __tablename__ = "commit_history"
    
    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"))
    commit_hash = Column(String)
    author = Column(String)
    message = Column(Text)
    timestamp = Column(DateTime)
    additions = Column(Integer, default=0)
    deletions = Column(Integer, default=0)
    
    submission = relationship("Submission", back_populates="commit_history")


class InvestigationStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Investigation(Base):
    __tablename__ = "investigations"
    
    id = Column(Integer, primary_key=True, index=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    assignment_id = Column(Integer, ForeignKey("assignments.id"))
    status = Column(String, default=InvestigationStatus.PENDING.value)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    
    created_by_user = relationship("User", back_populates="investigations")
    submissions = relationship("Submission", secondary="investigation_submissions", back_populates="investigations")
    agent_results = relationship("AgentResult", back_populates="investigation", cascade="all, delete-orphan")
    report = relationship("CaseReport", back_populates="investigation", uselist=False)
    audit_logs = relationship("AuditLog", back_populates="investigation")


class AgentType(str, enum.Enum):
    SIMILARITY_ANALYST = "similarity_analyst"
    TIMELINE_ANALYST = "timeline_analyst"
    EXCULPATORY_REVIEWER = "exculpatory_reviewer"
    CASE_WRITER = "case_writer"


class AgentResult(Base):
    __tablename__ = "agent_results"
    
    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id"))
    agent_type = Column(String)
    status = Column(String, default="pending")  # pending, running, completed, failed
    result = Column(JSON, nullable=True)
    error = Column(Text, nullable=True)
    execution_time = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    investigation = relationship("Investigation", back_populates="agent_results")


class CaseReport(Base):
    __tablename__ = "case_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id"), unique=True)
    report_content = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    investigation = relationship("Investigation", back_populates="report")
    decisions = relationship("InstructorDecision", back_populates="report")


class InstructorDecision(Base):
    __tablename__ = "instructor_decisions"
    
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("case_reports.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    decision = Column(String)  # approved, needs_further_review, dismissed
    notes = Column(Text, nullable=True)
    decided_at = Column(DateTime, default=datetime.utcnow)
    
    report = relationship("CaseReport", back_populates="decisions")
    user = relationship("User", back_populates="decisions")


class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id"), nullable=True)
    action = Column(String)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    investigation = relationship("Investigation", back_populates="audit_logs")


# Association table for investigation and submissions (many-to-many)
from sqlalchemy import Table
investigation_submissions = Table(
    'investigation_submissions',
    Base.metadata,
    Column('investigation_id', Integer, ForeignKey('investigations.id'), primary_key=True),
    Column('submission_id', Integer, ForeignKey('submissions.id'), primary_key=True)
)
