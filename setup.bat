@echo off
REM Strava Dashboard Setup Script for Windows
REM This script sets up the virtual environment and installs all dependencies

echo ==========================================
echo Strava Dashboard Setup
echo ==========================================
echo.

REM Check Python version
echo Checking Python version...
python --version

if %errorlevel% neq 0 (
    echo Error: Python is not installed!
    echo Please install Python 3.9 or higher
    pause
    exit /b 1
)

echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

if %errorlevel% neq 0 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

echo Virtual environment created successfully!
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Activate the virtual environment:
echo    venv\Scripts\activate
echo.
echo 2. Configure your Strava API credentials:
echo    copy .env.example .env
echo    REM Then edit .env with your credentials
echo.
echo 3. Run authentication:
echo    python auth.py
echo.
echo 4. Fetch your data:
echo    python data_manager.py
echo.
pause
