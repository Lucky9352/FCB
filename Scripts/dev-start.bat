@echo off
REM ================================================
REM Development Server Start Script
REM Starts local development server with all services
REM ================================================

echo.
echo ========================================
echo  TapNex Arena - Development Server
echo ========================================
echo.

cd ..

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please create one first: python -m venv venv
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo [1/7] Activating virtual environment...
call venv\Scripts\activate.bat
echo     ✓ Virtual environment activated

REM Check for .env file
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Please create .env file from .env.example
    echo.
    pause
    exit /b 1
)

REM Install/Update dependencies
echo [2/7] Checking Python dependencies...
pip install -q -r requirements.txt
echo     ✓ Dependencies installed

REM Check Node dependencies
echo [3/7] Checking Node dependencies...
if not exist "node_modules" (
    echo     Installing Node modules...
    call npm install
) else (
    echo     ✓ Node modules already installed
)

REM Build Tailwind CSS
echo [4/7] Building Tailwind CSS...
call npm run build-css-prod
echo     ✓ CSS built successfully

REM Run database migrations
echo [5/7] Running database migrations...
python manage.py migrate --noinput
echo     ✓ Migrations applied

REM Collect static files
echo [6/7] Collecting static files...
python manage.py collectstatic --noinput --clear
echo     ✓ Static files collected

REM Start development server
echo [7/7] Starting development server...
echo.
echo ========================================
echo  Server is starting...
echo  Access at: http://localhost:8000
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver

REM This will only run if server stops
echo.
echo Server stopped.
pause
