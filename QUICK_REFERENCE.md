# Quick Reference Guide

## 🚀 Start the Application (30 seconds)

### Windows PowerShell - Two Terminals

**Terminal 1 (Backend):**
```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python sample_data.py
python -m uvicorn app.main:app --reload
```
✓ Backend ready at http://localhost:8000

**Terminal 2 (Frontend):**
```powershell
cd Frontend
npm install
npm run dev
```
✓ Frontend ready at http://localhost:3000

**Login:**
- URL: http://localhost:3000
- Username: `instructor1`
- Password: `password123`

---

## 📚 Directory Structure

```
PII/
├── backend/           # Python FastAPI backend
│   ├── app/
│   │   ├── agents/    # 4 AI agents
│   │   ├── services/  # Business logic
│   │   ├── mcp/       # MCP tools
│   │   ├── models.py  # Database
│   │   └── main.py    # FastAPI app
│   └── sample_data.py # Demo data
├── Frontend/          # React frontend
│   ├── src/
│   │   ├── pages/     # 10 pages
│   │   ├── components/
│   │   └── services/  # API calls
│   └── package.json
└── Documentation
    ├── README.md           # Full guide
    ├── SETUP.md            # Installation
    ├── ARCHITECTURE.md     # Design
    └── COMPLETION.md       # Delivery
```

---

## 🔑 Key Files

| File | Purpose |
|------|---------|
| `backend/app/main.py` | FastAPI application, all endpoints |
| `backend/app/models.py` | Database models (11 tables) |
| `backend/app/agents/*.py` | 4 AI agents |
| `backend/app/orchestrator/agent_orchestrator.py` | Agent coordinator |
| `Frontend/src/App.tsx` | React main app, routing |
| `Frontend/src/pages/*.tsx` | 10 application pages |
| `Frontend/src/services/api.ts` | API client |
| `.env.example` | Configuration template |

---

## 🎯 Key Features

### Dashboard
- Real statistics from database
- Charts with Recharts
- Recent investigations list

### Submissions
- Upload Python/Java/C++/JS files
- View submission history
- Display source code

### Investigations
- Select 2+ submissions
- Run 4-agent investigation
- View detailed results
- Agents run in real time

### Reports
- Evidence-based findings
- Supporting & contradictory evidence
- Instructor approval workflow

### Four AI Agents
1. **Similarity Analyst** - Code comparison analysis
2. **Timeline Analyst** - Commit history analysis
3. **Exculpatory Reviewer** - Defense perspective
4. **Case Writer** - Report synthesis

---

## 📊 Database

11 models automatically created:
- Users, Students, Assignments
- Submissions, CommitHistory
- Investigations, AgentResults
- CaseReports, InstructorDecisions
- AuditLogs

Data persists in `pii.db` (SQLite)

---

## 🔌 API Endpoints

```
POST   /api/auth/login                    # Login
POST   /api/submissions/upload            # Upload file
GET    /api/submissions                   # List submissions
POST   /api/investigations/start          # Start investigation
GET    /api/investigations                # List investigations
GET    /api/investigations/{id}           # Investigation details
GET    /api/investigations/{id}/report    # Investigation report
POST   /api/reports/{id}/approve          # Approve report
GET    /api/dashboard/stats               # Dashboard stats
GET    /api/mcp/status                    # MCP server status
GET    /api/audit-logs                    # Activity log
GET    /api/settings                      # Configuration
```

---

## 🎨 Pages

| Page | URL | Purpose |
|------|-----|---------|
| Login | `/login` | Authentication |
| Dashboard | `/` | Statistics & overview |
| Submissions | `/submissions` | Upload & manage |
| Investigations | `/investigations` | Create & track |
| Investigation Detail | `/investigations/:id` | Full results |
| Reports | `/reports` | Case reports |
| Students | `/students` | Student profiles |
| MCP Tools | `/mcp-tools` | Server status |
| Settings | `/settings` | Configuration |
| Audit Log | `/audit-log` | Activity tracking |

---

## 🧪 Test Workflow

1. **Login:** instructor1 / password123
2. **View Dashboard:** See 4 sample submissions
3. **Go to Submissions:** View Alice, Bob, Charlie, Diana
4. **Start Investigation:** Select submissions 1 & 2 (similar code)
5. **Wait for Results:** Agents run automatically
6. **View Details:** Click investigation to see all 4 agent results
7. **Review Report:** Case Writer synthesizes findings
8. **Approve:** Instructor makes decision

