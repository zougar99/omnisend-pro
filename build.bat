@echo off
title OmniSend Pro — Building .EXE
echo ============================================
echo   OmniSend Pro v6.0 — Building .EXE
echo ============================================
echo.

cd /d "%~dp0"

set "PYTHON_CMD="
set "PYTHON_ARGS="
if exist "c:\Python314\python.exe" (
    set "PYTHON_CMD=c:\Python314\python.exe"
) else (
    where py >nul 2>&1
    if not errorlevel 1 (
        set "PYTHON_CMD=py"
        set "PYTHON_ARGS=-3"
    ) else (
        where python >nul 2>&1
        if not errorlevel 1 set "PYTHON_CMD=python"
    )
)

if not defined PYTHON_CMD (
    echo Python 3 was not found.
    echo Install Python 3.8+ then run this file again.
    pause
    exit /b 1
)

call "%PYTHON_CMD%" %PYTHON_ARGS% -m pip install -r requirements.txt

echo.
echo Building .EXE with PyInstaller...
echo.

call "%PYTHON_CMD%" %PYTHON_ARGS% -m PyInstaller --noconfirm --onefile --windowed --name "OmniSendPro" --icon=NONE --add-data "data;data" app.py

echo.
echo ============================================
if exist "dist\OmniSendPro.exe" (
    echo   BUILD SUCCESS!
    echo   Your .EXE is at: dist\OmniSendPro.exe
) else (
    echo   Build may have failed. Check errors above.
)
echo ============================================
echo.
pause
