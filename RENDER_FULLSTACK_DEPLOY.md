# 🚀 Deploy AutoMech Full Stack on Render

Complete guide to deploy both frontend and backend together on Render.

---

## 🎯 What You'll Get

**Single URL for everything:**
- Frontend UI at: `https://your-app.onrender.com`
- Backend API at: `https://your-app.onrender.com/api/...`
- **Total Cost: $0/month** (free tier)

---

## 📋 Prerequisites

- ✅ GitHub account
- ✅ Render account (sign up at [render.com](https://render.com))
- ✅ Groq API key (get from [console.groq.com](https://console.groq.com))
- ✅ Your code pushed to GitHub

---

## 🚀 Deployment Steps

### Step 1: Create Web Service on Render

1. Go to [render.com](https://render.com) and log in
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account if not already connected
4. Select repository: `Aerocodex777/AUTOMECH-AI`

### Step 2: Configure Service

Fill in these settings:

| Setting | Value |
|---------|-------|
| **Name** | `automech-fullstack` (or any name you like) |
| **Region** | Singapore (closest to India) |
| **Branch** | `main` |
| **Root Directory** | Leave empty |
| **Runtime** | Python 3 |
| **Build Command** | `bash render-fullstack-build.sh` |
| **Start Command** | `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | Free |

### Step 3: Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

Add these 3 variables:

#### Variable 1:
```
Key:   PREFER_CLOUD_LLM
Value: true
```

#### Variable 2:
```
Key:   GROQ_API_KEY
Value: your_actual_groq_api_key_here
```

#### Variable 3:
```
Key:   JWT_SECRET_KEY
Value: automech-super-secret-key-change-this-in-production-min-32-characters-long
```

### Step 4: Deploy!

1. Click **"Create Web Service"**
2. Wait 5-10 minutes for build and deployment
3. Watch the logs for progress

---

## 📊 What Happens During Build

```
🚀 AutoMech Full Stack Build Starting...
📦 Step 1: Installing Backend Dependencies...
   ✅ Backend dependencies installed
📦 Step 2: Installing Frontend Dependencies...
   ✅ Frontend dependencies installed
🎨 Step 3: Building Frontend...
   ✅ Frontend built successfully
🔍 Step 4: Verifying Build...
   ✅ Frontend dist folder exists
✅ Full Stack Build Complete!
🚀 Ready to start server...
```

---

## ✅ Verify Deployment

### 1. Check Build Logs
- Should see "Build succeeded"
- Should see "Deploy live"

### 2. Test Your App
Open your Render URL (e.g., `https://automech-fullstack.onrender.com`)

You should see:
- ✅ AutoMech login page
- ✅ Can create account
- ✅ Can chat with AI
- ✅ Can add vehicles

### 3. Test API
```bash
curl https://your-app.onrender.com/
# Should return: {"message": "AutoMech AI Backend"}
```

---

## 🔧 How It Works

### Architecture:
```
User Browser
    ↓
https://your-app.onrender.com
    ↓
Render Server
    ├─ Frontend (React) → Served as static files
    └─ Backend (FastAPI) → API endpoints
```

### Request Routing:
- `/` → Frontend (index.html)
- `/assets/*` → Frontend static files (CSS, JS, images)
- `/api/*` → Backend API
- `/docs` → API documentation

---

## 🐛 Troubleshooting

### Build Fails: "npm not found"
**Solution:** Render should have Node.js. If not, the build script will install it automatically.

### Build Fails: "Dependency conflict"
**Solution:** Already fixed in latest commit. Make sure you're deploying from the latest `main` branch.

### Frontend Shows Blank Page
**Solution:** 
1. Check build logs - frontend should build successfully
2. Verify `frontend/dist` folder was created
3. Check browser console for errors

### API Returns 404
**Solution:**
1. Make sure you're using correct API endpoints (e.g., `/chat`, not `/api/chat`)
2. Check CORS settings in `backend/main.py`

### "GROQ_API_KEY not configured"
**Solution:**
1. Go to Render dashboard → Your service → Environment
2. Verify `GROQ_API_KEY` is set correctly
3. Click "Manual Deploy" → "Deploy latest commit"

---

## 🔄 Updating Your App

### Automatic Updates:
1. Push changes to GitHub `main` branch
2. Render automatically detects and redeploys
3. Wait 5-10 minutes

### Manual Redeploy:
1. Go to Render dashboard
2. Click your service
3. Click "Manual Deploy" → "Deploy latest commit"

---

## 💰 Cost

| Component | Free Tier | Paid Tier |
|-----------|-----------|-----------|
| **Render Web Service** | ✅ 750 hours/month | $7/month (always-on) |
| **Groq API** | ✅ 30 req/min | Free forever |
| **Total** | **$0/month** | $7/month |

**Free tier limitations:**
- Spins down after 15 min of inactivity
- Cold start: ~30 seconds to wake up
- 750 hours/month (enough for hobby projects)

---

## 🎯 Production Checklist

Before going live:

- [ ] Deployment successful
- [ ] Frontend loads correctly
- [ ] Can create account and login
- [ ] Chat works with AI responses
- [ ] Vehicle profiles work
- [ ] All features tested
- [ ] Custom domain configured (optional)
- [ ] SSL certificate active (automatic on Render)
- [ ] Error monitoring set up (optional)

---

## 🌐 Custom Domain (Optional)

### Add Your Domain:
1. Go to Render dashboard → Your service → Settings
2. Scroll to "Custom Domain"
3. Click "Add Custom Domain"
4. Enter your domain (e.g., `automech.yourdomain.com`)
5. Follow DNS configuration instructions
6. Wait for SSL certificate (automatic)

---

## 📞 Support

**Render Issues:**
- Docs: https://render.com/docs
- Status: https://status.render.com
- Support: https://render.com/support

**AutoMech Issues:**
- Check build logs in Render dashboard
- Review this guide
- Test locally first: `bash run_automech.bat`

---

## 🎉 Success!

Your AutoMech is now live at:
**https://your-app.onrender.com**

Share it with users and start diagnosing vehicles! 🚗🔧

---

**Questions?** Check the troubleshooting section or Render documentation.
