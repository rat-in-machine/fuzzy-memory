@echo off
echo.
echo ============================================
echo  🎮 Iniciando Chatbot - Todos los Servicios
echo ============================================
echo.

cd /d "%~dp0"

echo [1/2] 🚀 Iniciando Backend FastAPI (puerto 8000)...
start "FastAPI Backend" cmd /k "python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 5 /nobreak >nul

echo [2/2] 🎨 Iniciando UI Streamlit (puerto 8501)...
start "Streamlit UI" cmd /k "streamlit run ui/app.py --server.port 8501"

echo.
echo ✅ Servicios iniciados correctamente
echo.
echo 📍 Backend API: http://localhost:8000
echo 📍 Streamlit UI: http://localhost:8501
echo 📍 API Docs: http://localhost:8000/docs
echo.
echo Presiona cualquier tecla para salir (los servicios seguirán corriendo)...
pause >nul
