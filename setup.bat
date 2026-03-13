@echo off
echo ======================================
echo  AI Medical Diagnosis System - Setup
echo ======================================

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.9, 3.10, or 3.11
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing dependencies...
pip install -r requirements-github.txt

echo.
echo ======================================
echo  Setup complete!
echo  Run the app with:
echo    venv\Scripts\activate
echo    streamlit run app.py
echo ======================================
pause
