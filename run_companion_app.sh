#!/bin/bash

echo "🎮 TFT Meta Guide - Companion App Launcher"
echo "=========================================="
echo ""

# Check if Flask is installed
if ! python -c "import flask" 2>/dev/null; then
    echo "⚠️  Flask not installed. Installing dependencies..."
    pip install flask flask-cors
    echo ""
fi

echo "🚀 Starting API server..."
echo "   Running on http://localhost:5000"
echo ""
echo "📖 Instructions:"
echo "   1. Wait for API server to start"
echo "   2. Open companion_app/index.html in your browser"
echo "   3. Enter your game state and get recommendations!"
echo ""
echo "⌨️  Press Ctrl+C to stop the server"
echo ""
echo "=========================================="
echo ""

# Start the API server
python backend/api.py
