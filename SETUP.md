# Setup Instructions for Programming Assignment Integrity Investigator

## ⚡ Quick Start (5 minutes)

### Windows Users

1. **Terminal 1 - Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python sample_data.py
python -m uvicorn app.main:app --reload
```
Backend runs on `http://localhost:8000`

2. **Terminal 2 - Frontend:**
```bash
cd Frontend
npm install
npm run dev
```
Frontend runs on `http://localhost:3000`

3. **Login:**
- Open browser to `http://localhost:3000`
- Username: `instructor1`
- Password: `password123`

### macOS/Linux Users

1. **Terminal 1 - Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python sample_data.py
python -m uvicorn app.main:app --reload
```

2. **Terminal 2 - Frontend:**
```bash
cd Frontend
npm install
npm run dev
```

3. **Login:** Same as above

## 🔧 Detailed Setup

### Prerequisites

- **Python:** 3.11 or higher
  - Check: `python --version`
  - Download: https://www.python.org/downloads/

- **Node.js:** 18+ and npm
  - Check: `node --version` and `npm --version`
  - Download: https://nodejs.org/

- **Git:** For version control
  - Download: https://git-scm.com/downloads

### Backend Setup (Python)

#### 1. Navigate to backend directory
```bash
cd backend
```

#### 2. Create virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Python dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure environment
Create `.env` file in project root (copy from `.env.example`):
```bash
# Windows
copy ..\.env.example ..\.env

# macOS/Linux
cp ../.env.example ../.env
```

Edit `.env` and set your preferences. For demo mode without Groq API:
```
USE_MOCK_MCP=true
GROQ_API_KEY=demo  # Will use mock mode
```

To use real Groq API:
1. Get API key from https://console.groq.com/
2. Set in `.env`: `GROQ_API_KEY=your_actual_key`

#### 5. Initialize database with sample data
```bash
python sample_data.py
```

Output:
```
Sample data initialized successfully!
Created: 1 instructor, 4 students, 1 assignment, 4 submissions with commit history
```

#### 6. Run backend server
```bash
python -m uvicorn app.main:app --reload
```

Backend available at:
- **API:** http://localhost:8000
- **Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

### Frontend Setup (React)

#### 1. Navigate to Frontend directory
```bash
cd Frontend
```

#### 2. Install Node dependencies
```bash
npm install
```

If you have issues:
```bash
# Clear npm cache
npm cache clean --force

# Remove node_modules and package-lock.json
rm -rf node_modules package-lock.json  # macOS/Linux
rmdir /s node_modules & del package-lock.json  # Windows

# Reinstall
npm install
```

#### 3. Start development server
```bash
npm run dev
```

Frontend available at: http://localhost:3000

#### 4. Build for production
```bash
npm run build
```

Output: `dist/` folder with optimized build

### Verify Everything Works

1. **Backend is running:**
   - Open http://localhost:8000/health
   - Should see: `{"status":"healthy"}`

2. **Frontend is running:**
   - Open http://localhost:3000
   - Should see login page

3. **Login works:**
   - Username: `instructor1`
   - Password: `password123`
   - Should redirect to dashboard

4. **Dashboard loads:**
   - See statistics cards
   - See recent investigations chart

## 📊 Testing the Full Investigation Workflow

### 1. View Sample Data
- Go to **Submissions** page
- Should see 4 submissions (Alice, Bob, Charlie, Diana)

### 2. Create Investigation
- Go to **Investigations** page
- Click "New Investigation"
- Select Assignment ID: `1`
- Select 2+ submissions (e.g., Alice + Bob)
- Click "Start Investigation"
- Watch investigation progress

### 3. View Results
- Investigation automatically runs all 4 agents
- Click "View Details" to see results
- Each agent shows independent analysis
- Status shows: pending → in_progress → completed

### 4. Check Reports
- Go to **Reports** page (after investigation completes)
- View case summary
- Instructor can approve/request review

## 🛠️ Troubleshooting

### Backend Issues

**"Module not found" errors:**
```bash
# Ensure virtual environment is activated
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Port 8000 already in use:**
```bash
# Use different port
python -m uvicorn app.main:app --reload --port 8001
```

