# Troubleshooting: "Could not import module 'main'" Error

## Error Message

```
ERROR: Could not import module "main"
ERROR: ASGI app could not be loaded
```

---

## Quick Fix - 3 Common Causes

### 1. Wrong Working Directory ❌ Most Common

**Problem:** Running uvicorn from the wrong directory

```powershell
# WRONG - Running from app/ directory
cd app
uvicorn main:app  # ❌ This will fail

# RIGHT - Running from backend/ directory
cd c:\Users\lenovo\OneDrive\Desktop\PII\backend
venv\Scripts\uvicorn app.main:app  # ✓ This works
```

**Solution:**
```powershell
# Always ensure you're in the backend directory
cd c:\Users\lenovo\OneDrive\Desktop\PII\backend
```

---

### 2. Incorrect Module Path ❌

**Problem:** Using wrong import path in uvicorn command

```powershell
# WRONG - These will fail
uvicorn main:app                    # ❌ Missing 'app' package
uvicorn backend.app.main:app        # ❌ Wrong path structure
uvicorn app/main:app                # ❌ Use dot notation, not slash
uvicorn app.main                    # ❌ Missing ':app' instance name

# RIGHT - Correct syntax
uvicorn app.main:app                # ✓ This works
#       │    │    └─ FastAPI instance name (defined in main.py)
#       │    └────── Python module (main.py)
#       └─────────── Python package (app/ directory)
```

**Solution:**
```powershell
# Always use this exact format
venv\Scripts\uvicorn app.main:app --host 127.0.0.1 --port 8000
```

---

### 3. Virtual Environment Not Activated / Dependencies Missing ❌

**Problem:** Dependencies not installed or wrong Python interpreter

```powershell
# WRONG - Using system Python
python -m uvicorn app.main:app      # ❌ May use wrong environment

# RIGHT - Using venv Python
venv\Scripts\uvicorn app.main:app   # ✓ Uses correct environment
```

**Solution:**
```powershell
# Reinstall dependencies if needed
cd c:\Users\lenovo\OneDrive\Desktop\PII\backend
venv\Scripts\pip install --upgrade pip
venv\Scripts\pip install --prefer-binary -r requirements.txt
```

---

## Complete Diagnostic Checklist

### Step 1: Verify Working Directory

```powershell
# Check current directory
Get-Location

# Should output:
# Path
# ----
# C:\Users\lenovo\OneDrive\Desktop\PII\backend

# If not, navigate to correct directory
cd c:\Users\lenovo\OneDrive\Desktop\PII\backend
```

### Step 2: Verify File Structure

```powershell
# Check that app directory exists
Test-Path app
# Should return: True

# Check that main.py exists
Test-Path app\main.py
# Should return: True

# Check that __init__.py exists
Test-Path app\__init__.py
# Should return: True
```

### Step 3: Verify Dependencies

```powershell
# Check if venv exists
Test-Path venv\Scripts\python.exe
# Should return: True

# Test imports
venv\Scripts\python -c "from app.main import app; print('Import OK')"
# Should output: Import OK
```

### Step 4: Verify App Instance

```powershell
# Verify FastAPI app instance exists
venv\Scripts\python -c "from app.main import app; print(f'App title: {app.title}')"
# Should output: App title: Programming Assignment Integrity Investigator
```

---

## Automated Solutions

### Solution 1: Use Startup Scripts (Easiest)

I've created automated startup scripts that handle all checks:

```powershell
# PowerShell
.\start_backend.ps1

# Or Windows Batch
start_backend.bat
```

These scripts will:
- ✓ Check working directory
- ✓ Verify venv exists
- ✓ Check dependencies
- ✓ Verify app imports
- ✓ Start server with correct settings

### Solution 2: Manual Startup (Traditional)

```powershell
# 1. Navigate to backend
cd c:\Users\lenovo\OneDrive\Desktop\PII\backend

# 2. Verify you're in the right place
Get-Location  # Should show: ...\PII\backend

# 3. Start server
venv\Scripts\uvicorn app.main:app --host 127.0.0.1 --port 8000
```

