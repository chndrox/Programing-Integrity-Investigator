@echo off
REM PII Backend Startup Script (Windows Batch)

echo ========================================
echo   PII Backend Server Startup
echo ========================================
echo.

REM Change to script directory
cd /d "%~dp0"

echo Current directory: %CD%
echo.

REM Check if venv exists
if not exist "venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found!
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created.
    echo.
)

REM Check dependencies
echo Checking dependencies...
venv\Scripts\python -c "try: import fastapi, uvicorn, pydantic; print('OK')" 2>nul
if errorlevel 1 (
    echo [WARNING] Dependencies not fully installed
    echo Installing dependencies...
    venv\Scripts\pip install --upgrade pip --quiet
    venv\Scripts\pip install --prefer-binary -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    echo Dependencies installed successfully.
    echo.
)

REM Verify app import
echo Verifying app module...
venv\Scripts\python -c "from app.main import app; print('OK')" 2>nul
if errorlevel 1 (
    echo [ERROR] Cannot import app.main module!
    echo.
    echo Troubleshooting:
    echo 1. Ensure you are in the backend directory
    echo 2. Check that app/main.py exists
    echo 3. Reinstall dependencies: venv\Scripts\pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo App module verified successfully.
echo.
echo ========================================
echo   Starting Uvicorn Server
echo ========================================
echo.
echo Server URL:    http://127.0.0.1:8000
echo Swagger UI:    http://127.0.0.1:8000/docs
echo Health Check:  http://127.0.0.1:8000/health
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server
venv\Scripts\uvicorn app.main:app --host 127.0.0.1 --port 8000