**Database locked:**
```bash
# Remove existing database
rm pii.db  # macOS/Linux
del pii.db  # Windows

# Reinitialize
python sample_data.py
```

**Groq API errors:**
- Check `.env` has correct API key
- Or set `USE_MOCK_MCP=true` for demo mode
- Check internet connection

### Frontend Issues

**"React is not defined" errors:**
```bash
# Clear React cache and reinstall
rm -rf node_modules package-lock.json  # macOS/Linux
npm install
npm run dev
```

**Port 3000 already in use:**
```bash
# Kill process on port 3000
# Windows: netstat -ano | findstr :3000
# macOS/Linux: lsof -i :3000
```

**Can't connect to backend:**
- Ensure backend is running on port 8000
- Check CORS is enabled (it is by default)
- Check `.env` API_BASE_URL in frontend

### Database Issues

**Tables not created:**
```bash
# Backend creates tables automatically on startup
# If not: restart backend server
python -m uvicorn app.main:app --reload
```

**Sample data not loaded:**
```bash
# Run sample data script
cd backend
python sample_data.py
```

## 📱 Development Workflow

### Making Changes

**Backend (Python):**
1. Edit Python files
2. Server auto-reloads
3. Changes instant (except model/schema changes)

**Frontend (React):**
1. Edit `.tsx` files
2. HMR (Hot Module Reload) auto-updates
3. Changes instant

### Database Changes

If you modify `models.py`:
1. Delete `pii.db`
2. Run `python sample_data.py`
3. Backend recreates tables

## 🔑 Important Notes

### Demo Mode
- Sample data includes 4 students with varying similarity
- Submissions 1 & 2 have high similarity (intentional)
- Submission 3 & 4 have different algorithms (low similarity)
- Useful for testing investigation workflow

### Security for Development
- `.env` file contains sensitive data - never commit
- Sample password is for demo only
- Change in production

### Performance
- First investigation takes longer (agent initialization)
- Subsequent investigations faster
- Timeline depends on Groq API response time

## 🚀 Next Steps After Setup

1. **Explore Dashboard:**
   - Understand statistics
   - Review sample data

2. **Test Submission Upload:**
   - Try uploading Python files
   - Test with different code

3. **Run Investigations:**
   - Create investigation with sample submissions
   - Review agent results
   - Understand report structure

4. **Customize:**
   - Modify settings for agent timeouts
   - Adjust similarity thresholds
   - Add more sample data

## 📚 Additional Commands

### Backend

```bash
# Run tests (if added)
pytest

# Check code types
mypy app/

# Format code
black app/

# Check imports
isort app/
```

### Frontend

```bash
# Type check
npm run type-check

# Build production
npm run build

# Preview production build
npm run preview
```

## 🆘 Getting Help

1. Check terminal output for errors
2. Review `.env` configuration
3. Ensure all ports are available (3000, 8000)
4. Check that Python and Node versions are correct
5. Try restarting both servers

## ✅ Setup Verification Checklist

- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed
- [ ] Backend virtual environment created
- [ ] Backend dependencies installed
- [ ] `.env` file configured
- [ ] Sample data initialized
- [ ] Backend server running (port 8000)
- [ ] Frontend dependencies installed
- [ ] Frontend server running (port 3000)
- [ ] Can login with demo credentials
- [ ] Dashboard displays statistics
- [ ] Can view sample submissions
- [ ] Can create investigation
- [ ] Investigation completes successfully
- [ ] Can view agent results
- [ ] Theme toggle works
- [ ] Light and dark modes work

---

**Setup Complete!** 🎉

You now have a fully functional Programming Assignment Integrity Investigator system ready for testing and development.
