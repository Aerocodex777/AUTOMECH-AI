# AutoMech AI — Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Step 1: Get Your Groq API Key (Free)
1. Go to https://console.groq.com/keys
2. Sign up (free account)
3. Create a new API key
4. Copy the key (starts with `gsk_...`)

### Step 2: Configure the Key
Open `backend/.env` and replace:
```
GROQ_API_KEY=your_groq_api_key_here
```
with:
```
GROQ_API_KEY=gsk_your_actual_key_here
```

### Step 3: Install Backend
```bash
cd backend
pip install -r requirements.txt
```

Wait for installation (2-3 minutes). This installs:
- LangChain + Groq integration
- ChromaDB for vector storage
- FastAPI for the API server
- SQLAlchemy for database

### Step 4: Install Frontend
```bash
cd ../frontend
npm install
```

Wait for installation (1-2 minutes).

### Step 5: Run the App

**Windows**: Double-click `run_automech.bat`

**Mac/Linux**:
```bash
# Terminal 1
cd backend
python main.py

# Terminal 2 (new terminal)
cd frontend
npm run dev
```

### Step 6: Open the App
Open your browser to: http://localhost:5173

You should see:
- ✅ Green status dot (backend connected)
- 🔧 AutoMech AI header
- Two tabs: Diagnose and Vehicles

## 🧪 Test It Out

### Test 1: Add a Vehicle
1. Click "Vehicles" tab
2. Click "+ Add Vehicle"
3. Fill in:
   - Customer Name: "Test User"
   - Make: "Maruti Suzuki"
   - Model: "Swift"
   - Year: 2019
   - Mileage: 45000
   - Fuel: "Petrol"
4. Click "✅ Save Vehicle"
5. Click the vehicle card to select it

### Test 2: Diagnose with OBD Code
1. Click "Diagnose" tab
2. Type "P0301" in the OBD input field
3. Type "engine makes clicking sound when cold" in the message box
4. Click send (or press Enter)
5. Wait 3-5 seconds for AI response

You should see:
- 🔍 Diagnosis: Cylinder 1 Misfire Detected
- 📋 Causes: Faulty spark plug, bad ignition coil
- 🛠️ Fix: Replace spark plug on cylinder 1
- 💰 Cost: ₹800 – ₹2,200 (Kerala market)

### Test 3: Voice Input (Chrome/Edge only)
1. Click the microphone button 🎤
2. Allow microphone access
3. Say: "check engine light is on"
4. Text appears in input box
5. Click send

## ✅ Success Indicators

### Backend Running Correctly
Terminal shows:
```
✅ Database ready (SQLite)
ℹ️  No PDFs found in data/manuals/ — RAG will use LLM knowledge only.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Frontend Running Correctly
Terminal shows:
```
VITE v5.3.4  ready in 500 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

### App Working Correctly
- Green status dot in header
- No console errors (F12 → Console)
- Can create vehicles
- Can send messages
- AI responds with structured diagnosis

## 🐛 Troubleshooting

### "Cannot connect to backend"
**Problem**: Frontend can't reach backend
**Solution**: 
1. Check backend terminal is running
2. Visit http://localhost:8000/ — should show `{"status": "AutoMech AI is running 🔧"}`
3. If not, restart backend: `cd backend && python main.py`

### "API Key Error"
**Problem**: Invalid or missing Groq API key
**Solution**:
1. Check `backend/.env` has your actual key
2. Key should start with `gsk_`
3. Get new key from https://console.groq.com/keys
4. Restart backend after updating .env

### "Module not found" errors
**Problem**: Dependencies not installed
**Solution**:
```bash
cd backend
pip install -r requirements.txt

cd ../frontend
npm install
```

### Voice input not working
**Problem**: Browser doesn't support Web Speech API
**Solution**: Use Chrome or Edge browser (Firefox/Safari don't support it)

### Slow first response
**Problem**: First diagnosis takes 10-15 seconds
**Solution**: This is normal — model is initializing. Subsequent responses are faster (3-5 seconds).

## 📚 Next Steps

### Add Vehicle Manuals (Optional)
1. Get PDF service manuals for Kerala vehicles
2. Place in `backend/data/manuals/`
3. Name them: `Maruti_Swift_2019.pdf`
4. Restart backend
5. RAG tool will now search manuals

### Use PostgreSQL (Optional)
1. Install PostgreSQL
2. Create database: `CREATE DATABASE automech;`
3. Update `backend/.env`:
   ```
   DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/automech
   ```
4. Restart backend

### Deploy to Production
See `DEPLOYMENT.md` for full guide.

## 🎯 What You Can Do Now

✅ Add vehicles for customers
✅ Diagnose issues with OBD codes
✅ Get AI-powered repair recommendations
✅ Estimate parts costs in INR (Kerala market)
✅ Use voice input for hands-free operation
✅ Track diagnostic history per vehicle
✅ Get safety warnings for critical systems

## 📖 Full Documentation

- `SETUP.md` — Detailed setup instructions
- `TESTING_CHECKLIST.md` — Complete test suite
- `DEPLOYMENT.md` — Production deployment
- `IMPLEMENTATION_SUMMARY.md` — Technical details

## 💬 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review `SETUP.md` for detailed instructions
3. Check backend terminal for error messages
4. Check browser console (F12) for frontend errors

---

**Ready to diagnose!** 🔧⚡

Open http://localhost:5173 and start helping Kerala mechanics fix vehicles faster.
