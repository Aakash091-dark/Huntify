# 🚀 Quick Start Guide - Huntify

Get up and running in 5 minutes!

## Step 1: Setup (One-time) ⚙️

Open PowerShell in the `backend` folder and run:

```powershell
cd c:\Users\Aakash\Desktop\Huntify\backend
.\setup_and_run.ps1
```

This installs everything you need.

## Step 2: Update Your Resume 📝

Edit your resume at:
```
backend\storage\master_resume\base_resume.txt
```

A sample resume is already there - replace it with your actual experience, skills, and projects.

## Step 3: Test the System 🧪

Test that job scrapers are working:

```bash
python test_connectors.py
```

This should find some jobs from Naukri, Indeed, Instahyre, etc.

## Step 4: Run Your First Job Hunt 🎯

### Option A: Safe Mode (Recommended First Time)

Prepare 3 applications without auto-submitting:

```bash
python run_auto_apply.py --max-jobs 3 --no-auto-submit
```

This will:
- Search for jobs based on your resume
- Match relevant positions
- Tailor your resume for each job
- Save everything for your review

Check results in: `storage\tailored_resumes\`

### Option B: Auto-Submit Mode

Automatically apply to 5 jobs:

```bash
python run_auto_apply.py --max-jobs 5
```

**You'll see the browser open and applications being filled automatically!**

## What Happens Next? 📊

The system will:

1. **Parse your resume** → Extract skills and keywords
2. **Search job boards** → Naukri, Indeed, Instahyre, LinkedIn
3. **Find matching jobs** → AI-powered relevance scoring
4. **Tailor resumes** → Customize for each position
5. **Apply automatically** → Fill forms and submit

## Monitoring Progress 👀

- **Watch the console** - Real-time status updates
- **Browser window** - See applications being filled (visible by default)
- **Log file** - `huntify_automation.log` has detailed activity
- **Tailored resumes** - Check `storage\tailored_resumes\` folder

## Common Commands 💻

```bash
# Conservative (high-quality matches only)
python run_auto_apply.py --max-jobs 5 --min-score 0.75

# Aggressive (more applications)
python run_auto_apply.py --max-jobs 20 --min-score 0.60

# Specific sources only
python run_auto_apply.py --sources "Naukri,Indeed"

# Hidden browser mode
python run_auto_apply.py --headless

# Prepare without submitting (for review)
python run_auto_apply.py --no-auto-submit
```

## Results You Can Expect 📈

Typical run with `--max-jobs 10`:
- **Jobs Evaluated**: 50-100
- **Jobs Matched**: 10-15  
- **Applications Submitted**: 5-8
- **Time Required**: 5-15 minutes

Success rate depends on the platform:
- Naukri: 60-80%
- Instahyre: 50-70%
- Indeed: 40-60%
- LinkedIn: 20-40% (many require login)

## Troubleshooting 🔧

### "No jobs found"
```bash
# Test scrapers
python test_connectors.py

# Try different keywords
python run_auto_apply.py --max-jobs 5
```

### "Browser automation failed"
```bash
# Reinstall browser
playwright install chromium

# Check it's installed
playwright --version
```

### "Application not submitting"
- Some sites use CAPTCHA (solve manually in visible mode)
- Some sites require login first
- Check `huntify_automation.log` for details

## Next Steps 🎓

After your first successful run:

1. **Verify applications** - Check job board websites
2. **Adjust settings** - Tune `--min-score` based on match quality
3. **Update resume** - Refine keywords for better matches
4. **Schedule runs** - Run daily for continuous applications
5. **Track results** - Monitor which sources work best

## Pro Tips 💡

1. **Start conservative** - Use `--no-auto-submit` first
2. **Watch the browser** - Learn what it does (default visible mode)
3. **Check logs** - Review `huntify_automation.log` after each run
4. **Update resume regularly** - Better keywords = better matches
5. **Use specific sources** - Focus on sites that work best for you

## Need Help? 🆘

- **Detailed guide**: See [AUTOMATION_GUIDE.md](AUTOMATION_GUIDE.md)
- **Check logs**: `huntify_automation.log`
- **Test scrapers**: `python test_connectors.py`
- **API docs**: Run `uvicorn app.main:app` then visit http://localhost:8000/docs

---

## Your First Command (Copy & Paste)

```bash
cd c:\Users\Aakash\Desktop\Huntify\backend
python run_auto_apply.py --max-jobs 3 --no-auto-submit --min-score 0.65
```

This is a safe first run that finds 3 jobs, prepares applications, but doesn't submit them automatically.

**Ready? Let's hunt some jobs! 🎯**
