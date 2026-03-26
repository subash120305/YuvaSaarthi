#!/bin/bash
echo "🚀 Starting YuvaSaarthi..."

# Check if ingestion is running
if pgrep -f "ingest_documents.py" > /dev/null; then
    echo "⚠️  Document ingestion is still running!"
    echo "   Please wait for it to finish."
    echo "   You can monitor progress with: tail -f logs/ingestion.log"
    exit 1
fi

echo "✅ Database ready."
echo "Starting Backend Server..."
python3 api_server.py
