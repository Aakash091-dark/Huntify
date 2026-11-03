# 🚀 Complete Huntify Start Guide

## Three Ways to Use Huntify

1. **Frontend Dashboard** (Visual Interface) ✨
2. **Command Line** (CLI Automation) ⚡
3. **API** (For Integration) 🔌

---

## Method 1: Frontend Dashboard (RECOMMENDED)

### Step 1: Install Dependencies (First Time Only)

**Backend:**
```powershell
cd c:\Users\Aakash\Desktop\Huntify\backend
pip install -r requirements.txt
playwright install chromium
```

**Frontend:**
```powershell
cd c:\Users\Aakash\Desktop\Huntify\frontend
npm install
```

### Step 2: Start Everything with One Command

```powershell
cd c:\Users\Aakash\Desktop\Huntify
.\START_ALL.ps1
```

This opens:
- ✅ Backend API at http://localhost:8000
- ✅ Frontend Dashboard at http://localhost:5173
- ✅ Browser automatically

### Step 3: Use the Dashboard

1. **Prepare Applications Mode:**
   - Click "Prepare Applications"
   - Discovers jobs and creates tailored resumes
   - Applications go to approval queue
   - You review and approve manually

2. **Auto-Apply Mode (NEW!):**
   - Click "🤖 Auto-Apply"
   - Configure settings:
     - Max Jobs: How many to apply to
     - Min Score: Match threshold (0.0-1.0)
     - Sources: Which job boards
     - Headless: Hide browser or show
   - Click "Start Auto-Apply"
   - Watch applications submit automatically!

---

## Method 2: Command Line (CLI)

### Quick Start

```powershell
cd c:\Users\Aakash\Desktop\Huntify\backend
python run_auto_apply.py
```

### With Options

```powershell
# Apply to 5 jobs, visible browser
python run_auto_apply.py --max-jobs 5

# Apply to 10 jobs, 75% minimum match
python run_auto_apply.py --max-jobs 10 --min-score 0.75

# Specific sources only
python run_auto_apply.py --sources "Naukri,Indeed,Instahyre"

# Hidden browser mode
python run_auto_apply.py --headless

# Prepare without submitting (safe mode)
python run_auto_apply.py --no-auto-submit
```

---

## Method 3: Direct API Calls

### Start Backend

```powershell
cd c:\Users\Aakash\Desktop\Huntify\backend
uvicorn app.main:app --reload
```

### API Endpoints

**View API Documentation:**
http://localhost:8000/docs

**Auto-Apply (POST):**
```bash
curl -X POST "http://localhost:8000/api/v1/applications/auto-apply?max_jobs=10&min_score=0.65&headless=false"
```

**Prepare Applications (POST):**
```bash
curl -X POST "http://localhost:8000/api/v1/applications/start"
```

**Get Dashboard (GET):**
```bash
curl "http://localhost:8000/api/v1/dashboard/summary"
```

**List Applications (GET):**
```bash
curl "http://localhost:8000/api/v1/applications/"
```

---

## 🎯 Recommended Workflow

### First Time Users

1. **Start with Frontend:**
   ```powershell
   .\START_ALL.ps1
   ```

2. **Test with "Prepare Applications":**
   - Click "Prepare Applications" button
   - Review what gets discovered
   - Check tailored resumes in `storage/tailored_resumes/`

3. **Try Auto-Apply with Safe Settings:**
   - Click "🤖 Auto-Apply"
   - Set Max Jobs: 3
   - Set Min Score: 0.70
   - Uncheck "headless" to watch
   - Click "Start Auto-Apply"

4. **Scale Up:**
   - Increase max jobs to 10-20
   - Lower min score to 0.60-0.65
   - Enable headless for faster processing

### Power Users

```powershell
# Run CLI in background
cd backend
python run_auto_apply.py --max-jobs 20 --min-score 0.60 --headless

# While monitoring in frontend
# Open another terminal:
cd frontend
npm run dev
# Visit http://localhost:5173
```

---

## 📊 What Each Method Does

### Frontend Dashboard
- ✅ Visual interface
- ✅ Real-time progress monitoring
- ✅ Configure settings with UI
- ✅ Review applications before submission
- ✅ View statistics and history
- ✅ Best for: Interactive use

### CLI
- ✅ Fully automated
- ✅ Can run in background
- ✅ Detailed logs
- ✅ Easy to schedule
- ✅ Best for: Automation & scheduling

### API
- ✅ Integrate with other tools
- ✅ Build custom interfaces
- ✅ Programmatic control
- ✅ Best for: Developers & integrations

