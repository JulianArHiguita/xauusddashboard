@echo off
echo Starting XAUUSD Dashboard...

echo Starting Backend...
cd backend
start cmd /k "venv\Scripts\uvicorn main:app --reload"
cd ..

echo Starting Frontend...
cd frontend
set PATH=%PATH%;C:\Program Files\Microsoft Visual Studio\2022\Community\MSBuild\Microsoft\VisualStudio\NodeJs
start cmd /k "npm run dev"
cd ..

echo Dashboard launched! Access it at the URL shown in the frontend terminal (usually http://localhost:5173)
