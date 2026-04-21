# AutoMech Hosting Guide

## 🚀 Deploying AutoMech to Production

This guide covers hosting AutoMech on various platforms with proper LLM configuration.

---

## 🤖 LLM Configuration for Hosting

AutoMech supports two LLM modes:

### 1. **Local Ollama** (Development)
- Runs Llama 3 on your machine
- Requires 8GB+ RAM
- Free, no API costs
- Best for: Local development

### 2. **Groq API** (Production/Hosting) ⭐ **Recommended for Hosting**
- Cloud-based Llama 3.3 70B
- No local resources needed
- Free tier: 30 requests/minute
- Best for: Production hosting

---

## ⚙️ Environment Configuration

### For Hosting (Production)

Set this in your `.env` file:

```bash
# Use cloud API for hosting
PREFER_CLOUD_LLM=true

# Your Groq API key (required)
GROQ_API_KEY=your_actual_groq_api_key_here

# Database (use PostgreSQL for production)
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/automech

# JWT Secret (generate a secure random string)
JWT_SECRET_KEY=your-secure-random-32-character-secret-key-here
```

### For Local Development

```bash
# Try local Ollama first, fallback to Groq
PREFER_CLOUD_LLM=false

# Groq API key (fallback)
GROQ_API_KEY=your_groq_api_key_here

# Database (SQLite is fine for development)
DATABASE_URL=sqlite:///./automech.db

# JWT Secret
JWT_SECRET_KEY=dev-secret-key-change-in-production
```

---

## 🌐 Hosting Platforms

### Option 1: Railway.app (Easiest)

