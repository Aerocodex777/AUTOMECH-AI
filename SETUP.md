# AutoMech AI — Setup Guide

## Prerequisites

1. **Python 3.9+** installed
2. **Node.js 18+** and npm installed
3. **Groq API Key** (free at https://console.groq.com/keys)
4. **PostgreSQL** (optional - SQLite fallback available)

## Quick Start

### 1. Configure API Key

Edit `backend/.env` and add your Groq API key:
```
GROQ_API_KEY=gsk_your_actual_key_here
```

### 2. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 4. Run the Application

**Option A: Use the batch script (Windows)**
```bash
run_automech.bat
```

**Option B: Manual start**

Terminal 1 (Backend):
```bash
cd backend
python main.py
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

### 5. Access the App

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Database Setup

### SQLite (Default - No Setup Required)
The app will automatically use SQLite (`automech.db`) if PostgreSQL is not configured.

### PostgreSQL (Optional)
If you want to use PostgreSQL:

1. Install PostgreSQL
2. Create database:
```sql
CREATE DATABASE automech;
```
3. Update `backend/.env`:
```
DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/automech
```

## Adding Vehicle Manuals (Optional)

1. Place PDF service manuals in `backend/data/manuals/`
2. Name them descriptively (e.g., `Maruti_Swift_2019.pdf`)
3. Restart the backend - manuals will be auto-indexed

## Testing the System

### Test 1: Health Check
```bash
curl http://localhost:8000/
```
Expected: `{"status": "AutoMech AI is running 🔧", "version": "1.0.0"}`

### Test 2: OBD Code Lookup
```bash
curl -X POST http://localhost:8000/diagnose/ \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "engine clicking", "obd_code": "P0301"}'
```

### Test 3: Create Vehicle
```bash
curl -X POST http://localhost:8000/vehicles/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Customer", "make": "Maruti Suzuki", "model": "Swift", "year": 2019, "mileage": 45000, "fuel_type": "Petrol"}'
```

## Features Checklist

✅ ReAct agent with 3 specialized tools
✅ OBD code lookup (28+ codes)
✅ RAG over vehicle manuals
✅ Parts cost estimator (Kerala market, INR)
✅ Voice input (Web Speech API)
✅ Vehicle profile management
✅ Diagnostic history tracking
✅ Safety warnings for critical systems
✅ PWA support with offline capability
✅ SQLite fallback (no PostgreSQL required)

## Troubleshooting

### "Cannot connect to backend"
- Ensure backend is running on port 8000
- Check `backend/.env` has valid GROQ_API_KEY

### "API Key Error"
- Get a free key from https://console.groq.com/keys
- Update `backend/.env` with your key

### "Voice input not working"
- Use Chrome or Edge browser
- Allow microphone permissions

### "No manuals found"
- This is normal if no PDFs are in `backend/data/manuals/`
- Agent will use LLM knowledge instead

## Architecture

```
User → Voice/Text Input → FastAPI → ReAct Agent → Tools:
                                                    ├─ OBD Lookup
                                                    ├─ RAG (Manuals)
                                                    └─ Parts Estimator
                                                    
                                    → PostgreSQL/SQLite (Vehicles + History)
```

## Tech Stack

- LLM: Groq API (llama-3.3-70b-versatile)
- Embeddings: sentence-transformers (all-MiniLM-L6-v2)
- Vector DB: ChromaDB
- Backend: FastAPI + SQLAlchemy async
- Frontend: React 18 + Vite + PWA
- Voice: Web Speech API

## Next Steps

1. Add real vehicle PDF manuals to `backend/data/manuals/`
2. Test with real OBD codes from Kerala vehicles
3. Customize parts pricing for your local market
4. Deploy to production (Render, Railway, or VPS)

---

Built for Kerala mechanics 🔧 Powered by Groq AI ⚡
