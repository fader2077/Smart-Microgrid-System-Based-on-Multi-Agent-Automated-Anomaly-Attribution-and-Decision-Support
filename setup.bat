@echo off
echo ========================================
echo Smart Grid AI Operator - Setup Script
echo ========================================
echo.

echo [Step 1/3] Checking Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.10+
    pause
    exit /b 1
)
echo.

echo [Step 2/3] Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo [Step 3/3] Checking Ollama...
where ollama >nul 2>nul
if %errorlevel% neq 0 (
    echo WARNING: Ollama not found in PATH
    echo.
    echo Please install Ollama:
    echo   1. Visit https://ollama.ai
    echo   2. Download and install for Windows
    echo   3. Run: ollama pull llama3.1
    echo.
) else (
    echo Ollama found!
    echo Checking if llama3.1 is installed...
    ollama list | findstr llama3.1
    if %errorlevel% neq 0 (
        echo.
        echo Installing llama3.1 model...
        ollama pull llama3.1
    )
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To test the system:
echo   python test_system.py
echo.
echo To run the web UI:
echo   streamlit run app.py
echo.
pause
