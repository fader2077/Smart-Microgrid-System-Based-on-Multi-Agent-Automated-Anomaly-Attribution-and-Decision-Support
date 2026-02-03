@echo off
REM Smart Microgrid AI System - Enterprise Edition Launcher
REM FastAPI + Chainlit Architecture

echo ============================================================
echo SMART MICROGRID AI SYSTEM - ENTERPRISE EDITION
echo ============================================================
echo.

REM Check if Ollama is running
echo [1/3] Checking Ollama...
ollama list >nul 2>&1
if %errorlevel% neq 0 (
    echo    WARNING: Ollama may not be running
    echo    Please start Ollama first: ollama serve
    pause
    exit /b 1
)
echo    OK - Ollama is running

REM Check if virtual environment exists
if exist "venv\" (
    echo [2/3] Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo [2/3] No virtual environment found, using global Python
)

REM Start FastAPI server with Chainlit
echo [3/3] Starting FastAPI server...
echo.
echo ============================================================
echo SERVER INFORMATION
echo ============================================================
echo FastAPI Server: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo AI Chat Interface: http://localhost:8000/chat
echo ============================================================
echo.
echo Press CTRL+C to stop the server
echo.

set PYTHONPATH=%CD%
uvicorn app.server:app --host 0.0.0.0 --port 8000 --reload

pause
