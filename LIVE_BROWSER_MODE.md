# 🌐 Live Browser Mode - Real-Time Job Applications

## What This Does

Instead of scraping, this mode:
1. **Opens the actual job board website** (Naukri, Indeed, etc.) in browser
2. **Searches for jobs** using your keywords
3. **Clicks on each job** one by one
4. **Applies in real-time** - fills forms and submits
5. **You watch it happen** live!

---

## 🚀 How to Use

### Option 1: Command Line (Simple)

```powershell
cd c:\Users\Aakash\Desktop\Huntify\backend
python run_live_browser.py --query "Python Developer" --sources Naukri --max 5
```

**What happens:**
- Browser opens
- Goes to Naukri.com
- Searches "Python Developer"
- Clicks on first 5 jobs
- Tries to apply to each
- You see everything!

---

### Option 2: With Multiple Sources

```powershell
python run_live_browser.py --query "Backend Engineer" --sources "Naukri,Indeed" --max 3
```

**What happens:**
- Opens Naukri → searches → applies to 3 jobs
- Then opens Indeed → searches → applies to 3 jobs
- Total 6 applications

---

### Option 3: Hidden Browser

```powershell
python run_live_browser.py --query "Python Developer" --headless --max 10
```

Runs in background (faster).

---

## 📊 Complete Examples

### Example 1: Apply to 5 Naukri jobs
```powershell
cd c:\Users\Aakash\Desktop\Huntify\backend
python run_live_browser.py --query "Python Developer" --sources Naukri --max 5
```

### Example 2: Apply to both Naukri and Indeed
```powershell
python run_live_browser.py --query "Backend Engineer" --sources "Naukri,Indeed" --max 3
```

### Example 3: Fast mode (hidden browser)
```powershell
python run_live_browser.py --query "Full Stack Developer" --sources Naukri --max 10 --headless
```

---

## 🎮 What You'll See

```
============================================================
HUNTIFY LIVE BROWSER APPLICATION
============================================================
Search Query: Python Developer
Sources: Naukri
Max per source: 5
Browser Mode: Visible
============================================================

⚠️ Browser will open and apply to jobs automatically. Continue? (yes/no): yes

============================================================
Processing source: Naukri
============================================================

Navigating to Naukri.com...
Searching for: Python Developer
Search results loaded
Found 25 job listings

============================================================
Processing job 1/5
============================================================
Job: Senior Python Developer at TechCorp
Found apply button: button:has-text('Apply')
  ✓ Filled name
  ✓ Filled email
  ✓ Filled phone
  ✓ Clicked submit
✓ Applied to Senior Python Developer at TechCorp

============================================================
Processing job 2/5
============================================================
Job: Backend Engineer at StartupXYZ
○ No apply button found

... continues for all jobs ...

============================================================
SESSION COMPLETE
============================================================
Total applications attempted: 5
Total applications successful: 3
============================================================
```

---

## ⚙️ Options

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--query` | Job search keywords | "Python Backend Developer" | `--query "React Developer"` |
| `--sources` | Job boards to use | "Naukri" | `--sources "Naukri,Indeed"` |
| `--max` | Max jobs per source | 5 | `--max 10` |
| `--headless` | Hide browser | False (visible) | `--headless` |

---

## 🎯 Use Cases

### When to Use Live Browser Mode

✅ **Best for:**
- When job boards block scraping
- When you want to see what's happening
- When you want maximum success rate
- When sites require interaction

❌ **Not ideal for:**
- Very large number of applications (slow)
- Running in background without supervision
- Sites that require login first

---

## 📝 Step-by-Step What Happens

### Naukri.com Flow

1. **Open Naukri.com**
   ```
   Browser → naukri.com homepage
   ```

2. **Search for jobs**
   ```
   Type "Python Developer" in search box
   Click "Search" button
   Wait for results
   ```

3. **For each job:**
   ```
   Click on job card
   Look for "Apply" button
   If found:
     - Click "Apply"
     - Fill name field
     - Fill email field
     - Fill phone field
     - Click "Submit"
   If successful:
     - Mark as applied ✓
   If not:
     - Mark as skipped ○
   ```

4. **Move to next job**
   ```
   Wait 3 seconds
   Repeat step 3
   ```

5. **Complete**
   ```
   Show summary
   Close browser
   ```

---

## 🔧 Troubleshooting

### Browser doesn't open
```powershell
# Make sure Playwright is installed
playwright install chromium

# Check installation
playwright --version
```

### Can't find search box
- Naukri/Indeed might have changed their website
- Check browser manually to see current layout
- May need to update selectors in code

### Applications not submitting
- Some sites require login first
- Some have CAPTCHA
- Some have multi-step forms
- Watch the browser to see what's blocking

### Too slow
```powershell
# Use headless mode (faster)
python run_live_browser.py --headless

# Or reduce max applications
python run_live_browser.py --max 3
```

---

## 💡 Pro Tips

1. **Watch first run** - Don't use `--headless` initially, see what happens
2. **Start small** - Use `--max 3` first, then increase
3. **One source first** - Test with just Naukri before adding Indeed
4. **Check logs** - See `huntify_live_browser.log` for details
5. **Be patient** - Each application takes 5-10 seconds

---

## 🆚 Comparison

### Live Browser Mode vs Regular Mode

| Feature | Live Browser | Regular Mode |
|---------|-------------|--------------|
| **How it works** | Opens real browser | Scrapes + applies |
| **Speed** | Slower (human-like) | Faster |
| **Success rate** | Higher | Medium |
| **Blocks/CAPTCHAs** | Handle manually | May fail |
| **Visibility** | See everything | Background |
| **Best for** | 5-20 applications | 20+ applications |

---

## 🚀 Quick Start Commands

```powershell
# 1. Navigate to backend
cd c:\Users\Aakash\Desktop\Huntify\backend

# 2. Run live browser (VISIBLE - watch it work!)
python run_live_browser.py --query "Python Developer" --sources Naukri --max 5

# 3. For faster execution (hidden browser)
python run_live_browser.py --query "Python Developer" --sources Naukri --max 10 --headless
```

---

## ✅ This is EXACTLY what you asked for!

- ✅ Don't scrape
- ✅ Go to browser
- ✅ Use real browser
- ✅ Apply in real-time
- ✅ Watch it happen

**Try it now:**
```powershell
cd c:\Users\Aakash\Desktop\Huntify\backend
python run_live_browser.py --query "Python Developer" --sources Naukri --max 3
```

You'll see the browser open Naukri, search, and start applying! 🎉
