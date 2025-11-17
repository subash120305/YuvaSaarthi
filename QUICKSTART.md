# ⚡ Quick Start Guide - YuvaSaarthi

Get your AI chatbot running in **10 minutes**!

---

## 📋 Checklist

Before starting, make sure you have:
- [ ] Windows 10/11
- [ ] Python 3.9+ installed
- [ ] Internet connection
- [ ] 10 minutes of time

---

## 🚀 Steps

### 1️⃣ Setup (2 minutes)

Open Command Prompt or PowerShell in the project folder and run:

```bash
setup.bat
```

This will:
- Create virtual environment
- Install all dependencies
- Create `.env` file

---

### 2️⃣ Get Groq API Key (2 minutes)

1. Go to: https://console.groq.com
2. Sign up (use Google/GitHub)
3. Create API Key
4. Copy the key (starts with `gsk_`)

---

### 3️⃣ Add API Key (1 minute)

Edit `.env` file and add your key:

```env
GROQ_API_KEY=gsk_your_key_here
```

Save the file.

---

### 4️⃣ Create Sample Data (2 minutes)

```bash
python create_sample_data.py
```

This creates sample educational PDFs for testing.

---

### 5️⃣ Process Documents (2 minutes)

```bash
python ingest_documents.py
```

Type `yes` when asked. This creates the knowledge base.

---

### 6️⃣ Start Chatbot (1 minute)

**Option A: Web Interface** (Easier for demo)

```bash
streamlit run streamlit_app.py
```

Browser will open automatically at http://localhost:8501

**Option B: Telegram Bot**

First, get Telegram bot token from @BotFather, add to `.env`, then:

```bash
python telegram_bot.py
```

---

## ✅ You're Done!

Try asking:
- "Explain Pythagoras theorem"
- "पाइथागोरस प्रमेय समझाओ"
- "What are admission requirements?"

---

## 🎯 Adding Your Own PDFs

1. Put PDF files in: `data/documents/textbooks/`
2. Name them: `class_10_math.pdf`, `class_11_physics.pdf`, etc.
3. Run: `python ingest_documents.py`
4. Done! Ask questions about your PDFs

---

## ❌ Troubleshooting

**"Python not found"**
→ Install Python from python.org

**"Groq API error"**
→ Check your API key in `.env` file

**"No documents found"**
→ Run `python create_sample_data.py` first

**"Module not found"**
→ Run `setup.bat` again

---

## 📚 Full Documentation

- [Complete README](README.md)
- [API Setup Guide](docs/API_SETUP.md)
- [Demo Tips](docs/DEMO_GUIDE.md)

---

**Need help? Check the docs or troubleshooting guide!**
