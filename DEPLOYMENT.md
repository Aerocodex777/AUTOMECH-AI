# AutoMech AI — Deployment Guide

## Deployment Options

### Option 1: Local Development (Current Setup)
✅ Already configured
- Backend: http://localhost:8000
- Frontend: http://localhost:5173
- Database: SQLite (automech.db)

### Option 2: Production VPS (Recommended for Kerala Workshop)

#### Requirements
- Ubuntu 22.04 VPS (2GB RAM minimum)
- Domain name (optional but recommended)
- SSL certificate (Let's Encrypt)

#### Setup Steps

**1. Server Setup**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip -y

# Install Node.js 20
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install nodejs -y

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Install Nginx
sudo apt install nginx -y
```

**2. Database Setup**
```bash
sudo -u postgres psql
CREATE DATABASE automech;
CREATE USER automech_user WITH PASSWORD 'secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE automech TO automech_user;
\q
```

**3. Clone & Configure**
```bash
cd /var/www
sudo git clone <your-repo> automech
cd automech

# Backend setup
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure .env
nano .env
# Add:
# GROQ_API_KEY=your_actual_key
# DATABASE_URL=postgresql+asyncpg://automech_user:secure_password_here@localhost:5432/automech

# Frontend setup
cd ../frontend
npm install
npm run build
```

**4. Systemd Service (Backend)**
```bash
sudo nano /etc/systemd/system/automech-backend.service
```

```ini
[Unit]
Description=AutoMech AI Backend
After=network.target postgresql.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/automech/backend
Environment="PATH=/var/www/automech/backend/venv/bin"
ExecStart=/var/www/automech/backend/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable automech-backend
sudo systemctl start automech-backend
sudo systemctl status automech-backend
```

**5. Nginx Configuration**
```bash
sudo nano /etc/nginx/sites-available/automech
```

```nginx
server {
    listen 80;
    server_name your-domain.com;  # or server IP

    # Frontend (React build)
    location / {
        root /var/www/automech/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/automech /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

**6. SSL Certificate (Let's Encrypt)**
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

**7. Update Frontend API URL**
Edit `frontend/src/components/Chat.jsx` and `VehicleProfile.jsx`:
```javascript
const API = '/api'  // Change from http://localhost:8000
```

Rebuild frontend:
```bash
cd /var/www/automech/frontend
npm run build
```

### Option 3: Docker Deployment

**docker-compose.yml**
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: automech
      POSTGRES_USER: automech
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

  backend:
    build: ./backend
    environment:
      GROQ_API_KEY: ${GROQ_API_KEY}
      DATABASE_URL: postgresql+asyncpg://automech:secure_password@postgres:5432/automech
    ports:
      - "8000:8000"
    depends_on:
      - postgres
    restart: always
    volumes:
      - ./backend/data:/app/data
      - ./backend/vectorstore:/app/vectorstore

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: always

volumes:
  postgres_data:
```

**backend/Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

**frontend/Dockerfile**
```dockerfile
FROM node:20 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**frontend/nginx.conf**
```nginx
server {
    listen 80;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://backend:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Deploy**
```bash
docker-compose up -d
```

### Option 4: Cloud Platforms

#### Render.com (Easiest)

**Backend (Web Service)**
- Build Command: `pip install -r requirements.txt`
- Start Command: `cd backend && python main.py`
- Environment Variables:
  - `GROQ_API_KEY`: your_key
  - `DATABASE_URL`: (use Render PostgreSQL add-on)

**Frontend (Static Site)**
- Build Command: `cd frontend && npm install && npm run build`
- Publish Directory: `frontend/dist`

#### Railway.app

**Backend**
- Root Directory: `backend`
- Start Command: `python main.py`
- Add PostgreSQL plugin
- Set GROQ_API_KEY in variables

**Frontend**
- Root Directory: `frontend`
- Build Command: `npm install && npm run build`
- Start Command: `npx serve -s dist -p $PORT`

#### Vercel (Frontend Only)

```bash
cd frontend
vercel --prod
```

Update API URL to your backend deployment.

## Post-Deployment Checklist

### Security
- [ ] HTTPS enabled (SSL certificate)
- [ ] Firewall configured (UFW or cloud firewall)
- [ ] PostgreSQL not exposed to internet
- [ ] Strong database password
- [ ] GROQ_API_KEY in environment (not in code)
- [ ] CORS restricted to your domain

### Performance
- [ ] Nginx gzip compression enabled
- [ ] Static assets cached
- [ ] Database indexes created
- [ ] ChromaDB persistent storage configured

### Monitoring
- [ ] Backend logs accessible (`journalctl -u automech-backend -f`)
- [ ] Nginx access logs monitored
- [ ] Disk space monitored (vector store grows)
- [ ] API rate limits configured

### Backup
- [ ] PostgreSQL daily backups
- [ ] Vector store backed up
- [ ] Vehicle manuals backed up
- [ ] .env file backed up securely

### Testing
- [ ] Health check: `curl https://your-domain.com/api/`
- [ ] Create vehicle via API
- [ ] Run diagnosis
- [ ] Check PWA installability
- [ ] Test on mobile device

## Maintenance

### Update Application
```bash
cd /var/www/automech
git pull
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart automech-backend

cd ../frontend
npm install
npm run build
```

### View Logs
```bash
# Backend logs
sudo journalctl -u automech-backend -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Database Backup
```bash
pg_dump -U automech_user automech > backup_$(date +%Y%m%d).sql
```

### Add Vehicle Manuals
```bash
# Upload PDFs to server
scp manual.pdf user@server:/var/www/automech/backend/data/manuals/

# Restart backend to re-index
sudo systemctl restart automech-backend
```

## Cost Estimates (Monthly)

### VPS Hosting
- DigitalOcean Droplet (2GB): $12/month
- Hetzner Cloud (2GB): €4.50/month
- Vultr (2GB): $10/month

### Cloud Platforms
- Render.com: $7/month (starter)
- Railway.app: $5/month (hobby)
- Vercel: Free (frontend only)

### API Costs
- Groq API: Free tier (generous limits)
- Upgrade if needed: Pay-as-you-go

### Total Estimate
**Budget Setup**: $5-10/month (Railway/Render)
**Professional Setup**: $15-20/month (VPS + domain + SSL)

## Support

For deployment issues:
1. Check logs first
2. Verify environment variables
3. Test database connection
4. Confirm Groq API key is valid
5. Check firewall rules

---

**Production URL**: _________________
**Deployed**: _________________
**Maintained by**: _________________
