#!/bin/bash

# YuvaSaarthi - Complete Setup Script

echo "=================================="
echo "🎓 YuvaSaarthi Setup"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Step 1: Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

echo ""
echo "✅ Python dependencies installed"
echo ""

# Step 2: Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

echo "✅ Node.js found: $(node --version)"
echo ""

# Step 3: Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo ""
echo "✅ Frontend dependencies installed"
echo ""

# Step 4: Check for knowledge base
if [ ! -d "data/chroma_db" ]; then
    echo "⚠️  Knowledge base not found. You need to run document ingestion."
    echo ""
    echo "Do you want to run it now? (y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo "📚 Running document ingestion..."
        python3 ingest_documents.py
    else
        echo "⏭️  Skipping document ingestion. Run 'python3 ingest_documents.py' later."
    fi
else
    echo "✅ Knowledge base found"
fi

echo ""
echo "=================================="
echo "✅ Setup Complete!"
echo "=================================="
echo ""
echo "To start YuvaSaarthi:"
echo ""
echo "1. Start Backend (Terminal 1):"
echo "   python3 api_server.py"
echo ""
echo "2. Start Frontend (Terminal 2):"
echo "   cd frontend && npm run dev"
echo ""
echo "3. Open browser:"
echo "   http://localhost:3000"
echo ""
echo "=================================="
