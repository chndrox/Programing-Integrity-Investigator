# Programming Assignment Integrity Investigator (PII)

A comprehensive, AI-powered web application for investigating potential plagiarism in programming assignments. The system uses multiple specialized AI agents to analyze code similarity, development timelines, and provide evidence-based reports to instructors.

## 🎯 Project Overview

Traditional plagiarism detection tools rely primarily on code similarity scores. However, similar code doesn't necessarily prove plagiarism. This application investigates both:

1. **Code Similarity** - Token-based, AST-based, and line-by-line analysis
2. **Development Process** - Git commit history, timeline analysis, incremental development patterns

The system provides four independent AI agents that analyze different aspects of potential plagiarism, then synthesizes their findings into a balanced, evidence-based report for instructor review.

## 🏗️ Architecture

### Technology Stack

**Frontend:**
- React 18 with TypeScript
- Vite for fast development
- Tailwind CSS for styling
- Recharts for data visualization
- Monaco Editor for code viewing
- Lucide React for icons

**Backend:**
- Python 3.11+ with FastAPI
- SQLAlchemy ORM
- SQLite database (development)
- Groq API for LLM-powered reasoning
- GitPython for commit history analysis

**AI Architecture:**
- 4 specialized AI agents (Similarity, Timeline, Exculpatory, Case Writer)
- Central Agent Orchestrator
- Concurrent execution with configurable limits
- Groq API integration for reasoning

**MCP (Model Context Protocol):**
- submissions-mcp: Submission and commit data access
- similarity-mcp: Code comparison and cohort baseline analysis

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Groq API key (optional for demo mode)

### Backend Setup

1. Create virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file (copy from `.env.example`):
```bash
cp ../.env.example .env
# Edit .env with your Groq API key (or use demo mode)
```

4. Initialize database with sample data:
```bash
python sample_data.py
```

5. Run backend server:
```bash
python -m uvicorn app.main:app --reload
```

Backend will be available at `http://localhost:8000`

### Frontend Setup

1. Install dependencies:
```bash
cd Frontend
npm install
```

2. Start development server:
```bash
npm run dev
```

Frontend will be available at `http://localhost:3000`

### Default Demo Credentials

- **Username:** instructor1
- **Password:** password123

This account is pre-created with sample data loaded into the database.

## 📋 Features

### Dashboard
- Overview statistics (total submissions, active investigations, cases under review)
- Risk distribution visualization
- Recent investigation summary
- MCP server connection status

### Submissions
- Upload programming assignments (Python, Java, C++, JavaScript)
- Display submission history with metadata
- Search and filter submissions
- View source code directly

### Investigations
- Select multiple submissions for investigation
- Start plagiarism investigation workflow
- Track investigation progress (pending, in_progress, completed)
- View results from all four AI agents
- Access investigation details and reports

### Four AI Agents

#### 1. Similarity Analyst
- Performs deterministic code comparison
- Uses token-based, AST-based, and line-by-line analysis
- Identifies matching code blocks
- Calculates similarity percentages
- Groq enhances analysis with pattern interpretation

#### 2. Timeline Analyst
- Analyzes Git commit history
- Identifies incremental development patterns
- Detects unusual temporal patterns
- Compares development timelines between submissions
- Never treats missing history as proof of plagiarism

#### 3. Exculpatory Reviewer
- Represents the student's defense perspective
- Searches for evidence supporting independent development
- Identifies legitimate alternative explanations
- Challenges assumptions and identifies evidence weaknesses
- Works independently and critically

#### 4. Case Writer
- Synthesizes findings from all three agents
- Preserves disagreements between agents
- Identifies evidence gaps and uncertainties
- Provides neutral, balanced summary
- Never generates automatic verdicts

### Reports
- Evidence-based case reports
- Supporting and contradictory evidence
- Conflicting agent opinions preserved
- Investigation limitations documented
- Instructor guidance and recommendations

### Additional Features
- **MCP Tools** - View available Model Context Protocol tools and status
- **Settings** - Configure application and agent parameters
- **Audit Log** - Track all system activities
- **Student Management** - Student profiles and submission history
- **Theme Support** - Light and dark modes with persistence
- **Responsive Design** - Works on desktop and tablet

## 🗄️ Database Models

- **User** - Instructor accounts
- **Student** - Student profiles with metadata
- **Assignment** - Programming assignments
- **Submission** - Student submissions with source code
- **CommitHistory** - Git commit data for each submission
- **Investigation** - Investigation records with status
- **AgentResult** - Individual agent analysis results
- **CaseReport** - Generated investigation reports
- **InstructorDecision** - Instructor approval/review decisions
- **AuditLog** - Activity tracking

## 🔧 Configuration

Create `.env` file in project root:

```env
# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=mixtral-8x7b-32768

# Backend Configuration
DATABASE_URL=sqlite:///./pii.db
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Upload Configuration
MAX_FILE_SIZE=10485760
UPLOAD_DIR=./uploads

# Agent Configuration
AGENT_CONCURRENCY_LIMIT=2
AGENT_TIMEOUT_SECONDS=120

# MCP Configuration
USE_MOCK_MCP=true
```

## 🎨 Design Features

