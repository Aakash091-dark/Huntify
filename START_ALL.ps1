# Huntify - Start Everything (Backend + Frontend)
# This script starts both backend and frontend in separate windows

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Starting Huntify Application" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

$huntifyPath = "c:\Users\Aakash\Desktop\Huntify"

# Check if backend directory exists
if (-not (Test-Path "$huntifyPath\backend")) {
    Write-Host "Error: Backend directory not found!" -ForegroundColor Red
    exit 1
}

# Check if frontend directory exists
if (-not (Test-Path "$huntifyPath\frontend")) {
    Write-Host "Error: Frontend directory not found!" -ForegroundColor Red
    exit 1
}

Write-Host "[1/3] Checking dependencies..." -ForegroundColor Yellow

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python not found" -ForegroundColor Red
    exit 1
}

# Check if Node.js is installed
try {
    $nodeVersion = node --version 2>&1
    Write-Host "  ✓ Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Node.js not found. Please install from nodejs.org" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[2/3] Starting Backend API..." -ForegroundColor Yellow
Write-Host "  Opening new terminal for backend..." -ForegroundColor Gray

# Start Backend in new PowerShell window
Start-Process powershell -ArgumentList @"
-NoExit -Command `"
Write-Host '================================' -ForegroundColor Cyan;
Write-Host 'Huntify Backend API' -ForegroundColor Cyan;
Write-Host '================================' -ForegroundColor Cyan;
Write-Host '';
cd '$huntifyPath\backend';
Write-Host 'Starting FastAPI server...' -ForegroundColor Yellow;
Write-Host '';
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
`"
"@

Write-Host "  ✓ Backend starting at http://localhost:8000" -ForegroundColor Green

Start-Sleep -Seconds 3

Write-Host ""
Write-Host "[3/3] Starting Frontend Dashboard..." -ForegroundColor Yellow
Write-Host "  Opening new terminal for frontend..." -ForegroundColor Gray

# Start Frontend in new PowerShell window
Start-Process powershell -ArgumentList @"
-NoExit -Command `"
Write-Host '================================' -ForegroundColor Cyan;
Write-Host 'Huntify Frontend Dashboard' -ForegroundColor Cyan;
Write-Host '================================' -ForegroundColor Cyan;
Write-Host '';
cd '$huntifyPath\frontend';
Write-Host 'Starting Vite dev server...' -ForegroundColor Yellow;
Write-Host '';
npm run dev
`"
"@

Write-Host "  ✓ Frontend starting at http://localhost:5173" -ForegroundColor Green

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Huntify Started Successfully! ✓" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Access your application:" -ForegroundColor Yellow
Write-Host "  Frontend Dashboard: http://localhost:5173" -ForegroundColor Cyan
Write-Host "  Backend API:        http://localhost:8000" -ForegroundColor Cyan
Write-Host "  API Documentation:  http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""

Write-Host "Two new terminal windows have opened:" -ForegroundColor Gray
Write-Host "  1. Backend API (don't close this)" -ForegroundColor Gray
Write-Host "  2. Frontend Dashboard (don't close this)" -ForegroundColor Gray
Write-Host ""

Write-Host "To stop the application:" -ForegroundColor Yellow
Write-Host "  Press Ctrl+C in each terminal window" -ForegroundColor Gray
Write-Host ""

Start-Sleep -Seconds 5

# Open browser automatically
Write-Host "Opening browser..." -ForegroundColor Yellow
Start-Process "http://localhost:5173"

Write-Host ""
Write-Host "Enjoy Huntify! 🎉" -ForegroundColor Green
Write-Host ""
