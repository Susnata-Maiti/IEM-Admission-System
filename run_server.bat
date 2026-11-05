@echo off
title IEM Admission System - Nexus P4
echo ====================================================================
echo Starting IEM Admission System on Windows 11...
echo ====================================================================

:: Change directory to wherever this batch file is placed
cd /d "%~dp0"

:: 1. Try standard python command from PATH
where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    python run_server.py
    goto end
)

:: 2. Try Windows Python launcher 'py'
where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    py run_server.py
    goto end
)

:: 3. Try standard Windows AppData install directory
if exist "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" run_server.py
    goto end
)

echo.
echo [ERROR] Python was not found on your system PATH or AppData.
echo Please ensure Python 3.10+ is installed.
echo ====================================================================
pause

:end
