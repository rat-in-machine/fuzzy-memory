@echo off
echo.
echo ========================================
echo  🚀 Iniciando FastAPI Backend (Puerto 8000)
echo ========================================
echo.
cd /d "%~dp0"
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
