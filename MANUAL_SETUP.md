# YuvaSaarthi - Manual Setup Commands

## Step 1: Install Python Dependencies (2-3 minutes)

Open Terminal and run:

```bash
cd /Users/admin/Desktop/YuvaSaarthi

pip3 install langchain langchain-community langchain-groq chromadb sentence-transformers pypdf groq requests google-api-python-client langdetect python-telegram-bot streamlit pydantic pydantic-settings python-dotenv loguru fastapi uvicorn python-multipart googletrans==4.0.0-rc1
```

Wait for installation to complete (you'll see progress).

---

## Step 2: Create Knowledge Base (1-2 minutes)

```bash
python3 ingest_documents.py
```

Type "yes" when prompted.

---

## Step 3: Start Backend (Keep this terminal open)

```bash
python3 api_server.py
```

You should see:
- "YuvaSaarthi API Server starting..."
- "Uvicorn running on http://0.0.0.0:8000"

**Leave this running!**

---

## Step 4: Start Frontend (New terminal window)

Open a NEW terminal window and run:

```bash
cd /Users/admin/Desktop/YuvaSaarthi/frontend

npm install

npm run dev
```

You should see:
- "Ready in Xms"
- "Local: http://localhost:3000"

---

## Step 5: Open Browser

Open your browser and go to:

```
http://localhost:3000
```

---

## ✅ Done!

You should now see the YuvaSaarthi chat interface.

---

## Troubleshooting

### If backend fails:
```bash
# Check Python version (need 3.9+)
python3 --version

# Try running ingestion again
python3 ingest_documents.py
```

### If frontend fails:
```bash
# Clear and reinstall
cd frontend
rm -rf node_modules .next
npm install
npm run dev
```

### Kill processes if needed:
```bash
# Kill backend (port 8000)
lsof -ti:8000 | xargs kill -9

# Kill frontend (port 3000)  
lsof -ti:3000 | xargs kill -9
```

---

**Questions? Check FINAL_README.md for complete documentation.**
