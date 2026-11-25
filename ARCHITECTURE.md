# System Architecture - Programming Assignment Integrity Investigator

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React + Vite)                   │
│  - Dashboard, Submissions, Investigations, Reports           │
│  - Light/Dark Theme Support                                 │
│  - Responsive Design (Desktop, Tablet, Mobile)             │
└──────────────────┬──────────────────────────────────────────┘
                   │ HTTP/REST API
                   │ (Axios + Bearer Token)
┌──────────────────▼──────────────────────────────────────────┐
│              Backend (FastAPI + Python 3.11)               │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ AI Agent Orchestration Layer                          │ │
│  │  ┌──────────────────────────────────────────────────┐ │ │
│  │  │ Agent Orchestrator (Controller)                 │ │ │
│  │  │  - Manages execution flow                       │ │ │
│  │  │  - Handles concurrency (limit: 2)              │ │ │
│  │  │  - Timeout management (120s default)           │ │ │
│  │  └──────────────────────────────────────────────────┘ │ │
│  │  ┌────────────┬────────────┬────────────┬──────────┐  │ │
│  │  │ Agent 1    │ Agent 2    │ Agent 3    │ Agent 4  │  │ │
│  │  │ Similarity │ Timeline   │ Exculpatory│ Case     │  │ │
│  │  │ Analyst    │ Analyst    │ Reviewer   │ Writer   │  │ │
│  │  └────────────┴────────────┴────────────┴──────────┘  │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Services Layer                                         │ │
│  │  ├─ Groq Service (LLM Integration)                    │ │
│  │  ├─ Similarity Service (Deterministic Analysis)      │ │
│  │  ├─ Timeline Service (Git History Analysis)          │ │
│  │  └─ Report Service                                   │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ MCP Layer                                              │ │
│  │  ├─ Submissions MCP (get_submission, commits)        │ │
│  │  └─ Similarity MCP (compare, cohort_baseline)        │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ REST API Layer                                         │ │
│  │  ├─ /api/auth (Login, Register)                      │ │
│  │  ├─ /api/submissions (Upload, List, Get)            │ │
│  │  ├─ /api/investigations (Create, List, Get, Report) │ │
│  │  ├─ /api/reports (Approve, Export)                  │ │
│  │  ├─ /api/mcp (Status)                               │ │
│  │  ├─ /api/settings (Configuration)                   │ │
│  │  └─ /api/audit-logs (Activity Tracking)             │ │
│  └────────────────────────────────────────────────────────┘ │
└───────────────────┬────────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
   ┌────────┐  ┌────────┐  ┌──────────┐
   │ SQLite │  │ Groq   │  │ External │
   │ DB     │  │ API    │  │ MCP      │
   │ (Dev)  │  │        │  │ Servers  │
   └────────┘  └────────┘  └──────────┘
```

## 🔄 Investigation Execution Flow

```
Instructor Selection
        │
        ▼
Investigation Created (pending)
        │
        ├─────────────────────────────────────────┐
        │                                         │
        ▼ (Parallel Phase)                       ▼
   ┌────────────────┐              ┌──────────────────┐
   │ Similarity     │              │ Timeline         │
   │ Analyst        │              │ Analyst          │
   │ (Runs)         │              │ (Runs)           │
   └────────────────┘              └──────────────────┘
        │ (Results)                 │ (Results)
        │                           │
        └───────────────┬───────────┘
                        │
                        ▼ (Sequential)
                   ┌────────────────┐
                   │ Exculpatory    │
                   │ Reviewer       │
                   │ (Uses both ^)  │
                   └────────────────┘
                        │ (Results)
                        │
                        ▼ (Sequential)
                   ┌────────────────┐
                   │ Case Writer    │
                   │ (Synthesizes)  │
                   └────────────────┘
                        │ (Report)
                        │
                        ▼
            Investigation Completed
                        │
                        ▼
            Results Stored in Database
                        │
                        ▼
            Instructor Reviews & Approves