- **Premium SaaS Dashboard** - Inspired by Linear, GitHub, Vercel
- **Minimal & Clean UI** - Solid colors, no gradients or excessive shadows
- **Professional Typography** - Consistent spacing and hierarchy
- **Light & Dark Themes** - Full theme support with persistence
- **Smooth Animations** - Subtle interactions with Framer Motion
- **Responsive Layout** - Adapts to desktop, tablet, mobile

### Color Palette

**Light Theme:**
- Background: #F8FAFC
- Sidebar: #FFFFFF
- Cards: #FFFFFF
- Primary: #4F46E5
- Text: #0F172A
- Border: #E2E8F0

**Dark Theme:**
- Background: #0B1120
- Sidebar: #111827
- Cards: #172033
- Primary: #818CF8
- Text: #F8FAFC
- Border: #293548

## 📊 API Endpoints

### Authentication
- `POST /api/auth/login` - Login and get access token
- `POST /api/auth/register` - Register new instructor

### Dashboard
- `GET /api/dashboard/stats` - Dashboard statistics
- `GET /api/dashboard/recent-investigations` - Recent investigations

### Submissions
- `POST /api/submissions/upload` - Upload submission
- `GET /api/submissions` - List submissions
- `GET /api/submissions/{id}` - Get submission details
- `DELETE /api/submissions/{id}` - Delete submission

### Investigations
- `POST /api/investigations/start` - Start new investigation
- `GET /api/investigations` - List investigations
- `GET /api/investigations/{id}` - Get investigation details
- `GET /api/investigations/{id}/report` - Get investigation report

### Reports
- `POST /api/reports/{id}/approve` - Approve report
- `POST /api/reports/{id}/request-review` - Request further review
- `GET /api/reports` - List reports

### MCP & Settings
- `GET /api/mcp/status` - MCP server status
- `GET /api/settings` - Application settings

### Audit
- `GET /api/audit-logs` - Audit log entries

## 🔬 Agent Orchestration Workflow

1. **Submission Selection** - Instructor selects 2+ submissions
2. **Investigation Creation** - System creates investigation record
3. **Phase 1 (Parallel):**
   - Similarity Analyst analyzes code
   - Timeline Analyst examines commit history
4. **Phase 2 (Sequential):**
   - Exculpatory Reviewer examines Phase 1 results
5. **Phase 3 (Sequential):**
   - Case Writer synthesizes all findings
6. **Report Storage** - Results saved to database
7. **Instructor Review** - Instructor reviews and makes decision

## 🧪 Testing

The application includes:
- Sample data initialization script
- Mock MCP servers for demo mode
- Deterministic similarity algorithms
- Timeline analysis without external Git access

## ⚠️ Important Security Notes

1. **API Keys** - Groq API keys are stored only on backend, never exposed to frontend
2. **Input Validation** - All file uploads validated for size and content
3. **Authentication** - JWT token-based with secure password hashing
4. **Code Execution** - Submitted code is NOT executed - only analyzed statically
5. **Database** - Use production-grade database (PostgreSQL) for deployment
6. **HTTPS** - Always use HTTPS in production

## 🎓 Key Design Principles

1. **Never Automatic Accusation** - Reports never conclude guilt, only present evidence
2. **Preserve Disagreement** - When agents disagree, all opinions are preserved
3. **Explain Limitations** - Reports clearly state analysis limitations
4. **Independent Evidence** - Each agent works independently and critically
5. **Student Defense** - Exculpatory agent actively searches for evidence supporting innocence
6. **Instructor Authority** - Final decision rests with instructor, not AI

## 📝 Development Notes

### Project Structure

```
PII/
├── backend/
│   ├── app/
│   │   ├── agents/              # AI agents
│   │   ├── orchestrator/        # Agent coordination
│   │   ├── services/            # Business logic
│   │   ├── mcp/                 # MCP tools
│   │   ├── api/                 # API routes
│   │   ├── models.py            # Database models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── database.py          # DB configuration
│   │   └── main.py              # FastAPI app
│   ├── sample_data.py           # Demo data initialization
│   └── requirements.txt
├── Frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/               # Page components
│   │   ├── services/            # API services
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── .env.example
└── README.md
```

## 🚀 Deployment

### Backend (Production)
1. Use PostgreSQL instead of SQLite
2. Set `USE_MOCK_MCP=false` to connect real MCP servers
3. Use Gunicorn or similar WSGI server
4. Enable HTTPS
5. Set strong `SECRET_KEY`
6. Configure environment variables

### Frontend (Production)
1. Run `npm run build` to create optimized bundle
2. Deploy to static hosting (Vercel, Netlify, etc.)
3. Update API base URL to production backend
4. Configure CORS settings appropriately

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Groq API Documentation](https://console.groq.com/)

## 📄 License

This project is provided as-is for educational and research purposes.

## ✅ Verification

The application has been tested to ensure:
- ✓ All four AI agents execute independently
- ✓ Agent results are stored and retrievable
- ✓ Similarity analysis uses deterministic algorithms
- ✓ Timeline analysis works with database-stored commits
- ✓ Exculpatory agent provides balanced defense perspective
- ✓ Case writer synthesizes findings without automatic verdict
- ✓ Investigation history persists across sessions
- ✓ Frontend connects to live backend API
- ✓ Dashboard displays real data from database
- ✓ Theme toggle works with persistence
- ✓ Responsive design adapts to different screen sizes

---

**Last Updated:** November 2026

Built with ❤️ for academic integrity and fair investigations
