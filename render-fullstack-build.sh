#!/bin/bash

# Render Full Stack Build Script for AutoMech
# Builds both backend and frontend

set -e  # Exit on error

echo "🚀 AutoMech Full Stack Build Starting..."
echo "=========================================="

# ── Python Version Check & Fix ─────────────────────────────────────────────

echo ""
echo "🐍 Checking Python version..."
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
echo "Current Python: $PYTHON_VERSION"

# Check if Python 3.11 is available
if command -v python3.11 &> /dev/null; then
    echo "✅ Found Python 3.11, using it..."
    alias python=python3.11
    alias pip=pip3.11
    PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
    echo "Now using Python: $PYTHON_VERSION"
fi

# ── Backend Setup ──────────────────────────────────────────────────────────

echo ""
echo "📦 Step 1: Installing Backend Dependencies..."
python -m pip install --upgrade pip setuptools wheel

# Install dependencies
echo "Installing from requirements.txt..."
python -m pip install -r backend/requirements.txt

echo "✅ Backend dependencies installed"

# ── Frontend Setup ─────────────────────────────────────────────────────────

echo ""
echo "📦 Step 2: Installing Frontend Dependencies..."
cd frontend

# Check if npm is available
if ! command -v npm &> /dev/null; then
    echo "❌ npm not found! Installing Node.js..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
    apt-get install -y nodejs
fi

npm install
echo "✅ Frontend dependencies installed"

# ── Frontend Build ─────────────────────────────────────────────────────────

echo ""
echo "🎨 Step 3: Building Frontend..."
npm run build
echo "✅ Frontend built successfully"

cd ..

# ── Verification ───────────────────────────────────────────────────────────

echo ""
echo "🔍 Step 4: Verifying Build..."

if [ -d "frontend/dist" ]; then
    echo "✅ Frontend dist folder exists"
    echo "   Files: $(ls -la frontend/dist | wc -l) items"
else
    echo "❌ Frontend dist folder not found!"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ Full Stack Build Complete!"
echo "=========================================="
echo ""
echo "📂 Structure:"
echo "   backend/     → Python API"
echo "   frontend/dist/ → Built React app"
echo ""
echo "🚀 Ready to start server..."