```

## 🤖 Four AI Agents

### 1. Similarity Analyst
**Input:** 2+ Submission source codes
**Process:**
- Token-based similarity (Python tokenization)
- AST-based comparison (Abstract Syntax Tree)
- Line-by-line matching
- Function/variable name overlap
- Groq API: Interpret patterns and calculate confidence

**Output:**
```json
{
  "similarity_metrics": {
    "weighted_similarity": 68.5,
    "token_similarity": 72.1,
    "ast_similarity": 65.3,
    "line_similarity": 68.0,
    "name_overlap": 55.2
  },
  "matching_blocks": [...],
  "confidence_level": "medium",
  "limitations": [...]
}
```

### 2. Timeline Analyst
**Input:** Submission commit history
**Process:**
- Analyze commit frequency
- Identify incremental development
- Detect unusual temporal patterns
- Compare timelines between submissions
- Groq API: Interpret development patterns

**Output:**
```json
{
  "commit_count": 4,
  "timeline_span_days": 2.5,
  "incremental_development": true,
  "unusual_patterns": [...],
  "analysis": "..."
}
```

### 3. Exculpatory Reviewer
**Input:** Similarity + Timeline results
**Process:**
- Search for evidence of independent work
- Identify legitimate alternative explanations
- Challenge assumptions
- Find weaknesses in plagiarism claim
- Calculate plagiarism probability (0-100%)
- Groq API: Generate defense arguments

**Output:**
```json
{
  "defense_case": {
    "defense_arguments": [...],
    "supporting_evidence": [...],
    "weakness_in_prosecution": [...],
    "plagiarism_probability": 35,
    "independence_probability": 65
  },
  "contradictions_found": [...]
}
```

### 4. Case Writer
**Input:** All three agent results
**Process:**
- Synthesize findings
- Preserve disagreements
- Identify evidence gaps
- Explain limitations
- Groq API: Generate neutral report

**Output:**
```json
{
  "executive_summary": "...",
  "findings": {
    "similarity_findings": {...},
    "timeline_findings": {...},
    "exculpatory_findings": {...}
  },
  "evidence_synthesis": {
    "supporting_plagiarism": [...],
    "supporting_innocence": [...],
    "conflicting_opinions": [...]
  },
  "confidence_and_limitations": {...}
}
```

## 💾 Database Schema

### Core Tables

**Users**
- id (PK)
- username, email, full_name
- hashed_password
- role (instructor/admin)

**Students**
- id (PK)
- student_id, name, email, department

**Assignments**
- id (PK)
- name, description, due_date

**Submissions**
- id (PK)
- student_id (FK), assignment_id (FK)
- file_name, file_path, language
- source_code (TEXT)
- git_repo_url
- submitted_at

**CommitHistory**
- id (PK)
- submission_id (FK)
- commit_hash, author, message
- timestamp
- additions, deletions

**Investigations**
- id (PK)
- created_by (FK → User)
- status (pending/in_progress/completed/failed)
- created_at, started_at, completed_at

**investigation_submissions** (Many-to-Many)
- investigation_id (FK)
- submission_id (FK)

**AgentResults**
- id (PK)
- investigation_id (FK)
- agent_type (similarity/timeline/exculpatory/case_writer)
- status, result (JSON), error
- execution_time

**CaseReports**
- id (PK)
- investigation_id (FK)
- report_content (JSON)

**InstructorDecisions**
- id (PK)
- report_id (FK)
- user_id (FK)
- decision (approved/needs_review/dismissed)
- decided_at

**AuditLogs**
- id (PK)
- user_id (FK)
- investigation_id (FK)
- action
- details (JSON)
- created_at

## 🔌 MCP Integration

### Submissions MCP
**Tools:**
- `get_submission(id)` - Retrieve full submission
- `get_commit_history(id)` - Get commit history
- `list_submissions(assignment_id, student_id)` - List with filters

### Similarity MCP
**Tools:**
- `compare_submissions(id1, id2)` - Compare two submissions
- `get_cohort_baseline(assignment_id)` - Baseline statistics

### Implementation
- **Mock Mode** (Development): Uses database directly
- **Live Mode** (Production): Connects to external MCP servers
- Fallback: Mock mode if live connection fails

## 🔐 Security Layers

1. **Authentication:**
   - JWT token-based
   - Bearer token in Authorization header
   - Secure password hashing (bcrypt)

2. **Input Validation:**
   - Pydantic schemas for all endpoints
   - File size limits (10MB default)
   - File type restrictions (.py, .java, etc.)

3. **Data Protection:**
   - API keys stored server-side only
   - Groq key never exposed to frontend
   - User passwords hashed before storage

4. **Code Execution:**
   - NO execution of submitted code
   - Static analysis only
   - Safe tokenization and AST parsing

5. **Audit Trail:**
   - All actions logged
   - Investigation history preserved
   - User attribution tracked

## 📊 Data Flow Example

**Scenario:** Compare Alice's and Bob's submissions

```
1. User selects submissions → POST /api/investigations/start
2. Investigation created with status=pending
3. Orchestrator retrieves submissions from database
4. MCP layers (mock mode) return submission data
5. Similarity Analyst:
   - Tokenizes both codes
   - Parses AST
   - Calls Groq for interpretation
   - Returns 68% similarity
