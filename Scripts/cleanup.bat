@echo off
REM ================================================
REM Daily Cleanup Script for TapNex Arena
REM Run this before starting development each day
REM ================================================

echo.
echo ========================================
echo  TapNex Arena - Daily Cleanup
echo ========================================
echo.

cd ..

REM Clean Python cache files
echo [1/6] Cleaning Python cache files...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul
del /s /q *.pyo 2>nul
echo     ✓ Python cache cleaned

REM Clean build artifacts
echo [2/6] Cleaning build artifacts...
if exist staticfiles (
    rmdir /s /q staticfiles
    echo     ✓ staticfiles removed
) else (
    echo     - staticfiles already clean
)

REM Clean Node cache
echo [3/6] Cleaning Node cache...
if exist node_modules\.cache (
    rmdir /s /q node_modules\.cache
    echo     ✓ Node cache cleaned
) else (
    echo     - Node cache already clean
)

REM Clean log files
echo [4/6] Cleaning log files...
del /s /q *.log 2>nul
echo     ✓ Log files cleaned

REM Clean temp files
echo [5/6] Cleaning temp files...
del /s /q *.tmp 2>nul
del /s /q *~ 2>nul
echo     ✓ Temp files cleaned

REM Clean Django session files (optional)
echo [6/6] Cleaning Django sessions...
if exist db.sqlite3 (
    echo     - SQLite database found (keeping it for local dev)
) else (
    echo     - No SQLite database
)
echo     ✓ Cleanup complete

echo.
echo ========================================
echo  Cleanup Complete! 
echo ========================================
echo.
echo Your development environment is clean.
echo Run "dev-start.bat" to start the server.
echo.

pause
