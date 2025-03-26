@echo off
echo Setting up AI Plant Care Assistant...

:: Create directory structure
echo Creating directories...
mkdir templates 2>nul
mkdir static\css 2>nul
mkdir static\js 2>nul
mkdir static\images 2>nul
mkdir uploads 2>nul

:: Copy files if they exist
echo Copying files...
if exist "app.py" copy "app.py" . >nul
if exist "config.py" copy "config.py" . >nul
if exist "model.py" copy "model.py" . >nul
if exist "utils.py" copy "utils.py" . >nul
if exist "requirements.txt" copy "requirements.txt" . >nul

:: Copy template files
if exist "templates\*.html" copy "templates\*.html" templates\ >nul

:: Copy static files
if exist "static\css\style.css" copy "static\css\style.css" static\css\ >nul
if exist "static\js\app.js" copy "static\js\app.js" static\js\ >nul
if exist "static\js\sw.js" copy "static\js\sw.js" static\js\ >nul
if exist "static\images\favicon.ico" copy "static\images\favicon.ico" static\images\ >nul

:: Set up Python virtual environment
echo Setting up Python virtual environment...
python -m venv venv
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo Setup complete!
echo To start the application:
echo 1. Run: venv\Scripts\activate.bat
echo 2. Run: python app.py
echo 3. Open http://localhost:5000 in your browser

pause
