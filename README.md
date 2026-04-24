# AutoMech AI 🔧

**AI-Powered Automotive Diagnostic Assistant for Kerala, India**

Fast, voice-enabled diagnostic tool that consolidates fragmented vehicle repair knowledge into one intelligent system. Built specifically for automobile mechanics in Kerala.

Live now : http://automech-ai-frontend.onrender.com

![Status](https://img.shields.io/badge/status-production%20ready-brightgreen)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Node](https://img.shields.io/badge/node-18%2B-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## ✨ Features

- 🤖 **AI Diagnostic Agent** — Groq-powered ReAct agent with specialized tools
- 🔍 **OBD Code Lookup** — 28+ diagnostic trouble codes with detailed fixes
- 📚 **RAG over Manuals** — Semantic search through vehicle service manuals
- 💰 **Parts Estimator** — Kerala market pricing in INR (OEM + aftermarket)
- 🎤 **Voice Input** — Hands-free operation for mechanics with dirty hands
- 🚗 **Vehicle Profiles** — Save customer vehicles for context-aware diagnostics
- ⚠️ **Safety Warnings** — Mandatory alerts for brakes/steering/fuel/airbag
- 📱 **PWA Support** — Installable on mobile, works offline
- 🌙 **Dark Theme** — Industrial-futuristic design optimized for workshops

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Groq API key (free from [console.groq.com](https://console.groq.com/keys))

### Local Development

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd automech-agent
```

2. **Configure API key**
```bash
# Edit backend/.env
GROQ_API_KEY=gsk_your_actual_key_here
PREFER_CLOUD_LLM=false  # Try local Ollama first, fallback to Groq
```

3. **Install dependencies**
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

4. **Run the application**
```bash
# Windows: Double-click run_automech.bat

# Mac/Linux:
# Terminal 1: cd backend && python main.py
# Terminal 2: cd frontend && npm run dev
```

5. **Open the app**
```
http://localhost:5173
```

### 🌐 Hosting/Production

For deploying to Railway, Render, AWS, or other platforms:

```bash
# Set in production .env
PREFER_CLOUD_LLM=true  # Always use Groq API (no Ollama dependency)
GROQ_API_KEY=your_groq_key_here
```

**See [HOSTING_GUIDE.md](HOSTING_GUIDE.md) for complete deployment instructions.**

See [QUICKSTART.md](QUICKSTART.md) for detailed instructions.

## 📖 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** — Get running in 5 minutes
- **[SETUP.md](SETUP.md)** — Detailed installation guide
- **[HOSTING_GUIDE.md](HOSTING_GUIDE.md)** — Deploy to production (Railway, Render, AWS, etc.)
- **[TESTING_CHECKLIST.md](TESTING_CHECKLIST.md)** — Complete test suite
- **[DEPLOYMENT.md](DEPLOYMENT.md)** — Production deployment guide
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** — Technical details

## 🎯 Supported Vehicles (Kerala Market)

### Cars
Maruti Suzuki, Hyundai, Tata, Honda, Toyota, Mahindra, Kia, MG

### Two-Wheelers
Hero, Honda, Bajaj, TVS, Royal Enfield

## 🏗️ Architecture

```
User Input (Voice/Text)
    ↓
React Frontend (PWA)
    ↓
FastAPI Backend
    ↓
ReAct Agent (Groq llama-3.3-70b-versatile)
    ↓
Tools:
├─ OBD Lookup (28+ codes)
├─ RAG (ChromaDB + sentence-transformers)
└─ Parts Estimator (Kerala pricing)
    ↓
PostgreSQL/SQLite (Vehicles + History)
```

## 🛠️ Tech Stack

### Backend
- **LLM**: Groq API (llama-3.3-70b-versatile)
- **Framework**: FastAPI + Uvicorn
- **Agent**: LangChain ReAct
- **Vector DB**: ChromaDB
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Database**: PostgreSQL + SQLite fallback
- **PDF Parsing**: PyMuPDF

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **PWA**: vite-plugin-pwa
- **Voice**: Web Speech API
- **Styling**: Custom CSS (no libraries)
- **Fonts**: Google Fonts (Inter + Outfit)

## 🧪 Testing

```bash
# Health check
curl http://localhost:8000/

# Test diagnosis
curl -X POST http://localhost:8000/diagnose/ \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "engine clicking", "obd_code": "P0301"}'
```

See [TESTING_CHECKLIST.md](TESTING_CHECKLIST.md) for comprehensive tests.

## 📊 Project Status

### ✅ Implemented
- ReAct agent with 3 specialized tools
- OBD code lookup (28+ codes)
- RAG over vehicle manuals
- Parts cost estimator (Kerala market)
- Voice input (Web Speech API)
- Vehicle profile management
- Diagnostic history tracking
- Safety warnings
- PWA with offline support
- Responsive mobile design

### 🔮 Future (v2)
- Image upload for warning lights
- Vision model analysis
- Malayalam language support
- Evaluation dataset
- Fine-tuned model

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License — see LICENSE file for details

## 🙏 Acknowledgments

- Built for Kerala mechanics
- Powered by Groq AI
- Inspired by real workshop challenges

## 📧 Support

For issues or questions:
1. Check [QUICKSTART.md](QUICKSTART.md) troubleshooting
2. Review [SETUP.md](SETUP.md) for detailed setup
3. Open an issue on GitHub

---

**Made with ❤️ by sreehari for Kerala's automotive community**

🔧 Diagnose faster. Fix smarter. Drive safer.
