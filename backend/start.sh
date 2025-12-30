#!/bin/bash

# Start script for Home Energy Advisor Backend

echo "🏠 Starting Home Energy Advisor Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "🔌 Activating virtual environment..."
    source venv/bin/activate
    echo "📥 Installing dependencies (downloading packages, please wait 2-3 minutes)..."
    echo "    You'll see download progress below..."
    echo ""
    # Use pip config to disable version checks and show progress
    export PIP_CONFIG_FILE=$(pwd)/pip.conf
    export PIP_DISABLE_PIP_VERSION_CHECK=1
    pip install --upgrade pip setuptools wheel -q
    pip install -r requirements.txt
    echo ""
    echo "✅ Dependencies installed successfully!"
else
    echo "🔌 Activating virtual environment..."
    source venv/bin/activate
    echo "✅ Virtual environment already exists (skipping dependency installation)"
    echo "   To reinstall dependencies, run: rm -rf venv && ./start.sh"
fi

# Disable pip version warnings for the session
export PIP_DISABLE_PIP_VERSION_CHECK=1

# Check if Ollama is running (for default LLM provider)
echo "🤖 Checking Ollama status..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama is running"
else
    echo "⚠️  Ollama is not running. Start it with: ollama serve"
    echo "   Or configure a different LLM provider in .env"
fi

# Start the server
echo "🚀 Starting FastAPI server..."
echo "📝 API Documentation: http://localhost:8000/docs"
echo "🏥 Health Check: http://localhost:8000/health"
echo ""

PYTHONPATH=$(pwd) uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
