# Fix: "Could not import module 'main'" Error

## 🎯 Quick Solution

The error occurs when uvicorn cannot find the `app.main` module. Here's the immediate fix:

### ✅ Correct Command (Copy & Paste)

```powershell
cd c:\Users\lenovo\OneDrive\Desktop\PII\backend
venv\Scripts\uvicorn app.main:app --host 127.0.0.1 --port 8000
```

**Key Points:**
1. Must be in `backend/` directory (NOT in `app/`)
2. Must use `venv\Scripts\uvicorn` (NOT system uvicorn)
3. Module path is `app.main:app` (uses dot notation)

---

## 🚀 Even Easier: Use Startup Scripts

I've created automated scripts that handle everything:

### Option 1: PowerShell Script
```powershell
cd c:\Users\lenovo\OneDrive\Desktop\PII\backend
.\start_backend.ps1
```

### Option 2: Batch File
```powershell
cd c:\Users\lenovo\OneDrive\Desktop\PII\backend
start_backend.bat
```

These scripts automatically:
- ✓ Check you're in the correct directory
- ✓ Verify virtual environment exists
- ✓ Check dependencies are installed
- ✓ Verify app module can be imported
- ✓ Start the server with correct settings

---

## 🔍 Why This Error Happens

### Common Mistake #1: Wrong Directory
```powershell
# ❌ WRONG - In app/ directory
cd c:\Users\lenovo\OneDrive\Desktop\PII\backend\app
uvicorn main:app  # ERROR: Cannot find module

# ✓ RIGHT - In backend/ directory
cd c:\Users\lenovo\OneDrive\Desktop\PII\backend
venv\Scripts\uvicorn app.main:app  # Works!
```

### Common Mistake #2: Wrong Module Path
```powershell
# ❌ WRONG - Various incorrect paths
uvicorn main:app              # Missing package name
uvicorn app/main:app          # Wrong separator (use . not /)
uvicorn backend.app.main:app  # Too deep in path
uvicorn app.main              # Missing :app

# ✓ RIGHT - Correct module path
uvicorn app.main:app          # Package.module:instance
```

### Common Mistake #3: System Python Instead of Venv
```powershell
# ❌ WRONG - System Python may not have dependencies
uvicorn app.main:app

# ✓ RIGHT - Use venv Python
venv\Scripts\uvicorn app.main:app
```

---

## 📋 Step-by-Step Manual Fix

If you want to understand what's happening:

### Step 1: Navigate to Backend Directory
```powershell
cd c:\Users\lenovo\OneDrive\Desktop\PII\backend
```

### Step 2: Verify You're in the Right Place
```powershell
Get-Location
# Should show: ...\PII\backend

# Check app directory exists
Test-Path app
# Should return: True
```

### Step 3: Verify Dependencies Installed
```powershell
venv\Scripts\python -c "from app.main import app; print('OK')"
# Should output: OK

# If error, reinstall:
venv\Scripts\pip install --prefer-binary -r requirements.txt
```

### Step 4: Start Server
```powershell
venv\Scripts\uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Expected output:
```
INFO:     Started server process [xxxx]
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

## 🛠️ If Still Not Working

### Check 1: Verify File Structure
```powershell
# All these should return True
Test-Path app
Test-Path app\main.py
Test-Path app\__init__.py
Test-Path venv\Scripts\python.exe
```

### Check 2: Test Direct Import
```powershell
venv\Scripts\python -c "from app.main import app; print(f'Title: {app.title}')"
# Should output: Title: Programming Assignment Integrity Investigator
```

### Check 3: Clean Reinstall
If nothing else works:
```powershell
# Remove venv
Remove-Item -Recurse -Force venv

# Recreate
python -m venv venv
venv\Scripts\pip install --upgrade pip
venv\Scripts\pip install --prefer-binary -r requirements.txt

# Test
venv\Scripts\python test_backend.py

# Start
venv\Scripts\uvicorn app.main:app --host 127.0.0.1 --port 8000
```

---

## ✅ Verification

After starting successfully, verify these URLs work:

| Test | URL | Expected |
|------|-----|----------|
| Health Check | http://127.0.0.1:8000/health | `{"status": "healthy"}` |
| Swagger UI | http://127.0.0.1:8000/docs | Interactive API docs |
| OpenAPI Schema | http://127.0.0.1:8000/openapi.json | JSON schema |

---

## 📚 Additional Resources

- **TROUBLESHOOTING.md** - Detailed error diagnosis guide
- **start_backend.ps1** - Automated PowerShell startup script
- **start_backend.bat** - Automated batch file startup script
- **test_backend.py** - Verification test script

---

## 💡 Best Practice

**Always use the startup scripts** - they handle all the edge cases and verify everything before starting the server.

```powershell
cd c:\Users\lenovo\OneDrive\Desktop\PII\backend
.\start_backend.ps1
```

This is the most reliable way to start your backend.

---

## Summary

**Problem:** `Could not import module "main"`

**Root Cause:** Usually wrong working directory or incorrect module path

**Solution:**
```powershell
cd c:\Users\lenovo\OneDrive\Desktop\PII\backend
venv\Scripts\uvicorn app.main:app --host 127.0.0.1 --port 8000
```

**Or use the automated script:**
```powershell
.\start_backend.ps1
```

Your backend should now start successfully! 🎉
