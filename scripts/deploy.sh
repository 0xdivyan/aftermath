#!/bin/bash
# Deployment script for Aftermath bot

set -e

echo "🚀 Deploying Aftermath Bot..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "📝 Creating from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your API keys before running!"
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p data

# Run tests
echo "🧪 Running tests..."
pytest tests/ -v

# Start bot
echo "✅ Deployment complete!"
echo "To start the bot:"
echo "  source venv/bin/activate"
echo "  python -m src.main"