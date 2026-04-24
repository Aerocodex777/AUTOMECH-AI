#!/bin/bash

# Startup script for Render with better error handling

set -e

echo "🚀 Starting AutoMech Server..."
echo "================================"

# Check environment variables
echo ""
echo "🔍 Checking environment variables..."

if [ -z "$GROQ_API_KEY" ] || [ "$GROQ_API_KEY" = "your_groq_api_key_here" ]; then
    echo "❌ ERROR: GROQ_API_KEY not set!"
    echo "Please set GROQ_API_KEY in Render dashboard"
    exit 1
fi
echo "✅ GROQ_API_KEY is set"

if [ -z "$JWT_SECRET_KEY" ]; then
    echo "⚠️  WARNING: JWT_SECRET_KEY not set, using default"
fi

if [ -z "$PORT" ]; then
    echo "⚠️  WARNING: PORT not set, using 8000"
    export PORT=8000
fi

echo "✅ PORT=$PORT"
echo "✅ PREFER_CLOUD_LLM=$PREFER_CLOUD_LLM"

# Start server
echo ""
echo "🚀 Starting uvicorn server..."
echo "================================"

cd backend
exec python -m uvicorn main:app --host 0.0.0.0 --port $PORT
