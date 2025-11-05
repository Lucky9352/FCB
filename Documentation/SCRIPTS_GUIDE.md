# 📜 Development Scripts Guide

## Overview

Three Windows batch scripts to streamline your daily development workflow:

1. **cleanup.bat** - Daily cleanup before starting work
2. **dev-start.bat** - Start local development server
3. **git-push.bat** - Push to GitHub with pre-checks

---

## 1️⃣ cleanup.bat

### Purpose
Run this **every day before starting development** to clean up build artifacts and cache files.

### What It Does
- ✅ Removes Python `__pycache__` directories
- ✅ Deletes `.pyc`, `.pyo` compiled files
- ✅ Removes `staticfiles/` build directory
- ✅ Cleans Node.js cache
- ✅ Deletes log files
- ✅ Removes temporary files

### Usage
```bash
cleanup.bat
```

### When to Run
- **Every morning** before starting development
- After pulling new changes from git
- When you notice stale cache issues
- Before running tests

### Output
```
========================================
 TapNex Arena - Daily Cleanup
========================================

[1/6] Cleaning Python cache files...
    ✓ Python cache cleaned
[2/6] Cleaning build artifacts...
    ✓ staticfiles removed
...
========================================
 Cleanup Complete!
========================================
```

---

## 2️⃣ dev-start.bat

### Purpose
Start the local development server with all necessary services and checks.

### What It Does
1. ✅ Activates virtual environment
2. ✅ Checks for .env file
3. ✅ Installs/updates Python dependencies
4. ✅ Checks Node dependencies
5. ✅ Builds Tailwind CSS
6. ✅ Runs database migrations
7. ✅ Collects static files
8. ✅ Starts Django development server

### Usage
```bash
dev-start.bat
```

### Prerequisites
- Virtual environment created: `python -m venv venv`
- `.env` file exists (copy from `.env.example`)
- Node.js installed

### Access
Once running, access at: **http://localhost:8000**

### Stop Server
Press **Ctrl+C**

### Output
```
========================================
 TapNex Arena - Development Server
========================================

[1/7] Activating virtual environment...
    ✓ Virtual environment activated
[2/7] Checking Python dependencies...
    ✓ Dependencies installed
...
========================================
 Server is starting...
 Access at: http://localhost:8000
========================================
```

---

## 3️⃣ git-push.bat

### Purpose
Push code to GitHub with comprehensive pre-push checks to ensure deployment-ready code.

### What It Does

#### Pre-Push Checks (Automatic)
1. ✅ Checks for pending migrations
2. ✅ Creates migrations if needed
3. ✅ Tests migrations work
4. ✅ Freezes requirements.txt
5. ✅ Builds production CSS
6. ✅ Tests static files collection
7. ✅ Checks for Python syntax errors

#### Git Operations
1. ✅ Stages all changes (`git add .`)
2. ✅ Commits with message (default: "IC" or custom)
3. ✅ Pushes to GitHub (`git push`)

### Usage

#### Default commit message (IC):
```bash
git-push.bat
[Press Enter when prompted]
```

#### Custom commit message:
```bash
git-push.bat
Enter commit message: Fixed booking bug
```

### When to Run
- After completing a feature
- After fixing bugs
- Before end of day
- When ready to deploy to Vercel

### Output
```
========================================
 TapNex Arena - Git Push
========================================

[Pre-Push Checks]

[1/6] Checking for pending migrations...
    ✓ No pending migrations
[2/6] Testing migrations...
    ✓ Migrations successful
[3/6] Updating requirements.txt...
    ✓ requirements.txt updated
[4/6] Building production CSS...
    ✓ CSS built successfully
[5/6] Testing static files collection...
    ✓ Static files OK
[6/6] Checking for Python syntax errors...
    ✓ No syntax errors

========================================
 All pre-push checks passed!
========================================

[Git Operations]

Enter commit message (or press Enter for 'IC'): 
[1/3] Staging changes...
    ✓ Changes staged
[2/3] Committing changes...
    ✓ Changes committed
[3/3] Pushing to GitHub...
    ✓ Pushed to GitHub

========================================
 Successfully pushed to GitHub!
========================================

Commit: IC
Branch: main

Your code is now on GitHub and will be deployed to Vercel.
```

### What Happens After Push
1. **GitHub** receives your code
2. **Vercel** detects the push
3. **Automatic deployment** starts
4. **Live site** updates (if checks pass)

