#!/bin/bash

# Render.com startup script for AutoMech (Full Stack)

set -e  # Exit on error

echo "🚀 Starting AutoMech Full Stack on Render..."

# Install backend dependencies
echo "📦 Installing backend dependencies..."
pip install -r backend/requirements.txt

# Install Node.js and npm if not available
if ! command -v node &> /dev/null; then
    echo "📦 Installing Node.js..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
    apt-get install -y nodejs
fi

# Build frontend
echo "🎨 Building frontend..."
cd frontend
npm install
npm run build
cd ..

echo "✅ Build complete!"

# Start backend (which will also serve frontend static files)
echo "🔧 Starting server..."
cd backend
uvicorn main:app --host 0.0.0.0 --port $PORT
