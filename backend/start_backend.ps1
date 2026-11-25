# PII Backend Startup Script
# This script ensures the backend starts correctly with all proper paths

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  PII Backend Server Startup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Host "✓ Working directory: $scriptDir" -ForegroundColor Green
Write-Host ""

# Check if venv exists
if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "✗ Virtual environment not found!" -ForegroundColor Red
    Write-Host "  Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Check if dependencies are installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
$checkDeps = & venv\Scripts\python -c "try: import fastapi, uvicorn, pydantic; print('OK')
except: print('MISSING')" 2>&1

if ($checkDeps -notlike "*OK*") {
    Write-Host "✗ Dependencies not installed!" -ForegroundColor Red
    Write-Host "  Installing dependencies..." -ForegroundColor Yellow
    & venv\Scripts\pip install --upgrade pip --quiet
    & venv\Scripts\pip install --prefer-binary -r requirements.txt
    Write-Host "✓ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "✓ Dependencies installed" -ForegroundColor Green
}

Write-Host ""

# Verify app can be imported
Write-Host "Verifying app module..." -ForegroundColor Yellow
$importCheck = & venv\Scripts\python -c "from app.main import app; print('OK')" 2>&1

if ($importCheck -like "*OK*") {
    Write-Host "✓ App module verified" -ForegroundColor Green
} else {
    Write-Host "✗ Cannot import app.main!" -ForegroundColor Red
    Write-Host "Error: $importCheck" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting steps:" -ForegroundColor Yellow
    Write-Host "1. Ensure you're in: c:\Users\lenovo\OneDrive\Desktop\PII\backend"
    Write-Host "2. Check that app/main.py exists"
    Write-Host "3. Run: venv\Scripts\pip install --prefer-binary -r requirements.txt"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting Uvicorn Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Server will start on: http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "Swagger UI available at: http://127.0.0.1:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the server
& venv\Scripts\uvicorn app.main:app --host 127.0.0.1 --port 8000
