# Huntify Setup and Run Script for Windows PowerShell

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Huntify - Automated Job Application Setup" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "[1/5] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ $pythonVersion found" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python not found. Please install Python 3.9+ from python.org" -ForegroundColor Red
    exit 1
}

# Install requirements
Write-Host ""
Write-Host "[2/5] Installing Python dependencies..." -ForegroundColor Yellow
python -m pip install -r requirements.txt --quiet
Write-Host "  ✓ Dependencies installed" -ForegroundColor Green

# Install Playwright browsers
Write-Host ""
Write-Host "[3/5] Installing Playwright browsers..." -ForegroundColor Yellow
playwright install chromium
Write-Host "  ✓ Chromium browser installed" -ForegroundColor Green

# Create directories if they don't exist
Write-Host ""
Write-Host "[4/5] Setting up directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "storage/master_resume" | Out-Null
New-Item -ItemType Directory -Force -Path "storage/tailored_resumes" | Out-Null
Write-Host "  ✓ Directories created" -ForegroundColor Green

# Check for base resume
Write-Host ""
Write-Host "[5/5] Checking for base resume..." -ForegroundColor Yellow
$resumeExists = Test-Path "storage/master_resume/base_resume.txt"
if (-not $resumeExists) {
    Write-Host "  ⚠ Base resume not found!" -ForegroundColor Yellow
    Write-Host "  Creating sample resume..." -ForegroundColor Yellow
    
    $sampleResume = @"
AAKASH SEHRAWAT
Backend Engineer | AI/ML Specialist

Email: aakashhssehrawat@gmail.com
Phone: +91 9217030815
LinkedIn: linkedin.com/in/aakash-sehrawat
GitHub: github.com/aakash-sehrawat

SUMMARY
Experienced Backend Engineer with 4.5 years of expertise in building scalable systems using Python, FastAPI, and modern cloud technologies. Strong background in AI/ML, LLM integration, and microservices architecture.

TECHNICAL SKILLS
- Languages: Python, JavaScript, SQL
- Frameworks: FastAPI, Django, React
- Databases: PostgreSQL, MongoDB, Redis
- Cloud & DevOps: Docker, Kubernetes, AWS, Azure
- AI/ML: LLM, RAG, Langchain, OpenAI, Claude
- Tools: Git, CI/CD, Celery, RabbitMQ

EXPERIENCE

Senior Backend Engineer | Tech Company | 2021 - Present
- Built scalable APIs using FastAPI serving 1M+ requests/day
- Implemented RAG-based AI systems using LangChain and vector databases
- Designed microservices architecture with Docker and Kubernetes
- Optimized database queries reducing response time by 60%

Backend Developer | Startup | 2020 - 2021
- Developed RESTful APIs using Python and Django
- Integrated third-party services and payment gateways
- Built real-time features using WebSockets and Redis

PROJECTS
- Job Application Automation System (Huntify)
  Built autonomous job application system using browser automation, AI matching, and resume tailoring

- AI-Powered Content Generator
  Developed LLM-based content generation platform with FastAPI backend

EDUCATION
Bachelor of Technology in Computer Science | 2016 - 2020

CERTIFICATIONS
- AWS Certified Developer
- Python Advanced Certification
"@
    
    Set-Content -Path "storage/master_resume/base_resume.txt" -Value $sampleResume
    Write-Host "  ✓ Sample resume created at storage/master_resume/base_resume.txt" -ForegroundColor Green
    Write-Host "  📝 Please update this file with your actual resume!" -ForegroundColor Yellow
} else {
    Write-Host "  ✓ Base resume found" -ForegroundColor Green
}

# Setup complete
Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Setup Complete! ✓" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Update your resume: storage/master_resume/base_resume.txt"
Write-Host "2. Run automated job hunt:"
Write-Host ""
Write-Host "   Quick Test (3 jobs, no auto-submit):" -ForegroundColor Cyan
Write-Host "   python run_auto_apply.py --max-jobs 3 --no-auto-submit"
Write-Host ""
Write-Host "   Full Run (10 jobs, auto-submit):" -ForegroundColor Cyan
Write-Host "   python run_auto_apply.py"
Write-Host ""
Write-Host "   Custom run:" -ForegroundColor Cyan
Write-Host "   python run_auto_apply.py --max-jobs 5 --min-score 0.70 --sources Naukri,Indeed"
Write-Host ""
Write-Host "For more options, see: AUTOMATION_GUIDE.md" -ForegroundColor Gray
Write-Host ""

# Offer to run now
$response = Read-Host "Would you like to run a test now? (yes/no)"
if ($response -eq "yes" -or $response -eq "y") {
    Write-Host ""
    Write-Host "Running test with 3 jobs (no auto-submit)..." -ForegroundColor Cyan
    Write-Host ""
    python run_auto_apply.py --max-jobs 3 --no-auto-submit --min-score 0.60
}
