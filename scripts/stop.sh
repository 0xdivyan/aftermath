#!/bin/bash
# Stop script for Aftermath bot

echo "🛑 Stopping Aftermath Bot..."
pkill -f "python -m src.main"
echo "✅ Bot stopped"
