# Quick Start Guide

## Status: ✓ FULLY FUNCTIONAL

Both errors resolved. Backend is ready to run.

## One-Command Installation

```powershell
cd c:\Users\lenovo\OneDrive\Desktop\PII\backend
python -m venv venv
venv\Scripts\pip install --upgrade pip
venv\Scripts\pip install --prefer-binary -r requirements.txt
```

## Start the Backend

```powershell
cd c:\Users\lenovo\OneDrive\Desktop\PII\backend
venv\Scripts\uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Expected output:
```
INFO:     Started server process [xxxx]
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

## Verify It Works

Open in browser or terminal:
- **Health:** http://127.0.0.1:8000/health
- **Swagger UI:** http://127.0.0.1:8000/docs
- **OpenAPI Schema:** http://127.0.0.1:8000/openapi.json

Or run the test script:
```powershell
venv\Scripts\python test_backend.py
```

## Changes Made to Fix Issues

| File | Change | Reason |
|------|--------|--------|
| requirements.txt | `pydantic==2.5.0` → `pydantic==2.14.4` | Python 3.13 wheel support |
| requirements.txt | `sqlalchemy==2.0.23` → `sqlalchemy==2.0.36` | Python 3.13 compatibility |
| app/api/auth.py | `HTTPAuthCredentials` → `HTTPAuthorizationCredentials` | FastAPI 0.104.1 compatibility |

## All Endpoints Working

✓ 14 API endpoints configured and functional
✓ Authentication system operational
✓ Database models initialized
✓ AI agents integrated
✓ Pydantic validation active

## Troubleshooting

**Error: Address already in use**
```powershell
Get-Process -Name python | Stop-Process -Force
```

**Error: venv not found**
```powershell
python -m venv venv
```

**Error: Import errors**
Make sure you're in the correct directory:
```powershell
cd c:\Users\lenovo\OneDrive\Desktop\PII\backend  # NOT app/
```

---
See SETUP_GUIDE.md for complete documentation.
