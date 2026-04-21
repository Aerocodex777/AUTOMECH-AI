# 🚀 Deploy AutoMech on Vercel (Frontend) + Render (Backend)

This guide shows you how to deploy AutoMech with:
- **Frontend on Vercel** (Free, Fast CDN)
- **Backend on Render** (Free tier available)

---

## 📋 Overview

**Why this setup?**
- Vercel is perfect for React frontends (fast, free, easy)
- Render provides free backend hosting with PostgreSQL
- Both have generous free tiers
- Total cost: **$0/month**

---

## Part 1: Deploy Backend on Render (5 minutes)

### Step 1: Sign up for Render
1. Go to [render.com](https://render.com)
2. Sign up with GitHub

### Step 2: Create Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub account
3. Select repository: `Aerocodex777/AUTOMECH-AI`
4. Configure:
   - **Name:** `automech-backend`
   - **Region:** Singapore (closest to India)
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** Free

### Step 3: Add Environment Variables
Click **"Environment"** and add:

```
PREFER_CLOUD_LLM=true
GROQ_API_KEY=your_actual_groq_api_key_here
JWT_SECRET_KEY=your_secure_random_32_char_string
```

**To generate a secure JWT secret:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 4: Deploy
1. Click **"Create Web Service"**
2. Wait 3-5 minutes for deployment
3. Copy your backend URL (e.g., `https://automech-backend.onrender.com`)

### Step 5: Test Backend
```bash
curl https://your-backend-url.onrender.com/
# Should return: {"message": "AutoMech AI Backend"}
```

---

## Part 2: Deploy Frontend on Vercel (3 minutes)

### Step 1: Sign up for Vercel
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub

### Step 2: Import Project
1. Click **"Add New..."** → **"Project"**
2. Import `Aerocodex777/AUTOMECH-AI`
3. Configure:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend` ⚠️ **IMPORTANT: Click "Edit" and set this!**
   - **Build Command:** `npm run build` (auto-detected)
   - **Output Directory:** `dist` (auto-detected)
   - **Install Command:** `npm install` (auto-detected)

### Step 3: Add Environment Variable
In **"Environment Variables"** section, add:

```
VITE_API_URL=https://your-backend-url.onrender.com
```

Replace with your actual Render backend URL from Part 1.

### Step 4: Deploy
1. Click **"Deploy"**
2. Wait 2-3 minutes
3. Your app will be live at `https://your-app.vercel.app`

---

## ✅ Verify Deployment

### Test Frontend
1. Open `https://your-app.vercel.app`
2. Should see AutoMech login page
3. Create account and test chat

### Test Backend Connection
1. Open browser console (F12)
2. Try sending a message
3. Check Network tab - should see requests to your Render backend

---

## 🔧 Optional: Add PostgreSQL Database

### On Render:
1. Click **"New +"** → **"PostgreSQL"**
2. Name: `automech-db`
3. Region: Same as backend
4. Instance: Free
5. Click **"Create Database"**
6. Copy the **Internal Database URL**
7. Go to your backend service → Environment
8. Add: `DATABASE_URL=<your-postgres-url>`
9. Redeploy backend

---

## 🌐 Custom Domain (Optional)

### For Vercel (Frontend):
1. Go to your project → Settings → Domains
2. Add your domain (e.g., `automech.yourdomain.com`)
3. Follow DNS configuration instructions

### For Render (Backend):
1. Go to your service → Settings
2. Add custom domain
3. Update `VITE_API_URL` in Vercel to use your custom backend domain

---

## 📊 Monitoring

### Render Dashboard:
- View logs: Service → Logs
- Monitor usage: Dashboard → Usage
- Check health: Service → Events

### Vercel Dashboard:
- View deployments: Project → Deployments
- Check analytics: Project → Analytics
- Monitor performance: Project → Speed Insights

---

## 🐛 Troubleshooting

### Frontend can't connect to backend
**Problem:** CORS errors in browser console

**Solution:** Check backend CORS settings in `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://your-app.vercel.app",  # Add your Vercel URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Backend shows "GROQ_API_KEY not configured"
**Solution:** 
1. Go to Render → Service → Environment
2. Verify `GROQ_API_KEY` is set correctly
3. Click "Manual Deploy" → "Deploy latest commit"

### Render backend spins down (cold starts)
**Problem:** Free tier spins down after 15 minutes of inactivity

**Solution:** 
- Accept 30-second cold start (normal for free tier)
- Or use a free uptime monitor (UptimeRobot) to ping every 14 minutes
- Or upgrade to paid tier ($7/month) for always-on

### Build fails on Vercel
**Problem:** "Module not found" errors

**Solution:**
1. Check `frontend/package.json` has all dependencies
2. Verify Root Directory is set to `frontend`
3. Check build logs for specific error

---

## 💰 Cost Breakdown

| Service | Free Tier | Paid Tier |
|---------|-----------|-----------|
| **Vercel (Frontend)** | ✅ Unlimited | $20/month (Pro) |
| **Render (Backend)** | ✅ 750 hours/month | $7/month (always-on) |
| **Render (PostgreSQL)** | ✅ 90 days free | $7/month |
| **Groq API (LLM)** | ✅ 30 req/min | Free forever |
| **Total** | **$0/month** | $14-27/month |

---

## 🎯 Production Checklist

Before going live:

- [ ] Backend deployed on Render
- [ ] Frontend deployed on Vercel
- [ ] Environment variables set correctly
- [ ] Backend URL updated in Vercel
- [ ] CORS configured for Vercel domain
- [ ] Database connected (optional)
- [ ] Custom domain configured (optional)
- [ ] Test all features (chat, vehicles, auth)
- [ ] Monitor logs for errors
- [ ] Set up error tracking (optional: Sentry)

---

## 🔄 Updating Your App

### Update Backend:
1. Push changes to GitHub
2. Render auto-deploys from `main` branch
3. Or click "Manual Deploy" in Render dashboard

### Update Frontend:
1. Push changes to GitHub
2. Vercel auto-deploys from `main` branch
3. Or click "Redeploy" in Vercel dashboard

---

## 📞 Support

**Render Issues:**
- Docs: https://render.com/docs
- Status: https://status.render.com

**Vercel Issues:**
- Docs: https://vercel.com/docs
- Status: https://vercel-status.com

**AutoMech Issues:**
- Check logs in Render/Vercel dashboards
- Review HOSTING_GUIDE.md
- Test locally first: `npm run dev` (frontend) + `python main.py` (backend)

---

## 🎉 You're Done!

Your AutoMech is now live:
- **Frontend:** `https://your-app.vercel.app`
- **Backend:** `https://automech-backend.onrender.com`

Share your app and start diagnosing vehicles! 🚗🔧

---

**Need help?** Check the troubleshooting section or review the logs in your dashboards.
