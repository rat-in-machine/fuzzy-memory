@echo off
cd /d "c:\Users\isma1\Desktop\Viewnext\Proyecto Hackaton\chatbot"
python -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000
