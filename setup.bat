@echo off
REM YuvaSaarthi - Windows Setup Script

echo ========================================
echo YuvaSaarthi Setup - Windows
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.9 or higher from python.org
    pause
    exit /b 1
)

echo [1/5] Python found
python --version

REM Create virtual environment
echo.
echo [2/5] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)

REM Activate virtual environment
echo.
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo [4/5] Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo.
echo [5/5] Installing dependencies...
echo This may take a few minutes...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo.
    echo Creating .env file...
    copy .env.example .env
    echo.
    echo [!] IMPORTANT: Edit .env file and add your API keys
)

REM Create directories
if not exist "data\documents" mkdir data\documents
if not exist "data\vectorstore" mkdir data\vectorstore

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file and add your API keys
echo 2. Run: python create_sample_data.py
echo 3. Run: python ingest_documents.py
echo 4. Start the bot:
echo    - Telegram: python telegram_bot.py
echo    - Web: streamlit run streamlit_app.py
echo.
pause
