#!/bin/bash

# AI Town Startup Script
# This script sets up and runs the AI Town simulation

echo "🤖 Starting AI Town..."
echo "================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating template..."
    cat > .env << EOF
# OpenRouter API Key - Get from https://openrouter.ai
OPENROUTER_API_KEY=your_api_key_here

# Flask Configuration
SECRET_KEY=your_secret_key_here
PORT=5000
DEBUG=True

# Simulation Settings
WORLD_WIDTH=50
WORLD_HEIGHT=50
MAX_AGENTS=10
UPDATE_INTERVAL=1.0
EOF
    echo "✅ Created .env file. Please edit it with your OpenRouter API key."
    echo "   Get your API key from: https://openrouter.ai"
    exit 1
fi

# Check if requirements are installed
echo "📦 Checking dependencies..."
if ! pip3 show flask &> /dev/null; then
    echo "📥 Installing dependencies..."
    pip3 install -r requirements.txt
fi

# Check if port 5000 is available
if lsof -ti:5000 &> /dev/null; then
    echo "⚠️  Port 5000 is already in use. Trying port 5001..."
    export PORT=5001
fi

# Start the server
echo "🚀 Starting AI Town server..."
echo "   Open http://localhost:${PORT:-5000} in your browser"
echo "   Press Ctrl+C to stop"
echo "================================"

python3 town_server.py