---

## ⚙️ Configuration

### .env Variables

```
GROQ_API_KEY=your_key_or_demo
GROQ_MODEL=mixtral-8x7b-32768
DATABASE_URL=sqlite:///./pii.db
AGENT_CONCURRENCY_LIMIT=2
AGENT_TIMEOUT_SECONDS=120
USE_MOCK_MCP=true
```

### Theme Support
- Light theme: Default (#F8FAFC bg)
- Dark theme: Toggle in top-right
- Persists in localStorage

---

## 🔧 Development Commands

**Backend:**
```bash
# Run server
python -m uvicorn app.main:app --reload

# API documentation
http://localhost:8000/docs

# Type checking
mypy app/

# Reset database
rm pii.db && python sample_data.py
```

**Frontend:**
```bash
# Dev server
npm run dev

# Production build
npm run build

# Type check
npm run type-check

# Preview build
npm run preview
```

---

## 🐛 Troubleshooting

**Backend won't start:**
- Activate virtual environment first
- Check port 8000 is free
- Delete `pii.db` and reinitialize

**Frontend won't start:**
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again
- Check port 3000 is free

**Can't login:**
- Run `python sample_data.py` to initialize
- Username: `instructor1`, Password: `password123`

**Investigation stuck:**
- Check backend console for errors
- Groq API might be timing out (120s default)
- Check `.env` has valid API key or `USE_MOCK_MCP=true`

**Database locked:**
- Kill Python process
- Delete `pii.db`
- Restart backend

---

## 📱 Responsive Breakpoints

- **Desktop:** 1024px+ (Full layout)
- **Tablet:** 768px-1023px (Adjusted sidebar)
- **Mobile:** <768px (Stacked layout)

---

## 🎓 Key Concepts

### Investigation Workflow
```
Submit Submissions
        ↓
Create Investigation
        ↓
Run Agents (Parallel: Similarity + Timeline)
        ↓
Run Exculpatory (Sequential: Uses both)
        ↓
Run Case Writer (Sequential: Synthesizes)
        ↓
Save Results to Database
        ↓
Instructor Reviews & Approves
```

### Agent Independence
Each agent runs independently:
- **Similarity Analyst:** Deterministic code analysis
- **Timeline Analyst:** Commit pattern analysis
- **Exculpatory Reviewer:** Defense evidence gathering
- **Case Writer:** Neutral synthesis

Disagreements preserved in final report.

---

## 🔐 Security

- ✓ JWT authentication
- ✓ Secure password hashing (bcrypt)
- ✓ API key backend-only
- ✓ Input validation
- ✓ File upload restrictions
- ✓ SQL injection prevention
- ✓ CORS configured
- ✓ Audit logging
- ✓ No code execution

---

## 📈 Performance Tips

- Groq API calls ~2-5s each (network dependent)
- Similarity analysis ~0.5-2s
- Timeline analysis ~0.3-1s
- Full investigation ~4-15s total

For faster development:
- Use mock mode (avoid Groq calls)
- Set shorter timeouts
- Increase concurrency limit if system allows

---

## 📞 Support

**Documentation:**
- README.md - Full guide
- SETUP.md - Installation
- ARCHITECTURE.md - Design
- COMPLETION.md - Delivery

**Common Issues:**
- Check SETUP.md troubleshooting section
- Review backend console logs
- Check frontend browser console
- Verify .env configuration

---

## 🚀 Deployment

**Simple (Development):**
```bash
# Just follow quick start above
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

**Production:**
1. Backend: Deploy to cloud (AWS, Azure, GCP)
2. Frontend: Deploy to CDN (Vercel, Netlify)
3. Database: Use PostgreSQL
4. Configure HTTPS
5. Set real Groq API key
6. Update CORS settings

---

## ✅ Verification

- [x] Backend starts without errors
- [x] Frontend builds and runs
- [x] Can login with demo credentials
- [x] Dashboard shows real data
- [x] Can upload submissions
- [x] Can create investigations
- [x] Agents run and complete
- [x] Results saved to database
- [x] Theme toggle works
- [x] All pages accessible

---

**Ready to use!** 🎉

Start with the quick start command and you're running in <5 minutes.
