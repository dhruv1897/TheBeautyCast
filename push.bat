@echo off
setlocal
REM ===================================================================
REM  ONE-CLICK PUSH  -  The Beauty Cast
REM ===================================================================
REM  Double-click this file, or run:  push.bat "your message"
REM
REM  It sets up the virtual environment on first run, installs anything
REM  missing, runs the tests, and only pushes if they pass.
REM ===================================================================

REM Always work from the folder this file lives in, even on double-click.
cd /d "%~dp0"

REM --- 1. Find a usable Python -------------------------------------
REM Python 3.14 is very new and some packages have no build for it yet,
REM so prefer 3.12 if the launcher has it.
set PY=python
py -3.12 --version >nul 2>&1 && set PY=py -3.12

REM --- 2. Create the virtual environment on first run --------------
if not exist ".venv\Scripts\python.exe" (
    echo.
    echo === First run: creating virtual environment ===
    %PY% -m venv .venv
    if errorlevel 1 (
        echo.
        echo *** Could not create the virtual environment. ***
        echo *** Check Python is installed: python --version ***
        pause
        exit /b 1
    )
)

REM --- 3. Use the venv's own python directly ------------------------
REM This is more reliable than "activate" inside a batch file.
set VPY=.venv\Scripts\python.exe

REM --- 4. Install anything missing ---------------------------------
"%VPY%" -m pytest --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo === Installing dependencies, this takes a minute ===
    "%VPY%" -m pip install --upgrade pip
    "%VPY%" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo *** Install failed. Copy the red text above and send it to Claude. ***
        pause
        exit /b 1
    )
)

REM --- 5. Run the tests --------------------------------------------
echo.
echo === Running tests ===
"%VPY%" -m pytest -q
if errorlevel 1 (
    echo.
    echo *** TESTS FAILED - nothing was pushed. Fix the errors above. ***
    pause
    exit /b 1
)

REM --- 6. Commit ----------------------------------------------------
set MSG=%~1
if "%MSG%"=="" set MSG=Update site

echo.
echo === Committing: %MSG% ===
git add -A
git commit -m "%MSG%"
if errorlevel 1 echo (Nothing new to commit - continuing.)

REM --- 7. Push ------------------------------------------------------
echo.
echo === Pushing to GitHub ===
git push origin main
if errorlevel 1 (
    echo.
    echo *** PUSH FAILED ***
    echo *** Try:  git pull origin main   then run this again. ***
    pause
    exit /b 1
)

echo.
echo === Done. Changes are on GitHub. ===
pause
