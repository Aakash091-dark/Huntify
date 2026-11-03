# Huntify - Fully Automated Job Application System

## 🚀 What This Does

Huntify is a fully automated job application system that:

1. **Scrapes real jobs** from multiple job boards (LinkedIn, Naukri, Indeed, Instahyre, etc.)
2. **Extracts keywords from your resume** to search for relevant positions
3. **Matches jobs** to your skills and experience
4. **Tailors your resume** for each specific job posting
5. **Automatically fills and submits applications** using browser automation

## 📋 Prerequisites

### 1. Install Playwright Browsers

The system uses Playwright for browser automation. After installing requirements, run:

```bash
playwright install chromium
```

### 2. Prepare Your Resume

Place your resume at:
```
backend/storage/master_resume/base_resume.txt
```

Or use `.docx` format. The system will extract skills and keywords from it.

## 🎯 Quick Start

### Method 1: Command Line (Recommended for Testing)

```bash
# Navigate to backend directory
cd backend

# Run with default settings (visible browser)
python run_auto_apply.py

# Apply to 5 jobs with 70% minimum match
python run_auto_apply.py --max-jobs 5 --min-score 0.70

# Run in headless mode (no visible browser)
python run_auto_apply.py --headless

# Use specific job sources only
python run_auto_apply.py --sources "Naukri,Indeed,Instahyre"

# Prepare applications without auto-submitting (for review)
python run_auto_apply.py --no-auto-submit
```

### Method 2: API Endpoint

1. Start the FastAPI server:
```bash
cd backend
uvicorn app.main:app --reload
```

2. Make API call:
```bash
# Fully automated application
curl -X POST "http://localhost:8000/applications/auto-apply?max_jobs=10&min_score=0.60&headless=false"

# Or use the existing endpoint (prepares applications without submitting)
curl -X POST "http://localhost:8000/applications/start"
```

3. Access API docs at: http://localhost:8000/docs

## ⚙️ Configuration Options

### Command Line Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--max-jobs` | 10 | Maximum number of applications to submit |
| `--min-score` | 0.60 | Minimum match score (0.0-1.0) to apply |
| `--headless` | False | Run browser without visible window |
| `--no-auto-submit` | False | Prepare applications but don't submit |
| `--sources` | All | Comma-separated list of job sources |
| `--resume` | Default | Custom path to your resume file |

### Job Sources Available

- ✅ **Naukri** - Web scraping enabled
- ✅ **Instahyre** - Web scraping enabled
- ✅ **Indeed** - Web scraping enabled
- ✅ **LinkedIn** - Web scraping enabled
- 🔄 **Wellfound** - Basic implementation
- 🔄 **Foundit** - Needs implementation
- 🔄 **Cutshort** - Needs implementation
- 🔄 **CompanyCareers** - Needs implementation

## 📊 How It Works

### Step 1: Resume Parsing
```
Your resume → Extract skills, experience, preferred roles
```

### Step 2: Job Discovery
```
For each job source:
  - Build search query from your skills
  - Scrape job listings
  - Extract: title, company, location, URL, description
  - Filter: must have valid URL and company name
```

### Step 3: Matching & Scoring
```
For each job:
  - Calculate match score (0.0-1.0)
  - Based on: skill overlap, role match, experience fit
  - Filter: only jobs above min_score threshold
  - Sort: highest matches first
```

### Step 4: Resume Tailoring
```
For each matched job:
  - Analyze job description
  - Emphasize relevant skills
  - Generate tailored resume (DOCX + TXT)
  - Save: storage/tailored_resumes/{role}_{company}.docx
```

### Step 5: Automated Application
```
For each job with tailored resume:
  - Open job URL in browser (Playwright)
  - Click "Apply" button
  - Fill form fields:
    ✓ First name, last name
    ✓ Email, phone
    ✓ LinkedIn, GitHub
    ✓ Upload tailored resume
    ✓ Cover letter (auto-generated)
  - Click "Submit"
  - Verify submission success
  - Record result
```

## 🛡️ Safety Features

### Built-in Protections

1. **Rate Limiting**: 1-5 second delays between applications
2. **Human-Like Behavior**: Slow typing, random delays
3. **Error Handling**: Graceful failures, detailed logging
4. **Confirmation Required**: Asks before auto-submitting
5. **Visible Browser Mode**: Watch what's happening (default)
6. **Detailed Logs**: All actions logged to `huntify_automation.log`