---

## 🔄 Typical Daily Workflow

### Morning Routine
```bash
# 1. Clean up from yesterday
cleanup.bat

# 2. Pull latest changes
git pull

# 3. Start development server
dev-start.bat
```

### During Development
- Make code changes
- Test locally at http://localhost:8000
- Restart server if needed (Ctrl+C, then dev-start.bat)

### End of Day / Ready to Deploy
```bash
# Push to GitHub (automatic checks + deployment)
git-push.bat
```

---

## 🚨 Troubleshooting

### cleanup.bat Issues

**Error: "Access denied"**
- Close all running Python processes
- Close VS Code terminal if file is locked
- Run as administrator if needed

### dev-start.bat Issues

**Error: "Virtual environment not found"**
```bash
python -m venv venv
```

**Error: ".env file not found"**
```bash
copy .env.example .env
# Edit .env with your values
```

**Error: "Port already in use"**
- Another server is running on port 8000
- Kill the process or use different port:
```bash
python manage.py runserver 8001
```

### git-push.bat Issues

**Error: "Not a git repository"**
```bash
git init
git remote add origin <your-repo-url>
```

**Error: "Migrations failed"**
- Check database connection in .env
- Ensure DATABASE_URL is correct
- Try manually: `python manage.py migrate`

**Error: "Git push failed"**
- First push: `git push -u origin main`
- Check internet connection
- Verify GitHub credentials
- Check if remote branch exists

**Error: "CSS build failed"**
- Check if Node.js is installed
- Run: `npm install`
- Manually test: `npm run build-css-prod`

---

## 📊 What Each Script Affects

### cleanup.bat
- **Deletes:** Cache files, build artifacts
- **Preserves:** Source code, .env, database
- **Safe:** Yes, can run anytime

### dev-start.bat
- **Creates:** staticfiles/, migrations
- **Modifies:** Database (runs migrations)
- **Preserves:** Source code, .env
- **Safe:** Yes, for development only

### git-push.bat
- **Creates:** requirements.txt, migrations, commits
- **Modifies:** Git history, GitHub repository
- **Triggers:** Vercel deployment
- **Safe:** Yes, but pushes to production

---

## 🎯 Best Practices

### DO ✅
- Run cleanup.bat every morning
- Use dev-start.bat to start server
- Use git-push.bat for all pushes
- Test locally before pushing
- Use descriptive commit messages

### DON'T ❌
- Don't push without testing locally
- Don't skip cleanup.bat for weeks
- Don't commit sensitive data
- Don't force push (git push -f)
- Don't ignore error messages

---

## 🔐 Security Notes

### These scripts DO NOT:
- ❌ Commit .env file (it's in .gitignore)
- ❌ Commit venv/ or node_modules/
- ❌ Commit sensitive files
- ❌ Expose secrets

### Always Verify:
```bash
# Check what will be committed
git status

# Check if sensitive file is tracked
git check-ignore -v .env
# Should output: .gitignore:40:.env	.env
```

---

## 📝 Script Locations

```
FGC/
├── cleanup.bat           # Daily cleanup
├── dev-start.bat         # Start server
├── git-push.bat          # Push to GitHub
└── SCRIPTS_GUIDE.md      # This file
```

---

## 🆘 Need Help?

### Check Status
```bash
# Git status
git status

# Django check
python manage.py check

# Test migrations
python manage.py migrate --plan
```

### Manual Operations

#### If scripts fail, run manually:

**Cleanup:**
```bash
rd /s /q staticfiles
del /s /q *.pyc
```

**Start Server:**
```bash
venv\Scripts\activate
python manage.py runserver
```

**Push to Git:**
```bash
python manage.py makemigrations
python manage.py migrate
pip freeze > requirements.txt
git add .
git commit -m "Update"
git push
```

---

## 🎉 Quick Reference

| Task | Command | When |
|------|---------|------|
| Daily cleanup | `cleanup.bat` | Every morning |
| Start development | `dev-start.bat` | When coding |
| Push to GitHub | `git-push.bat` | Deploy ready |
| Manual push | `git add . && git commit -m "msg" && git push` | Emergency |
| Stop server | `Ctrl+C` | In terminal |

---

**Happy Coding! 🚀**

*TapNex Arena Development Team*
