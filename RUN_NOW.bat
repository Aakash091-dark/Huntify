@echo off
echo ============================================
echo Huntify - Auto Apply to Jobs  
echo ============================================
echo.
echo This will open a browser and start applying
echo to jobs automatically.
echo.
pause

cd backend
python run_simple_apply.py --query "Python Developer" --max 3

pause