1. **Create account** at [railway.app](https://railway.app)

2. **Deploy from GitHub:**
   ```bash
   # Push your code to GitHub
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin your-github-repo-url
   git push -u origin main
   ```

3. **In Railway:**
   - Click "New Project" → "Deploy from GitHub"
   - Select your repository
   - Add environment variables:
     ```
     PREFER_CLOUD_LLM=true
     GROQ_API_KEY=your_key_here
     JWT_SECRET_KEY=your_secret_here
     ```

4. **Railway will auto-detect** Python and install dependencies

5. **Set start command:**
   ```bash
   cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

**Cost:** Free tier available, ~$5/month for production

---

### Option 2: Render.com

1. **Create account** at [render.com](https://render.com)

2. **Create Web Service:**
   - Connect GitHub repository
   - Environment: Python 3
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Add Environment Variables:**
   ```
   PREFER_CLOUD_LLM=true
   GROQ_API_KEY=your_key_here
   JWT_SECRET_KEY=your_secret_here
   ```

4. **Add PostgreSQL Database** (optional):
   - Create PostgreSQL instance in Render
   - Copy DATABASE_URL to environment variables

**Cost:** Free tier available (spins down after inactivity)

---

### Option 3: DigitalOcean App Platform

1. **Create account** at [digitalocean.com](https://digitalocean.com)

2. **Create App:**
   - Choose GitHub repository
   - Detect Python app
   - Set environment variables

3. **Configure:**
   ```yaml
   # app.yaml
   name: automech
   services:
   - name: backend
     environment_slug: python
     github:
       repo: your-username/automech
       branch: main
     run_command: cd backend && uvicorn main:app --host 0.0.0.0 --port 8080
     envs:
     - key: PREFER_CLOUD_LLM
       value: "true"
     - key: GROQ_API_KEY
       value: your_key_here
       type: SECRET
     - key: JWT_SECRET_KEY
       value: your_secret_here
       type: SECRET
   ```

**Cost:** $5/month minimum

---

### Option 4: AWS EC2 (Advanced)

1. **Launch EC2 instance** (t2.medium or larger)

2. **SSH into instance:**
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

3. **Install dependencies:**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx -y
   ```

4. **Clone and setup:**
   ```bash
   git clone your-repo-url
   cd automech
   python3 -m venv venv
   source venv/bin/activate
   pip install -r backend/requirements.txt
   ```

5. **Create `.env` file:**
   ```bash
   cd backend
   nano .env
   # Add your environment variables
   ```

6. **Run with systemd:**
   ```bash
   sudo nano /etc/systemd/system/automech.service
   ```
   
   ```ini
   [Unit]
   Description=AutoMech API
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/automech/backend
   Environment="PATH=/home/ubuntu/automech/venv/bin"
   ExecStart=/home/ubuntu/automech/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000

   [Install]
   WantedBy=multi-user.target
   ```

7. **Start service:**
   ```bash
   sudo systemctl start automech
   sudo systemctl enable automech
   ```

8. **Configure Nginx:**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

**Cost:** ~$10-20/month

---

### Option 5: Heroku

1. **Install Heroku CLI**

2. **Create Heroku app:**
   ```bash
   heroku create automech-app
   ```

3. **Add buildpack:**
   ```bash
   heroku buildpacks:set heroku/python
   ```

4. **Set environment variables:**
   ```bash
   heroku config:set PREFER_CLOUD_LLM=true
   heroku config:set GROQ_API_KEY=your_key_here
   heroku config:set JWT_SECRET_KEY=your_secret_here
   ```

5. **Create Procfile:**
   ```
   web: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

6. **Deploy:**
   ```bash
   git push heroku main
   ```

**Cost:** $7/month minimum (free tier discontinued)

---

## 🔑 Getting Groq API Key (Free)

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up with Google/GitHub
3. Navigate to "API Keys"
4. Click "Create API Key"
5. Copy the key (starts with `gsk_...`)
6. Add to your `.env` file

**Free Tier Limits:**
- 30 requests per minute
- 14,400 requests per day
- Llama 3.3 70B model included

---

## 📊 Database Options

### Development: SQLite (Default)
```bash
# No configuration needed
# Uses automech.db file
```

### Production: PostgreSQL (Recommended)

**Railway/Render:**
- Add PostgreSQL service
- Copy DATABASE_URL automatically

**Manual Setup:**
```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database
sudo -u postgres psql
CREATE DATABASE automech;
CREATE USER automech_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE automech TO automech_user;
\q

# Update .env
DATABASE_URL=postgresql+asyncpg://automech_user:your_password@localhost:5432/automech
```

---

## ✅ Deployment Checklist

Before deploying:

- [ ] Set `PREFER_CLOUD_LLM=true` in production `.env`
- [ ] Add valid `GROQ_API_KEY`
- [ ] Generate secure `JWT_SECRET_KEY` (32+ characters)
- [ ] Use PostgreSQL for production database
- [ ] Set up proper CORS origins in `main.py`
- [ ] Enable HTTPS (most platforms do this automatically)
- [ ] Test all endpoints after deployment
- [ ] Monitor Groq API usage
- [ ] Set up error logging
- [ ] Configure backup strategy for database

---

## 🧪 Testing Deployment

After deployment, test these endpoints:

```bash
# Health check
curl https://your-app.com/

# Chat endpoint
curl -X POST https://your-app.com/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "P0300 code", "user_id": "test"}'

# Should return diagnosis using Groq API
```

---

## 🐛 Troubleshooting

### "GROQ_API_KEY not configured"
- Check environment variables are set correctly
- Restart the application after setting env vars

### "Connection timeout"
- Groq API might be rate-limited
- Check your API key is valid
- Verify internet connectivity from server

### "Module not found"
- Ensure all dependencies are installed: `pip install -r backend/requirements.txt`
- Check Python version (3.9+ required)

### Ollama trying to connect when hosted
- Set `PREFER_CLOUD_LLM=true` to skip Ollama check
- This saves startup time on hosted platforms

---

## 💰 Cost Comparison

| Platform | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| **Groq API** | ✅ 30 req/min | N/A | LLM (always free) |
| **Railway** | ✅ $5 credit | $5-20/month | Easiest deployment |
| **Render** | ✅ Limited | $7+/month | Free tier testing |
| **DigitalOcean** | ❌ | $5+/month | Predictable pricing |
| **AWS EC2** | ✅ 1 year | $10+/month | Full control |
| **Heroku** | ❌ | $7+/month | Simple deployment |

**Recommended for Production:** Railway or Render with Groq API

---

## 🎯 Recommended Setup

**For most users:**
```
Platform: Railway.app
LLM: Groq API (free)
Database: Railway PostgreSQL
Total Cost: ~$5/month
```

**Configuration:**
```bash
PREFER_CLOUD_LLM=true
GROQ_API_KEY=your_groq_key
DATABASE_URL=postgresql://... (auto-provided by Railway)
JWT_SECRET_KEY=generate-secure-random-string
```

This setup:
- ✅ Always works (no Ollama dependency)
- ✅ Fast and reliable
- ✅ Easy to deploy
- ✅ Affordable
- ✅ Scales automatically

---

## 📞 Support

If you encounter issues:
1. Check logs in your hosting platform
2. Verify environment variables
3. Test Groq API key at [console.groq.com](https://console.groq.com)
4. Review this guide's troubleshooting section

---

**Ready to deploy? Start with Railway + Groq for the easiest experience! 🚀**
