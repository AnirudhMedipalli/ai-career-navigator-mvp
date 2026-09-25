@echo off
setlocal

set "PROJECT_DIR=%~dp0"
set "PYTHON=%PROJECT_DIR%.venv\Scripts\python.exe"

if not exist "%PYTHON%" if exist "%PROJECT_DIR%..\.venv\Scripts\python.exe" set "PYTHON=%PROJECT_DIR%..\.venv\Scripts\python.exe"

if not exist "%PYTHON%" (
    where py >nul 2>nul
    if errorlevel 1 (
        echo Python 3 was not found. Install Python 3 and try again.
        pause
        exit /b 1
    )
    echo Creating a virtual environment...
    py -3 -m venv "%PROJECT_DIR%.venv"
    if errorlevel 1 (
        echo Could not create the virtual environment.
        pause
        exit /b 1
    )
    set "PYTHON=%PROJECT_DIR%.venv\Scripts\python.exe"
)

"%PYTHON%" -c "import streamlit, pandas, numpy, sklearn, plotly, pypdf, dotenv" >nul 2>nul
if errorlevel 1 (
    echo Installing project dependencies...
    "%PYTHON%" -m pip install -r "%PROJECT_DIR%requirements.txt"
    if errorlevel 1 (
        echo Could not install project dependencies.
        pause
        exit /b 1
    )
)

pushd "%PROJECT_DIR%"
"%PYTHON%" -m streamlit run app\app.py
set "EXIT_CODE=%ERRORLEVEL%"
popd

if not "%EXIT_CODE%"=="0" pause
exit /b %EXIT_CODE%