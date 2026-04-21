# 🚀 AutoMech AI - Local Setup Guide

## Run This Project on Any Computer

Follow these steps to run AutoMech AI on a new system.

---

## 📋 Prerequisites

### Required Software:
1. **Python 3.10+** - [Download](https://www.python.org/downloads/)
2. **Node.js 18+** - [Download](https://nodejs.org/)
3. **Git** - [Download](https://git-scm.com/)

### Optional (for better performance):
4. **Ollama** - [Download](https://ollama.ai/) (for local AI)

---

## 🔧 Step-by-Step Setup

### Step 1: Clone the Repository

```bash
# Clone from GitHub (or copy the folder)
git clone https://github.com/yourusername/automech-ai.git
cd automech-ai

# OR if you have the folder, just navigate to it
cd path/to/automech-ai
```

---

### Step 2: Backend Setup

```bash
# Navigate to backend folder
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Create .env file
# Copy the example below or use the existing .env
```

**Create `backend/.env` file:**
```env
# Required: Groq API Key (get from https://console.groq.com)
GROQ_API_KEY=your_groq_api_key_here

# Optional: OpenAI API Key (for vision fallback)
OPENAI_API_KEY=your_openai_api_key_here

# Database (SQLite by default, no setup needed)
DATABASE_URL=sqlite+aiosqlite:///./automech.db

# Security (generate random string)
SECRET_KEY=your-secret-key-here-change-this-in-production

# JWT Settings
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Start the backend:**
```bash
# Make sure you're in the backend folder
python main.py

# You should see:
# ✅ Database ready (SQLite)
# INFO: Uvicorn running on http://0.0.0.0:8000
```

**Keep this terminal open!**

---

### Step 3: Frontend Setup

**Open a NEW terminal** (keep backend running)

```bash
# Navigate to frontend folder
cd frontend

# Install Node.js dependencies
npm install

# Start the frontend
npm run dev

# You should see:
# VITE ready in XXX ms
# ➜ Local: http://localhost:5173/
```

**Keep this terminal open too!**

---

### Step 4: Access the Application

Open your browser and go to:
```
http://localhost:5173
```

You should see the AutoMech AI interface! 🎉

---

## 🔑 Getting API Keys

### Groq API Key (Required)
1. Go to https://console.groq.com
2. Sign up / Log in
3. Go to "API Keys"
4. Create new key
5. Copy and paste into `backend/.env`

### OpenAI API Key (Optional - for better image analysis)
1. Go to https://platform.openai.com
2. Sign up / Log in
3. Go to "API Keys"
4. Create new key
5. Copy and paste into `backend/.env`

---

## 🐛 Troubleshooting

### Problem: "Module not found" errors

**Solution:**
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

---

### Problem: "Port already in use"

**Solution:**
```bash
# Find and kill the process using the port

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:8000 | xargs kill -9
```

---

### Problem: "GROQ_API_KEY not found"

**Solution:**
1. Make sure `backend/.env` file exists
2. Check that GROQ_API_KEY is set
3. Restart the backend server

---

### Problem: "Database error"

**Solution:**
```bash
# Delete the database and let it recreate
cd backend
rm automech.db
python main.py
```

---

### Problem: Frontend can't connect to backend

**Solution:**
Check `frontend/src/components/Chat.jsx`:
```javascript
const API = 'http://localhost:8000'  // Make sure this is correct
```

---

## 📦 What Gets Installed

### Backend Dependencies (~500MB):
- FastAPI - Web framework
- LangChain - AI agent framework
- Groq/OpenAI - LLM APIs
- SQLAlchemy - Database
- BeautifulSoup - Web scraping
- And more...

### Frontend Dependencies (~300MB):
- React - UI framework
- Vite - Build tool
- Axios - HTTP client
- And more...

---

## 🎯 Quick Start Commands

**For someone who just got your code:**

```bash
# 1. Install Python dependencies
cd backend
pip install -r requirements.txt

# 2. Create .env file with your Groq API key
echo "GROQ_API_KEY=your_key_here" > .env

# 3. Start backend (in one terminal)
python main.py

# 4. Install Node dependencies (in another terminal)
cd ../frontend
npm install

# 5. Start frontend
npm run dev

# 6. Open browser
# Go to http://localhost:5173
```

---

## 🔄 Updating the Project

If you make changes and want to share:

```bash
# 1. Commit changes
git add .
git commit -m "Your changes"
git push

# 2. On another computer, pull changes
git pull

# 3. Update dependencies if needed
cd backend && pip install -r requirements.txt
cd ../frontend && npm install

# 4. Restart both servers
```

---

## 📱 Running on Different Devices

### Same Network (e.g., phone on same WiFi)

**Find your computer's IP:**
```bash
# Windows
ipconfig
# Look for "IPv4 Address" (e.g., 192.168.1.100)

# Mac/Linux
ifconfig
# Look for "inet" (e.g., 192.168.1.100)
```

**Update frontend to use IP:**
```javascript
// frontend/src/components/Chat.jsx
const API = 'http://192.168.1.100:8000'  // Use your IP
```

**Access from phone:**
```
http://192.168.1.100:5173
```

---

## 🐳 Docker Setup (Advanced)

**Create `docker-compose.yml` in project root:**
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
    volumes:
      - ./backend:/app
  
  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    depends_on:
      - backend
```

**Run with Docker:**
```bash
docker-compose up
```

---

## 📝 System Requirements

### Minimum:
- **CPU**: 2 cores
- **RAM**: 4GB
- **Storage**: 2GB free space
- **OS**: Windows 10+, macOS 10.15+, Linux

### Recommended:
- **CPU**: 4+ cores
- **RAM**: 8GB+
- **Storage**: 5GB free space
- **Internet**: Stable connection (for API calls)

---

## 🎓 For Your Demo Team

**Share this with your team:**

1. **Clone the repo** or copy the folder
2. **Install Python 3.10+** and **Node.js 18+**
3. **Get Groq API key** from https://console.groq.com
4. **Run setup commands** (see Quick Start above)
5. **Test it works** - open http://localhost:5173

**That's it!** 🚀

---

## 🆘 Need Help?

**Common issues and solutions:**

1. **Python not found**: Install Python and add to PATH
2. **npm not found**: Install Node.js
3. **Port in use**: Change port or kill existing process
4. **API key error**: Check .env file exists and has correct key
5. **Dependencies fail**: Try `pip install --upgrade pip` first

---

## 📞 Support

If you encounter issues:
1. Check the error message carefully
2. Look in this troubleshooting guide
3. Check `backend/main.py` logs
4. Check browser console (F12)
5. Ask your team member who set it up first

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:5173
- [ ] Can register a new user
- [ ] Can login
- [ ] Can create vehicle profile
- [ ] Can ask diagnostic questions
- [ ] Can upload images
- [ ] Can see parts recommendations
- [ ] Malayalam input works
- [ ] Conversation memory works

If all checked, you're good to go! 🎉
