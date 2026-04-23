#!/bin/bash

# Render.com build script for AutoMech backend

set -e  # Exit on error

echo "🔧 Starting Render build..."

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Build complete!"
