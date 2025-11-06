#!/bin/bash

# Bot Chat Frontend Startup Script
# Starts the React frontend on localhost:3000

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 Starting Bot Chat Frontend..."
echo "📍 Directory: $SCRIPT_DIR"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    echo "✅ Dependencies installed"
fi

# Check if .env file exists, create one if not
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
# API Base URL
VITE_API_BASE_URL=http://localhost:5000/api
EOF
    echo "✅ .env file created"
fi

echo ""
echo "🌐 Starting development server on http://localhost:3000"
echo "   Press Ctrl+C to stop"
echo ""

# Start the dev server
npm run dev