---

## Common Error Patterns and Solutions

### Error: "No module named 'app'"

**Cause:** Wrong working directory or PYTHONPATH issue

**Solution:**
```powershell
cd c:\Users\lenovo\OneDrive\Desktop\PII\backend
# Do NOT cd into app/
venv\Scripts\uvicorn app.main:app --host 127.0.0.1 --port 8000
```

---

### Error: "No module named 'fastapi'" or "No module named 'pydantic'"

**Cause:** Dependencies not installed in venv

**Solution:**
```powershell
cd c:\Users\lenovo\OneDrive\Desktop\PII\backend
venv\Scripts\pip install --prefer-binary -r requirements.txt
```

---

### Error: "cannot import name 'app' from 'app.main'"

**Cause:** Variable name mismatch in main.py

**Solution:**
Check that `app/main.py` contains:
```python
app = FastAPI(
    title="Programming Assignment Integrity Investigator",
    # ... rest of config
)
```

The variable must be named `app` to match `uvicorn app.main:app`

---

### Error: Port 8000 already in use

**Cause:** Previous uvicorn instance still running

**Solution:**
```powershell
# Kill existing Python processes
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

# Wait 2 seconds
Start-Sleep -Seconds 2

# Start server again
venv\Scripts\uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Or use a different port:
```powershell
venv\Scripts\uvicorn app.main:app --host 127.0.0.1 --port 8001
```

---

## Advanced Debugging

### Check Python Path

```powershell
venv\Scripts\python -c "import sys; print('\n'.join(sys.path))"
```

Should include:
- Current directory (empty string or '.')
- Path to backend directory

### Check Uvicorn Can Find Module

```powershell
venv\Scripts\python -c "import uvicorn; from uvicorn.importer import import_from_string; app = import_from_string('app.main:app'); print(f'Success: {app.title}')"
```

Should output: `Success: Programming Assignment Integrity Investigator`

### Verify All App Imports

```powershell
venv\Scripts\python -c "
from app.database import engine, Base, get_db, settings
from app.models import User, Student, Assignment
from app.schemas import UserResponse
from app.api.auth import get_current_user
from app.orchestrator.agent_orchestrator import AgentOrchestrator
print('All imports successful')
"
```

---

## If Nothing Works - Clean Reinstall

### Nuclear Option: Fresh Start

```powershell
# 1. Stop all Python processes
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

# 2. Remove virtual environment
Remove-Item -Recurse -Force venv

# 3. Remove Python cache
Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force

# 4. Create fresh venv
python -m venv venv

# 5. Install dependencies
venv\Scripts\pip install --upgrade pip
venv\Scripts\pip install --prefer-binary -r requirements.txt

# 6. Verify
venv\Scripts\python test_backend.py

# 7. Start server
venv\Scripts\uvicorn app.main:app --host 127.0.0.1 --port 8000
```

---

## Verification After Fix

Once the server starts successfully, you should see:

```
INFO:     Started server process [xxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Then verify:
- Health: http://127.0.0.1:8000/health
- Swagger: http://127.0.0.1:8000/docs

---

## Quick Reference Card

### ✓ Correct Startup Command
```powershell
cd c:\Users\lenovo\OneDrive\Desktop\PII\backend
venv\Scripts\uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### ✓ Using Startup Script
```powershell
cd c:\Users\lenovo\OneDrive\Desktop\PII\backend
.\start_backend.ps1
# or
start_backend.bat
```

### ✓ Verification Test
```powershell
cd c:\Users\lenovo\OneDrive\Desktop\PII\backend
venv\Scripts\python test_backend.py
```

---

## Summary

**Most Common Cause:** Wrong working directory (not in backend/)

**Quick Fix:**
```powershell
cd c:\Users\lenovo\OneDrive\Desktop\PII\backend
venv\Scripts\uvicorn app.main:app --host 127.0.0.1 --port 8000
```

**If that doesn't work:** Use one of the automated startup scripts or follow the clean reinstall steps above.