---

## 🔧 Configuration Files

### Update Your Resume
```
backend/storage/master_resume/base_resume.txt
```
Put your actual resume here with skills, experience, projects.

### Check Results
```
backend/storage/tailored_resumes/     # Generated resumes
backend/huntify_automation.log         # Detailed logs
```

---

## 🎮 Frontend Features

### Dashboard Overview
- **Jobs Discovered**: Total jobs found from all sources
- **Applications Prepared**: Jobs matched to your profile
- **In Progress**: Currently being processed
- **Approved**: Ready for submission
- **Awaiting Approval**: Need your review

### Buttons

**"Prepare Applications"**
- Finds jobs
- Matches to your resume
- Creates tailored resumes
- Adds to approval queue
- Waits for your review

**"🤖 Auto-Apply"**
- Everything above PLUS
- Automatically opens each job
- Fills application forms
- Uploads tailored resume
- Submits automatically
- Moves to next job

### Settings Panel

When you click "🤖 Auto-Apply", you can configure:

1. **Maximum Jobs** (1-50)
   - How many applications to submit
   - Default: 10

2. **Minimum Match Score** (0.0-1.0)
   - Only apply to jobs above this score
   - 0.60 = 60% match
   - Default: 0.65

3. **Job Sources**
   - Comma-separated: "LinkedIn,Naukri,Indeed"
   - Empty = use all sources
   - Default: All

4. **Headless Mode**
   - ✅ Checked = Hidden browser (faster)
   - ❌ Unchecked = Visible browser (watch it work)
   - Default: Unchecked

---

## 🚦 Status Indicators

### Application Statuses

- **pending_review**: Ready for your approval
- **approved**: Approved by you
- **submitted**: Successfully submitted
- **partially_completed**: Form filled but couldn't confirm submission
- **failed**: Error occurred
- **ready_for_review**: Prepared, waiting for manual review

### Colors

- 🟢 Green = Success
- 🟡 Yellow = In Progress
- 🔵 Blue = Info
- 🔴 Red = Error

---

## 💡 Pro Tips

1. **First run**: Use visible browser to see what happens
2. **Test small**: Start with 3-5 jobs before scaling up
3. **Check logs**: `huntify_automation.log` has detailed info
4. **Update resume**: Better keywords = better matches
5. **Use both**: Frontend for monitoring + CLI for automation

---

## 🆘 Troubleshooting

### Frontend Won't Load

```powershell
# Check if backend is running
# Should see output at http://localhost:8000

# Check if frontend is running
# Should see output at http://localhost:5173

# Restart everything:
.\START_ALL.ps1
```

### Backend Errors

```powershell
# Check Python installation
python --version

# Reinstall dependencies
cd backend
pip install -r requirements.txt

# Check playwright
playwright install chromium
```

### Frontend Errors

```powershell
# Check Node.js installation
node --version

# Reinstall dependencies
cd frontend
Remove-Item -Recurse -Force node_modules
npm install
```

### Port Already in Use

```powershell
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID)
taskkill /PID <PID> /F

# Or use different port
uvicorn app.main:app --reload --port 8001
```

---

## 📝 Complete Example Session

**Terminal 1:**
```powershell
cd c:\Users\Aakash\Desktop\Huntify
.\START_ALL.ps1
```
*Two windows open - backend and frontend*

**Browser:**
1. Goes to http://localhost:5173 automatically
2. Click "🤖 Auto-Apply"
3. Set Max Jobs: 5
4. Set Min Score: 0.70
5. Uncheck headless
6. Click "Start Auto-Apply"
7. Watch browser automation work!

**Results:**
- Check dashboard for statistics
- View `storage/tailored_resumes/` for generated resumes
- Check `huntify_automation.log` for details

---

## ⚡ Quickest Possible Start

**Copy this into PowerShell:**
```powershell
cd c:\Users\Aakash\Desktop\Huntify ; .\START_ALL.ps1
```

Then in the browser that opens:
1. Click "🤖 Auto-Apply"
2. Click "Start Auto-Apply"
3. Done!

---

## 📚 Additional Resources

- **Frontend Details**: See [FRONTEND_START.md](FRONTEND_START.md)
- **CLI Details**: See [QUICKSTART.md](QUICKSTART.md)
- **Full Documentation**: See [AUTOMATION_GUIDE.md](AUTOMATION_GUIDE.md)
- **System Architecture**: See [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md)

---

**Happy Job Hunting! 🎯**

Now you have THREE ways to use Huntify - pick what works best for you!
