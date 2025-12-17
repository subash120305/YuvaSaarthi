# YuvaSaarthi - Complete Setup Guide

## Quick Start

### 1. Install Python Dependencies
```bash
cd /Users/admin/Desktop/YuvaSaarthi
pip install -r requirements.txt
pip install googletrans==4.0.0-rc1
pip install fastapi uvicorn python-multipart
```

### 2. Ingest Documents (Knowledge Base)
```bash
python ingest_documents.py
```

### 3. Start Backend API Server
```bash
python api_server.py
```
The API will run on: http://localhost:8000

### 4. Install Frontend Dependencies & Start
```bash
cd frontend
npm install
npm run dev
```
The frontend will run on: http://localhost:3000

---

## What's Changed

### Frontend (Next.js):
- ✅ **No Sidebar** - Clean, single-chat interface
- ✅ **LocalStorage** - Chat history persists
- ✅ **23 Languages** - Full Indian language support
- ✅ **Backend Integration** - Connected to Python API
- ✅ **Glassmorphic Design** - Professional UI
- ✅ **Settings in Navbar** - About/Help moved to dropdown

### Backend (Python):
- ✅ **FastAPI Server** - New API layer
- ✅ **Google Translate** - All 23 languages
- ✅ **RAG Integration** - Document search
- ✅ **CORS Enabled** - Frontend can connect

---

## API Endpoints

### POST /api/chat
Send a message and get AI response

**Request:**
```json
{
  "message": "What are JEE exam dates?",
  "language": "en",
  "conversation_id": "user123"
}
```

**Response:**
```json
{
  "response": "JEE Main 2026 dates are...",
  "videos": [],
  "language": "en"
}
```

### GET /api/languages
Get list of supported languages

### GET /api/health
Che</s> health

---

## File Structure

```
YuvaSaarthi/
├── frontend/               # Next.js UI
│   ├── app/
│   ├── components/
│   │   ├── chat-interface.tsx    (Modified - No sidebar)
│   │   ├── navbar.tsx             (Modified - Settings dropdown)
│   │   ├── chat-area.tsx
│   │   ├── chat-input.tsx
│   │   └── ...
│   └── package.json
│
├── backend/               # Python Backend
│   ├── chatbot_engine.py
│   ├── document_processor.py
│   ├── google_translator.py
│   └── ...
│
├── api_server.py         # NEW - FastAPI server
├── ingest_documents.py
└── requirements.txt
```

---

## Development Workflow

1. **Make sure documents are ingested:**
   ```bash
   python ingest_documents.py
   ```

2. **Start backend (Terminal 1):**
   ```bash
   python api_server.py
   ```

3. **Start frontend (Terminal 2):**
   ```bash
   cd frontend && npm run dev
   ```

4. **Open browser:**
   http://localhost:3000

---

## Features

### Chat Interface:
- Send messages
- Get AI responses with knowledge base
- Auto-translate to/from 23 languages
- Code syntax highlighting
- Markdown support
- Copy/Like/Share responses

### Language Support:
- Hindi, Bengali, Telugu, Tamil, Marathi, Gujarati
- Kannada, Malayalam, Odia, Punjabi, Assamese, Urdu
- +11 more Indian languages
- Auto language detection

### Settings (Top-right menu):
- Theme toggle (Light/Dark)
- About YuvaSaarthi
- Help & Support
- Clear chat history

---

## Troubleshooting

### Backend Issues:
```bash
# Check if vector store exists
ls data/chroma_db/

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend Issues:
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules .next
npm install
```

### Port Already in Use:
```bash
# Backend (kill port 8000)
lsof -ti:8000 | xargs kill -9

# Frontend (kill port 3000)
lsof -ti:3000 | xargs kill -9
```

---

## Production Deployment

### Backend:
- Deploy on Railway/Render
- Or use Vercel Serverless Functions

### Frontend:
- Deploy on Vercel (automatic)
- Or Netlify

---

**Ready to use!** 🚀
