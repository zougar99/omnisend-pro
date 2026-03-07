@echo off
title OmniSend Pro v6.0
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
    echo Install Python 3.8+ then try again.
    pause
    exit /b 1
)

call "%PYTHON_CMD%" %PYTHON_ARGS% app.py
pause
