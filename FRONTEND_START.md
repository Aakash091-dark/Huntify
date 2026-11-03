# 🎨 How to Start Huntify Frontend

## 🚀 Quick Start (2 Terminals Needed)

### Terminal 1: Start Backend API

```powershell
# Open PowerShell Terminal 1
cd c:\Users\Aakash\Desktop\Huntify\backend
uvicorn app.main:app --reload
```

**Backend will run at:** http://localhost:8000

---

### Terminal 2: Start Frontend

```powershell
# Open PowerShell Terminal 2
cd c:\Users\Aakash\Desktop\Huntify\frontend
npm run dev
```

**Frontend will run at:** http://localhost:5173

---

## 📋 First Time Setup

### 1. Install Frontend Dependencies (First Time Only)

```powershell
cd c:\Users\Aakash\Desktop\Huntify\frontend
npm install
```

### 2. Install Backend Dependencies (First Time Only)

```powershell
cd c:\Users\Aakash\Desktop\Huntify\backend
pip install -r requirements.txt
playwright install chromium
```

---

## 🎯 Complete Startup Process

### Copy & Paste Commands:

**Terminal 1 (Backend):**
```powershell
cd c:\Users\Aakash\Desktop\Huntify\backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 (Frontend):**
```powershell
cd c:\Users\Aakash\Desktop\Huntify\frontend
npm run dev
```

---

## 🌐 Access Your Application

Once both are running:

1. **Frontend Dashboard:** http://localhost:5173
2. **Backend API:** http://localhost:8000
3. **API Documentation:** http://localhost:8000/docs
4. **API Redoc:** http://localhost:8000/redoc

---

## 🎨 What the Frontend Shows

The frontend dashboard displays:

- ✅ **Job Discovery** - Search and view available jobs
- ✅ **Application Queue** - Pending applications
- ✅ **Application Status** - Track submitted applications
- ✅ **Resume Management** - Upload and manage resumes
- ✅ **Automation Controls** - Start/stop auto-apply
- ✅ **Statistics** - Application metrics and success rates

---

## 🔧 Troubleshooting

### Frontend Won't Start

```powershell
# Delete node_modules and reinstall
cd c:\Users\Aakash\Desktop\Huntify\frontend
Remove-Item -Recurse -Force node_modules
Remove-Item -Force package-lock.json
npm install
npm run dev
```

### Backend Won't Start

```powershell
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill the process if needed (replace PID with actual number)
taskkill /PID <PID> /F

# Restart backend
cd c:\Users\Aakash\Desktop\Huntify\backend
uvicorn app.main:app --reload
```

### Port Already in Use

**Change Backend Port:**
```powershell
uvicorn app.main:app --reload --port 8001
```

**Change Frontend Port:**
Edit `frontend/vite.config.ts` and add:
```typescript
export default defineConfig({
  server: {
    port: 3000
  }
})
```

---

## 📊 Using the Frontend

### 1. Start Auto-Apply from Web UI

1. Open http://localhost:5173
2. Click **"Start Auto-Apply"** button
3. Set options:
   - Max jobs: 10
   - Min score: 0.60
   - Sources: Select job boards
4. Click **"Start"**
5. Watch applications in real-time!

### 2. View Application Queue

1. Navigate to **"Queue"** tab
2. See pending applications
3. Approve/reject manually if needed

### 3. Check Application History

1. Navigate to **"Applications"** tab
2. View all submitted applications
3. See status (submitted, failed, pending)

---

## 🎮 Frontend vs CLI

### Use Frontend When:
- ✅ You want a visual dashboard
- ✅ You want to monitor progress in real-time
- ✅ You want to manually review before submitting
- ✅ You want to see statistics and charts

### Use CLI When:
- ✅ You want fully automated operation
- ✅ You want to run in background
- ✅ You want to schedule with cron/task scheduler
- ✅ You want to see detailed logs

---

## 🔄 Both Methods Work Together

You can use BOTH at the same time:

1. **Frontend:** Monitor and control
2. **CLI:** Run automation in background
3. **API:** Serves both frontend and CLI

---

## 📝 Complete Example Session

```powershell
# Terminal 1: Start Backend
cd c:\Users\Aakash\Desktop\Huntify\backend
uvicorn app.main:app --reload

# Terminal 2: Start Frontend
cd c:\Users\Aakash\Desktop\Huntify\frontend
npm run dev

# Terminal 3 (Optional): Run CLI automation
cd c:\Users\Aakash\Desktop\Huntify\backend
python run_auto_apply.py --max-jobs 5
```

Now you have:
- ✅ Backend API running
- ✅ Frontend dashboard running
- ✅ CLI automation running
- ✅ All working together!

---

## 🎯 Quick Reference

| Task | Command | URL |
|------|---------|-----|
| **Start Backend** | `uvicorn app.main:app --reload` | http://localhost:8000 |
| **Start Frontend** | `npm run dev` | http://localhost:5173 |
| **API Docs** | (automatic) | http://localhost:8000/docs |
| **Run CLI** | `python run_auto_apply.py` | N/A |

---

## 🚀 Fastest Start (2 Commands)

**Terminal 1:**
```powershell
cd c:\Users\Aakash\Desktop\Huntify\backend ; uvicorn app.main:app --reload
```

**Terminal 2:**
```powershell
cd c:\Users\Aakash\Desktop\Huntify\frontend ; npm run dev
```

**Then open:** http://localhost:5173

---

## 💡 Pro Tips

1. **Keep both terminals open** while using the frontend
2. **Backend must run first** before frontend can connect
3. **Use API docs** (http://localhost:8000/docs) to test endpoints
4. **Check browser console** (F12) for frontend errors
5. **Check terminal** for backend errors

---

**Enjoy your Huntify Dashboard! 🎉**
