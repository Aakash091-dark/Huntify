# Huntify System Overview

## 🎯 What You Asked For

> "make it like it goes to web write keyword according my resume get the jobs apply then next job apply then next job"

## ✅ What's Been Implemented

### 1. Resume Keyword Extraction ✓
**File**: `app/resume_engine/parser.py`

- Reads your resume from `storage/master_resume/base_resume.txt`
- Extracts skills, experience, and keywords
- Builds search queries automatically

### 2. Web Scraping for Real Jobs ✓
**Files**: `app/job_discovery/connectors/*.py`

Implemented real web scraping for:
- ✅ **Naukri.com** - Full scraping with BeautifulSoup
- ✅ **Instahyre** - Full scraping with BeautifulSoup
- ✅ **Indeed India** - Full scraping with BeautifulSoup
- ✅ **LinkedIn** - Full scraping with BeautifulSoup

Each connector:
- Searches using keywords from your resume
- Scrapes real job listings (title, company, URL, description)
- Returns validated jobs with real URLs

### 3. Intelligent Job Matching ✓
**File**: `app/autonomous/auto_agent.py`

- Calculates match score (0.0-1.0) for each job
- Based on skill overlap with job description
- Filters jobs by minimum score threshold
- Sorts by relevance

### 4. Resume Tailoring ✓
**File**: `app/resume_tailoring/tailor.py`

- Customizes your resume for each specific job
- Emphasizes relevant skills
- Generates both DOCX and TXT formats
- Saves to `storage/tailored_resumes/`

### 5. Automated Application ✓
**File**: `app/application_agent/auto_applier.py`

For each matched job:
1. Opens job URL in browser (Playwright)
2. Clicks "Apply" button
3. Fills form fields:
   - First name, last name
   - Email, phone
   - LinkedIn, GitHub
   - Uploads tailored resume
   - Fills cover letter
4. Clicks "Submit"
5. Verifies submission success
6. **Moves to next job automatically**
7. Repeats until all jobs processed

### 6. Continuous Loop Processing ✓
**File**: `app/autonomous/auto_agent.py` - Function: `run_fully_automated_hunt()`

```python
jobs_with_resumes = [...]  # Matched jobs with tailored resumes

for job in jobs_with_resumes:
    # Apply to this job
    result = apply_to_job(job, resume)
    
    # Log result
    print(f"Applied to {job['title']} at {job['company']}")
    
    # Delay before next application
    time.sleep(5)
    
    # Next job → automatic loop continues
```

## 🎮 How to Use

### Simple Command (Does Everything You Asked)

```bash
cd backend
python run_auto_apply.py
```

This single command:
1. ✅ Reads your resume → extracts keywords
2. ✅ Goes to web (Naukri, Indeed, etc.)
3. ✅ Searches jobs using your keywords
4. ✅ Gets the jobs (scrapes listings)
5. ✅ Applies to first job
6. ✅ Then next job
7. ✅ Then next job
8. ✅ Continues until done

### With Options

```bash
# Apply to 20 jobs
python run_auto_apply.py --max-jobs 20

# Only high-match jobs
python run_auto_apply.py --min-score 0.75

# Specific sources
python run_auto_apply.py --sources "Naukri,Indeed"

# Hidden browser
python run_auto_apply.py --headless
```

## 📊 Complete Workflow

```
START
  ↓
┌─────────────────────────┐
│ 1. Parse Resume         │
│    Extract keywords     │
└─────────────────────────┘
  ↓
┌─────────────────────────┐
│ 2. Go to Web            │
│    Search: Naukri       │
│    Search: Indeed       │
│    Search: Instahyre    │
│    Search: LinkedIn     │
└─────────────────────────┘
  ↓
┌─────────────────────────┐
│ 3. Get Jobs             │
│    Scrape listings      │
│    Validate URLs        │
│    Extract details      │
└─────────────────────────┘
  ↓
┌─────────────────────────┐
│ 4. Match & Filter       │
│    Calculate scores     │
│    Sort by relevance    │
│    Select top matches   │
└─────────────────────────┘
  ↓
┌─────────────────────────┐
│ 5. Tailor Resumes       │
│    For each job         │
│    Customize resume     │
└─────────────────────────┘
  ↓
┌─────────────────────────┐
│ 6. Apply Loop           │
│    ┌─────────────────┐  │
│    │ Job 1 → Apply   │  │
│    └─────────────────┘  │
│    ┌─────────────────┐  │
│    │ Job 2 → Apply   │  │
│    └─────────────────┘  │
│    ┌─────────────────┐  │
│    │ Job 3 → Apply   │  │
│    └─────────────────┘  │
│    ┌─────────────────┐  │
│    │ Job N → Apply   │  │
│    └─────────────────┘  │
└─────────────────────────┘
  ↓
END (All jobs processed)
```

