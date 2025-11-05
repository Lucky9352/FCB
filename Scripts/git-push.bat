@echo off
REM ================================================
REM Git Push Script with Pre-Push Checks
REM Runs all necessary checks before pushing to GitHub
REM ================================================

echo.
echo ========================================
echo  TapNex Arena - Git Push
echo ========================================
echo.

cd ..

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM ================================================
REM PRE-PUSH CHECKS
REM ================================================

echo [Pre-Push Checks]
echo.

REM 1. Check for migrations
echo [1/6] Checking for pending migrations...
python manage.py makemigrations --dry-run --check >nul 2>&1
if errorlevel 1 (
    echo     ! Pending migrations detected. Creating them...
    python manage.py makemigrations
    if errorlevel 1 (
        echo     ERROR: Failed to create migrations!
        pause
        exit /b 1
    )
    echo     ✓ Migrations created
) else (
    echo     ✓ No pending migrations
)

REM 2. Run migrations (to ensure migrations work)
echo [2/6] Testing migrations...
python manage.py migrate --noinput
if errorlevel 1 (
    echo     ERROR: Migrations failed!
    pause
    exit /b 1
)
echo     ✓ Migrations successful

REM 3. Freeze requirements
echo [3/6] Updating requirements.txt...
pip freeze > requirements.txt
echo     ✓ requirements.txt updated

REM 4. Build CSS for production
echo [4/6] Building production CSS...
call npm run build-css-prod
if errorlevel 1 (
    echo     ERROR: CSS build failed!
    pause
    exit /b 1
)
echo     ✓ CSS built successfully

REM 5. Collect static files (to test)
echo [5/6] Testing static files collection...
python manage.py collectstatic --noinput --clear >nul 2>&1
if errorlevel 1 (
    echo     WARNING: Static files collection had issues
) else (
    echo     ✓ Static files OK
)

REM 6. Check for syntax errors
echo [6/6] Checking for Python syntax errors...
python -m py_compile manage.py >nul 2>&1
if errorlevel 1 (
    echo     ERROR: Python syntax errors found!
    pause
    exit /b 1
)
echo     ✓ No syntax errors

echo.
echo ========================================
echo  All pre-push checks passed!
echo ========================================
echo.

REM ================================================
REM GIT OPERATIONS
REM ================================================

echo [Git Operations]
echo.

REM Check if git repository exists
if not exist ".git" (
    echo ERROR: Not a git repository!
    echo Run "git init" first.
    pause
    exit /b 1
)

REM Get custom commit message or use default
set /p CUSTOM_MSG="Enter commit message (or press Enter for 'IC'): "
if "%CUSTOM_MSG%"=="" (
    set COMMIT_MSG=IC
) else (
    set COMMIT_MSG=%CUSTOM_MSG%
)

REM Stage all changes
echo [1/3] Staging changes...
git add .
if errorlevel 1 (
    echo     ERROR: Git add failed!
    pause
    exit /b 1
)
echo     ✓ Changes staged

REM Check if there are changes to commit
git diff-index --quiet HEAD --
if not errorlevel 1 (
    echo.
    echo No changes to commit.
    echo.
    pause
    exit /b 0
)

REM Commit changes
echo [2/3] Committing changes...
git commit -m "%COMMIT_MSG%"
if errorlevel 1 (
    echo     ERROR: Git commit failed!
    pause
    exit /b 1
)
echo     ✓ Changes committed

REM Push to GitHub
echo [3/3] Pushing to GitHub...
git push
if errorlevel 1 (
    echo     ERROR: Git push failed!
    echo     This might be a first push. Try: git push -u origin main
    pause
    exit /b 1
)
echo     ✓ Pushed to GitHub

echo.
echo ========================================
echo  Successfully pushed to GitHub!
echo ========================================
echo.
echo Commit: %COMMIT_MSG%
echo Branch: 
git branch --show-current
echo.
echo Your code is now on GitHub and will be deployed to Vercel.
echo.

pause
