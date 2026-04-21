# ⚡ AutoMech AI - 5-Minute Setup

## Prerequisites
- Python 3.10+
- Node.js 18+
- Groq API Key (free from https://console.groq.com)

---

## 🚀 Setup Commands

### 1. Backend Setup (Terminal 1)
```bash
cd backend
pip install -r requirements.txt
echo "GROQ_API_KEY=your_key_here" > .env
python main.py
```

### 2. Frontend Setup (Terminal 2)
```bash
cd frontend
npm install
npm run dev
```

### 3. Open Browser
```
http://localhost:5173
```

---

## 🔑 Get Groq API Key
1. Go to https://console.groq.com
2. Sign up (free)
3. Create API key
4. Copy to `backend/.env`

---

## ✅ That's It!
Your AutoMech AI is running locally! 🎉

**Troubleshooting?** See `LOCAL_SETUP_GUIDE.md`