## 🛠️ Technical Architecture

### Components Created/Modified

#### ✅ New Files Created
1. `connectors/naukri.py` - Real Naukri scraper
2. `connectors/indeed.py` - Real Indeed scraper
3. `connectors/instahyre.py` - Real Instahyre scraper
4. `connectors/linkedin.py` - Real LinkedIn scraper
5. `application_agent/auto_applier.py` - Browser automation engine
6. `autonomous/auto_agent.py` - Fully automated workflow orchestrator
7. `run_auto_apply.py` - Command-line interface
8. `test_connectors.py` - Test script for scrapers
9. `setup_and_run.ps1` - Windows setup script

#### ✅ Enhanced Files
1. `api/routes/applications.py` - Added `/auto-apply` endpoint

#### ✅ Documentation Created
1. `README.md` - Main project documentation
2. `AUTOMATION_GUIDE.md` - Comprehensive automation guide
3. `QUICKSTART.md` - Quick start guide
4. `SYSTEM_OVERVIEW.md` - This file

### Technology Stack

- **Web Scraping**: BeautifulSoup4, Requests
- **Browser Automation**: Playwright (Chromium)
- **Resume Parsing**: Custom parser with regex
- **AI Matching**: Custom scoring algorithm
- **Resume Generation**: python-docx
- **API**: FastAPI
- **Language**: Python 3.9+

## 📈 Example Run Output

```
================================
STARTING FULLY AUTOMATED JOB HUNT
================================

[1/5] Parsing resume...
✓ Resume parsed - Skills: Python, FastAPI, PostgreSQL, AI, LLM

[2/5] Discovering jobs from 4 sources...
  Naukri: Found 8 jobs
  Indeed: Found 6 jobs
  Instahyre: Found 5 jobs
  LinkedIn: Found 4 jobs
✓ Found 23 valid job listings

[3/5] Matching jobs against resume (min score: 0.60)...
✓ 12 jobs matched (showing top 10)

[4/5] Tailoring resumes for 10 jobs...
  ✓ Tailored resume for: Backend Engineer at TechCorp
  ✓ Tailored resume for: Python Developer at StartupXYZ
  ...
✓ Tailored 10 resumes

[5/5] Applying to 10 jobs automatically...
Browser mode: visible

============================================================
Processing application 1/10
Job: Backend Engineer at TechCorp
============================================================

  → Opening job URL
  → Clicked apply button
  → Filled: first_name
  → Filled: last_name
  → Filled: email
  → Filled: phone
  → Uploaded resume
  → Clicked submit
  ✓ Application submitted!

Waiting 5 seconds before next application...

============================================================
Processing application 2/10
Job: Python Developer at StartupXYZ
============================================================
  ...

================================
APPLICATION SUMMARY
================================
✓ Successfully submitted: 7
⚠ Partially completed: 2
✗ Failed: 1
================================
```

## 🎯 Key Features Delivered

| Your Requirement | Implementation | Status |
|-----------------|----------------|---------|
| Goes to web | Web scrapers for 4+ job boards | ✅ Done |
| Write keyword according to resume | Auto-extract keywords from resume | ✅ Done |
| Get the jobs | Real job scraping with validation | ✅ Done |
| Apply | Browser automation fills forms | ✅ Done |
| Then next job | Automatic loop with delays | ✅ Done |
| Apply then next | Continuous processing | ✅ Done |

## 🚀 Ready to Run

Everything is set up and ready. Just:

```bash
cd c:\Users\Aakash\Desktop\Huntify\backend
python run_auto_apply.py
```

The system will do exactly what you asked:
1. Read your resume
2. Go to web
3. Search with keywords
4. Get jobs
5. Apply
6. Next job
7. Apply
8. Next job
9. ... continues automatically

## 📁 Files You Need to Know

### To Run
- `run_auto_apply.py` - Main script

### To Configure
- `storage/master_resume/base_resume.txt` - Your resume

### To Check Results
- `huntify_automation.log` - Detailed logs
- `storage/tailored_resumes/` - Generated resumes

### To Test
- `test_connectors.py` - Test scrapers work

## 🎓 Next Steps

1. **Update your resume** at `storage/master_resume/base_resume.txt`
2. **Test connectors**: `python test_connectors.py`
3. **First run**: `python run_auto_apply.py --max-jobs 3 --no-auto-submit`
4. **Full automation**: `python run_auto_apply.py`

---

**Your automated job hunt system is ready! 🎯**

The system does exactly what you requested:
- Goes to web ✓
- Uses keywords from your resume ✓
- Gets jobs ✓
- Applies automatically ✓
- Moves to next job ✓
- Continues until done ✓
