# ⚡ Quick Deploy Reference

## 🎯 TL;DR - Deploy in 5 Minutes

### 1. Set Environment Variables
```bash
PREFER_CLOUD_LLM=true
GROQ_API_KEY=your_groq_key_here
JWT_SECRET_KEY=random-32-char-string
```

### 2. Deploy Command
```bash
cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 3. Done! ✅

---

## 🚀 Platform-Specific Quick Start

### Railway.app (Recommended)
1. Connect GitHub repo
2. Add env vars (above)
3. Deploy automatically
4. **Cost:** ~$5/month

### Render.com
1. New Web Service → GitHub
2. Build: `pip install -r backend/requirements.txt`
3. Start: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add env vars
5. **Cost:** Free tier available

### DigitalOcean
1. Create App → GitHub
2. Set env vars
3. Deploy
4. **Cost:** $5/month

---

## 🔑 Get Groq API Key (Free)
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up
3. Create API Key
4. Copy key (starts with `gsk_`)

---

## ✅ Pre-Deploy Test
```bash
python test_deployment.py
```

---

## 🧪 Post-Deploy Test
```bash
# Health check
curl https://your-app.com/

# Test chat
curl -X POST https://your-app.com/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "P0300 code", "user_id": "test"}'
```

---

## 📚 Full Documentation
- **[HOSTING_GUIDE.md](HOSTING_GUIDE.md)** - Complete guide
- **[DEPLOYMENT_READY.md](DEPLOYMENT_READY.md)** - Overview
- **[CHANGES_SUMMARY.md](CHANGES_SUMMARY.md)** - What changed

---

## 💡 Key Settings

| Setting | Development | Production |
|---------|-------------|------------|
| `PREFER_CLOUD_LLM` | `false` | `true` |
| Database | SQLite | PostgreSQL |
| JWT Secret | Any | Secure random |

---

## 🆘 Common Issues

**"GROQ_API_KEY not configured"**
→ Add env var in hosting platform

**"Connection timeout"**
→ Check API key at console.groq.com

**Still trying Ollama**
→ Set `PREFER_CLOUD_LLM=true`

---

**That's it! Your AutoMech will work on any hosting platform! 🎉**