### Recommendation for First Run

```bash
# Start with visible browser and no auto-submit
python run_auto_apply.py --no-auto-submit --max-jobs 3

# Review what it does, then enable auto-submit
python run_auto_apply.py --max-jobs 5
```

## 📁 File Structure

```
backend/
├── app/
│   ├── job_discovery/
│   │   └── connectors/          # Web scrapers for each job board
│   │       ├── naukri.py        # ✅ Real scraping
│   │       ├── instahyre.py     # ✅ Real scraping
│   │       ├── indeed.py        # ✅ Real scraping
│   │       └── linkedin.py      # ✅ Real scraping
│   │
│   ├── application_agent/
│   │   └── auto_applier.py      # 🆕 Browser automation engine
│   │
│   ├── autonomous/
│   │   ├── agent.py             # Manual review workflow
│   │   └── auto_agent.py        # 🆕 Fully automated workflow
│   │
│   └── resume_tailoring/
│       └── tailor.py            # Resume customization
│
├── storage/
│   ├── master_resume/           # Your base resume
│   └── tailored_resumes/        # Generated resumes
│
└── run_auto_apply.py            # 🆕 CLI interface
```

## 🔧 Troubleshooting

### Browser automation fails
```bash
# Reinstall Playwright browsers
playwright install chromium

# Check if chromium is installed
playwright --version
```

### No jobs found
```python
# Test individual connectors
from app.job_discovery.connectors.naukri import NaukriConnector
connector = NaukriConnector()
jobs = connector.fetch_jobs("Python Developer", limit=5)
print(jobs)
```

### Application not submitting
- Some sites use CAPTCHA or bot detection
- Some sites require login (LinkedIn)
- Use `--no-auto-submit` to review forms manually
- Check `huntify_automation.log` for details

### Rate limiting / IP blocks
- Add longer delays between applications
- Use VPN if blocked
- Reduce `--max-jobs` to smaller batches

## 🎓 Usage Examples

### Conservative Approach (Recommended First Time)
```bash
python run_auto_apply.py \
  --max-jobs 3 \
  --min-score 0.75 \
  --no-auto-submit \
  --sources "Naukri"
```

### Aggressive Approach (Multiple Sources)
```bash
python run_auto_apply.py \
  --max-jobs 20 \
  --min-score 0.60 \
  --headless \
  --sources "Naukri,Instahyre,Indeed"
```

### High-Quality Matches Only
```bash
python run_auto_apply.py \
  --max-jobs 5 \
  --min-score 0.85 \
  --sources "LinkedIn,Wellfound"
```

## 📈 Expected Results

### Typical Run (10 jobs, min score 0.60)
```
Jobs Evaluated: ~50-100
Jobs Matched: ~10-15
Applications Submitted: ~5-8 (success rate varies by site)
Time Required: ~5-15 minutes
```

### Success Rates by Platform
- **Naukri**: 60-80% (good compatibility)
- **Instahyre**: 50-70% (varies by company)
- **Indeed**: 40-60% (many redirect to company sites)
- **LinkedIn**: 20-40% (login required for Easy Apply)

## ⚠️ Important Notes

1. **Login Required**: Some sites (LinkedIn, Wellfound) require login. The system can't bypass authentication.

2. **CAPTCHAs**: Sites with bot protection may block automation. Use visible browser mode to solve CAPTCHAs manually.

3. **Dynamic Forms**: Some application forms are highly customized. The system handles common patterns but may need manual completion for complex forms.

4. **Legal Compliance**: Ensure web scraping complies with each site's Terms of Service.

5. **Resume Quality**: The better your base resume, the better the matching and tailoring.

6. **Job Board Changes**: Sites update their HTML frequently. Scrapers may need periodic updates.

## 🔄 Next Steps

After your first run:

1. Check `huntify_automation.log` for detailed activity
2. Review generated resumes in `storage/tailored_resumes/`
3. Verify applications at each job board's website
4. Adjust `--min-score` based on match quality
5. Fine-tune your base resume for better keyword matching

## 📞 Support

For issues or improvements:
- Check logs: `huntify_automation.log`
- Review code: `app/application_agent/auto_applier.py`
- Test scrapers individually in the `connectors/` directory

---

**Happy Job Hunting! 🎯**
