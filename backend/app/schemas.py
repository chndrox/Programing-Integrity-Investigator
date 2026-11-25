from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class AgentTypeEnum(str, Enum):
    SIMILARITY_ANALYST = "similarity_analyst"
    TIMELINE_ANALYST = "timeline_analyst"
    EXCULPATORY_REVIEWER = "exculpatory_reviewer"
    CASE_WRITER = "case_writer"


# User Schemas
class UserBase(BaseModel):
    username: str
    email: str
    full_name: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


# Student Schemas
class StudentBase(BaseModel):
    student_id: str
    name: str
    email: str
    department: str


class StudentCreate(StudentBase):
    pass


class StudentResponse(StudentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Assignment Schemas
class AssignmentBase(BaseModel):
    name: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None


class AssignmentCreate(AssignmentBase):
    pass


class AssignmentResponse(AssignmentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Submission Schemas
class SubmissionBase(BaseModel):
    student_id: int
    assignment_id: int


class SubmissionCreate(SubmissionBase):
    pass


class SubmissionResponse(SubmissionBase):
    id: int
    file_name: str
    file_path: str
    language: str
    git_repo_url: Optional[str]
    submitted_at: datetime
    student: StudentResponse
    assignment: AssignmentResponse

    class Config:
        from_attributes = True


class SubmissionWithCodeResponse(SubmissionResponse):
    source_code: str


# Commit History Schemas
class CommitHistoryResponse(BaseModel):
    id: int
    commit_hash: str
    author: str
    message: str
    timestamp: datetime
    additions: int
    deletions: int

    class Config:
        from_attributes = True


# Agent Result Schemas
class AgentResultBase(BaseModel):
    agent_type: AgentTypeEnum
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class AgentResultResponse(AgentResultBase):
    id: int
    investigation_id: int
    status: str
    execution_time: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True


# Investigation Schemas
class InvestigationCreate(BaseModel):
    assignment_id: int
    submission_ids: List[int]


class InvestigationResponse(BaseModel):
    id: int
    assignment_id: int
    status: str
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    submissions: List[SubmissionResponse]
    agent_results: List[AgentResultResponse]

    class Config:
        from_attributes = True


# Case Report Schemas
class CaseReportResponse(BaseModel):
    id: int
    investigation_id: int
    report_content: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True


# Instructor Decision Schemas
class InstructorDecisionCreate(BaseModel):
    decision: str  # approved, needs_further_review, dismissed
    notes: Optional[str] = None


class InstructorDecisionResponse(InstructorDecisionCreate):
    id: int
    report_id: int
    user_id: int
    decided_at: datetime

    class Config:
        from_attributes = True


# Audit Log Schemas
class AuditLogResponse(BaseModel):
    id: int
    user_id: Optional[int]
    investigation_id: Optional[int]
    action: str
    details: Optional[Dict[str, Any]]
    created_at: datetime

    class Config:
        from_attributes = True


# Dashboard Schemas
class DashboardStats(BaseModel):
    total_submissions: int
    active_investigations: int
    cases_requiring_review: int
    completed_investigations: int
    risk_distribution: Dict[str, int]


class RecentInvestigation(BaseModel):
    id: int
    assignment_id: int
    status: str
    created_at: datetime
    submission_count: int


# Similarity Analysis Schemas
class SimilarityMatch(BaseModel):
    submission_1_id: int
    submission_2_id: int
    similarity_percentage: float
    matching_lines: List[Dict[str, Any]]
    unique_lines_1: int
    unique_lines_2: int


class TimelineEvidence(BaseModel):
    submission_id: int
    commit_count: int
    development_span_days: float
    commits: List[CommitHistoryResponse]
    incremental_development: bool


# MCP Status Schemas
class MCPToolResponse(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]


class MCPServerStatus(BaseModel):
    name: str
    connected: bool
    tools: List[MCPToolResponse]
    last_check: datetime
