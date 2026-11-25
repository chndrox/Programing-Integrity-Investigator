"""
SUBMISSIONS-MCP SERVER

Provides tools for retrieving submission data and commit history.
Implements local mock mode if external MCP servers unavailable.
"""

import logging
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.models import Submission, CommitHistory, Student

logger = logging.getLogger(__name__)


class SubmissionsMCP:
    """Mock implementation of submissions MCP server."""

    def __init__(self, db: Session):
        self.db = db

    async def get_submission(self, submission_id: int) -> Dict[str, Any]:
        """
        Retrieve submission data.
        
        Tool: submissions-mcp.get_submission
        Parameters:
        - submission_id: int
        
        Returns: Submission object with metadata and source code
        """
        
        try:
            submission = self.db.query(Submission).filter(
                Submission.id == submission_id
            ).first()
            
            if not submission:
                return {
                    "status": "error",
                    "message": f"Submission {submission_id} not found"
                }
            
            return {
                "status": "success",
                "submission": {
                    "id": submission.id,
                    "student_id": submission.student.id,
                    "student_name": submission.student.name,
                    "student_email": submission.student.email,
                    "assignment_id": submission.assignment_id,
                    "assignment_name": submission.assignment.name,
                    "file_name": submission.file_name,
                    "language": submission.language,
                    "git_repo_url": submission.git_repo_url,
                    "submitted_at": submission.submitted_at.isoformat(),
                    "source_code": submission.source_code
                }
            }
        
        except Exception as e:
            logger.error(f"Error retrieving submission: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }

    async def get_commit_history(self, submission_id: int) -> Dict[str, Any]:
        """
        Retrieve commit history for a submission.
        
        Tool: submissions-mcp.get_commit_history
        Parameters:
        - submission_id: int
        
        Returns: List of commits with metadata
        """
        
        try:
            submission = self.db.query(Submission).filter(
                Submission.id == submission_id
            ).first()
            
            if not submission:
                return {
                    "status": "error",
                    "message": f"Submission {submission_id} not found"
                }
            
            commits = self.db.query(CommitHistory).filter(
                CommitHistory.submission_id == submission_id
            ).order_by(CommitHistory.timestamp).all()
            
            commits_data = []
            for commit in commits:
                commits_data.append({
                    "hash": commit.commit_hash,
                    "author": commit.author,
                    "message": commit.message,
                    "timestamp": commit.timestamp.isoformat(),
                    "additions": commit.additions,
                    "deletions": commit.deletions
                })
            
            return {
                "status": "success",
                "submission_id": submission_id,
                "commit_count": len(commits_data),
                "commits": commits_data
            }
        
        except Exception as e:
            logger.error(f"Error retrieving commit history: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }

    async def list_submissions(
        self,
        assignment_id: Optional[int] = None,
        student_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        List submissions with optional filters.
        
        Tool: submissions-mcp.list_submissions
        Parameters:
        - assignment_id: int (optional)
        - student_id: int (optional)
        
        Returns: List of submissions
        """
        
        try:
            query = self.db.query(Submission)
            
            if assignment_id:
                query = query.filter(Submission.assignment_id == assignment_id)
            
            if student_id:
                query = query.filter(Submission.student_id == student_id)
            
            submissions = query.order_by(Submission.submitted_at.desc()).all()
            
            submissions_data = []
            for submission in submissions:
                submissions_data.append({
                    "id": submission.id,
                    "student_name": submission.student.name,
                    "assignment_name": submission.assignment.name,
                    "submitted_at": submission.submitted_at.isoformat(),
                    "language": submission.language
                })
            
            return {
                "status": "success",
                "count": len(submissions_data),
                "submissions": submissions_data
            }
        
        except Exception as e:
            logger.error(f"Error listing submissions: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }

    def get_tools(self) -> List[Dict[str, Any]]:
        """Return list of available tools in this MCP server."""
        return [
            {
                "name": "get_submission",
                "description": "Retrieve a submission with its source code",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "submission_id": {
                            "type": "integer",
                            "description": "The ID of the submission to retrieve"
                        }
                    },
                    "required": ["submission_id"]
                }
            },
            {
                "name": "get_commit_history",
                "description": "Retrieve commit history for a submission",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "submission_id": {
                            "type": "integer",
                            "description": "The ID of the submission"
                        }
                    },
                    "required": ["submission_id"]
                }
            },
            {
                "name": "list_submissions",
                "description": "List submissions with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "assignment_id": {
                            "type": "integer",
                            "description": "Filter by assignment ID (optional)"
                        },
                        "student_id": {
                            "type": "integer",
                            "description": "Filter by student ID (optional)"
                        }
                    }
                }
            }
        ]
