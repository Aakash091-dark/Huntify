# 🎯 Huntify - AI-Powered Job Application Automation

**Fully automated job hunting system that finds jobs, tailors resumes, and applies automatically.**

## ✨ Features

- 🔍 **Automated Job Discovery** - Scrapes real jobs from LinkedIn, Naukri, Indeed, Instahyre, and more
- 🎯 **Smart Matching** - AI-powered matching based on your skills and experience
- 📝 **Resume Tailoring** - Automatically customizes your resume for each job
- 🤖 **Browser Automation** - Fills and submits applications automatically using Playwright
- 📊 **Application Tracking** - Tracks all applications with status and results
- 🔄 **Continuous Operation** - Applies to jobs one after another automatically

## 🚀 Quick Start

### 1. Setup (Windows)

```powershell
cd backend
.\setup_and_run.ps1
```

This will:
- Install Python dependencies
- Install Playwright browsers
- Create necessary directories
- Set up sample resume

### 2. Add Your Resume

Edit your resume at:
```
backend/storage/master_resume/base_resume.txt
```

Include: skills, experience, projects, education - the system extracts keywords from this.

### 3. Run Automated Job Hunt

```bash
cd backend

# Test run (3 jobs, manual review)
python run_auto_apply.py --max-jobs 3 --no-auto-submit

# Full automation (10 jobs, auto-submit)
python run_auto_apply.py

# Custom configuration
python run_auto_apply.py --max-jobs 5 --min-score 0.75 --sources "Naukri,Indeed"
```

## 📖 How It Works

```
Your Resume
    ↓
1. Parse skills & keywords
    ↓
2. Search job boards (Naukri, LinkedIn, Indeed, etc.)
    ↓
3. Scrape real job listings
    ↓
4. Match jobs to your profile (AI scoring)
    ↓
5. Tailor resume for each job
    ↓
6. Open job in browser (Playwright)
    ↓
7. Fill application form automatically
    ↓
8. Submit application
    ↓
9. Next job → Repeat
```

## ⚙️ Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `--max-jobs` | 10 | Maximum applications to submit |
| `--min-score` | 0.60 | Minimum match score (0.0-1.0) |
| `--headless` | False | Hide browser window |
| `--no-auto-submit` | False | Prepare but don't submit |
| `--sources` | All | Job sources to use |

## 📊 Job Sources

| Source | Status | Notes |
|--------|--------|-------|
| Naukri | ✅ Active | Real web scraping |
| Instahyre | ✅ Active | Real web scraping |
| Indeed | ✅ Active | Real web scraping |
| LinkedIn | ✅ Active | Real web scraping |
| Wellfound | 🔄 Basic | Needs enhancement |
| Foundit | 📝 Planned | Coming soon |
| Cutshort | 📝 Planned | Coming soon |

## 🎓 Usage Examples

### Conservative (First Time)
```bash
python run_auto_apply.py --max-jobs 3 --min-score 0.75 --no-auto-submit
```

### Moderate
```bash
python run_auto_apply.py --max-jobs 10 --min-score 0.65
```

### Aggressive (Multiple Sources)
```bash
python run_auto_apply.py --max-jobs 20 --min-score 0.60 --sources "Naukri,Indeed,Instahyre"
```

## 📁 Project Structure

```
Huntify/
├── backend/
│   ├── app/
│   │   ├── job_discovery/
│   │   │   └── connectors/          # Job board scrapers
│   │   ├── application_agent/
│   │   │   ├── automation.py        # Browser automation
│   │   │   └── auto_applier.py      # Auto application engine
│   │   ├── autonomous/
│   │   │   └── auto_agent.py        # Fully automated workflow
│   │   ├── resume_engine/
│   │   │   └── parser.py            # Resume parsing
│   │   └── resume_tailoring/
│   │       └── tailor.py            # Resume customization
│   ├── storage/
│   │   ├── master_resume/           # Your base resume
│   │   └── tailored_resumes/        # Generated resumes
│   ├── run_auto_apply.py            # CLI interface
│   └── setup_and_run.ps1            # Setup script
└── AUTOMATION_GUIDE.md              # Detailed guide
```

## 🛠️ API Endpoints

Start the server:
```bash
uvicorn app.main:app --reload
```

### Endpoints:

- `POST /applications/start` - Prepare applications (manual review)
- `POST /applications/auto-apply` - Fully automated application
- `GET /applications/` - List all applications
- `GET /applications/queue` - View pending applications
- `POST /applications/{id}/approve` - Approve an application

API docs: http://localhost:8000/docs

## 🔧 Troubleshooting

### No Jobs Found
```bash
# Test scrapers individually
python
>>> from app.job_discovery.connectors.naukri import NaukriConnector
>>> connector = NaukriConnector()
>>> jobs = connector.fetch_jobs("Python Developer", limit=5)
>>> print(f"Found {len(jobs)} jobs")
```

### Browser Issues
```bash
# Reinstall browsers
playwright install chromium
```

### Application Not Submitting
- Some sites use CAPTCHA (use visible mode)
- Some sites require login first
- Check logs: `huntify_automation.log`

## 📈 Expected Results

Typical run with 10 jobs:
- **Jobs Evaluated**: 50-100
- **Jobs Matched**: 10-15
- **Applications Submitted**: 5-8
- **Time**: 5-15 minutes

Success rates vary by platform (40-80%).

## ⚠️ Important Notes

1. **Login Required**: LinkedIn, Wellfound need login (automation can't handle this)
2. **CAPTCHAs**: Some sites have bot protection
3. **Terms of Service**: Ensure compliance with each site's ToS
4. **Rate Limits**: Built-in delays prevent blocking
5. **Manual Review**: Some applications may need manual completion

## 🔐 Safety Features

- ✅ Rate limiting between applications
- ✅ Human-like behavior (delays, typing speed)
- ✅ Visible browser mode (default)
- ✅ Detailed logging
- ✅ Confirmation before auto-submit
- ✅ Graceful error handling

## 📚 Documentation

- [AUTOMATION_GUIDE.md](AUTOMATION_GUIDE.md) - Comprehensive automation guide
- [API Documentation](http://localhost:8000/docs) - Interactive API docs

## 🤝 Contributing

Feel free to:
- Add new job board connectors
- Improve matching algorithms
- Enhance resume tailoring
- Add new automation features

## 📝 License

MIT License - See LICENSE file

## 🎉 Getting Started Checklist

- [ ] Run setup script: `.\setup_and_run.ps1`
- [ ] Update your resume in `storage/master_resume/base_resume.txt`
- [ ] Test with: `python run_auto_apply.py --max-jobs 3 --no-auto-submit`
- [ ] Review results in logs and tailored_resumes folder
- [ ] Run full automation: `python run_auto_apply.py`
- [ ] Check application status on job boards

---

**Happy Job Hunting! 🚀**

For detailed usage, see [AUTOMATION_GUIDE.md](AUTOMATION_GUIDE.md)