6. Timeline Analyst (parallel):
   - Loads commit history from DB
   - Analyzes patterns
   - Calls Groq for assessment
   - Returns incremental development = true
7. Exculpatory Reviewer (sequential):
   - Receives both results
   - Calls Groq with findings
   - Calculates plagiarism probability = 35%
8. Case Writer (sequential):
   - Receives all three results
   - Calls Groq to synthesize
   - Generates balanced report
9. All results saved to database
10. Investigation status = completed
11. Report available for instructor review
```

## 🎨 Frontend Architecture

### Component Hierarchy
```
App (Router, Theme Toggle)
├── Layout (Sidebar, TopBar)
│   ├── Dashboard (Stats, Charts)
│   ├── Submissions (Upload, List)
│   ├── Investigations (Create, List, Detail)
│   ├── Reports (View, Approve)
│   ├── Students
│   ├── MCPTools (Status)
│   ├── Settings (Configuration)
│   ├── AuditLog (Activity)
│   └── Login
└── Components
    ├── Header
    ├── Sidebar
    ├── Charts
    ├── Forms
    └── Tables
```

### State Management
- React Hooks (useState, useEffect)
- Context API for theme
- Local Storage for persistence
- Axios interceptors for auth

### Styling
- Tailwind CSS utility classes
- CSS variables for theming
- Responsive breakpoints
- Dark mode support

## 🧪 Testing Strategy

### Unit Tests (Backend)
- Similarity algorithms
- Timeline analysis
- Groq service error handling
- Database models

### Integration Tests
- Full investigation workflow
- API endpoints
- Agent orchestration
- MCP tool interfaces

### End-to-End Tests
- Login workflow
- Investigation creation
- Report generation
- UI interactions

## 📈 Performance Considerations

### Backend
- Database indexing on frequently queried fields
- Concurrent agent execution (limited to 2)
- Agent timeouts (120s default)
- Groq API rate limiting

### Frontend
- Code splitting for pages
- Lazy loading of components
- Memoization of expensive computations
- Local caching of API responses

### Database
- SQLite for development (acceptable)
- PostgreSQL recommended for production
- Query optimization
- Connection pooling

## 🚀 Deployment Architecture

### Development
- Localhost: Frontend (3000), Backend (8000)
- SQLite database
- Mock MCP servers
- Demo credentials

### Production
- Frontend: Static hosting (Vercel, Netlify)
- Backend: Cloud server (AWS, Azure, GCP)
- Database: PostgreSQL on managed service
- API: HTTPS with SSL certificate
- MCP: Real server connections
- Monitoring: Logs and alerts

## 📝 Configuration Management

### Environment Variables
```
GROQ_API_KEY - LLM access
GROQ_MODEL - Model selection
DATABASE_URL - Database connection
SECRET_KEY - JWT signing
AGENT_CONCURRENCY_LIMIT - Parallel agent limit
AGENT_TIMEOUT_SECONDS - Execution timeout
USE_MOCK_MCP - Mode selection
MAX_FILE_SIZE - Upload limit
```

### Application Settings
- Stored in `.env`
- Configurable via UI (/settings)
- Database configuration flexible
- Agent parameters adjustable

---

This architecture ensures scalability, maintainability, and extensibility while maintaining security and performance standards.
