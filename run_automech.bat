@echo off
echo 🔧 Starting AutoMech AI...
start cmd /k "cd backend && python main.py"
start cmd /k "cd frontend && npm run dev"
echo ✅ Backend and Frontend should be starting in new windows.
echo 💬 Backend: http://localhost:8000
echo 🚗 Frontend: http://localhost:5173
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
