@echo off
echo ===================================================
echo   CHURN AI ENTERPRISE - SYSTEM STARTUP
echo ===================================================
echo.
echo 1. Starting Backend API Services...
start cmd /k "python app.py"
echo 2. Starting Frontend Analytics Dashboard...
cd frontend
npm run dev
