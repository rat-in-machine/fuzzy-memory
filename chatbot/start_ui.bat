@echo off
echo.
echo ========================================
echo  🎮 Iniciando Streamlit UI (Puerto 8501)
echo ========================================
echo.
cd /d "%~dp0"
streamlit run ui/app.py --server.port 8501
    call venv\Scripts\activate.bat
)

REM Verificar si streamlit está instalado
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo ❌ Streamlit no está instalado
    echo 📦 Instala las dependencias con:
    echo    pip install streamlit
    echo.
    pause
    exit /b 1
)

echo ✅ Iniciando aplicación Streamlit...
echo 🌐 La interfaz se abrirá en http://localhost:8501
echo.
echo Presiona Ctrl+C para detener la aplicación
echo ========================================
echo.

REM Ejecutar streamlit
python -m streamlit run ui/app.py --logger.level=info

pause
