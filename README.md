# 🎓 YuvaSaarthi 2.0
## National Education Platform for India 🇮🇳

**"Education for Every Indian, in Every Indian Language"**

YuvaSaarthi is an intelligent multilingual chatbot designed to help students across **all of India** with educational queries, competitive exam guidance, scholarship information, and concept explanations in **all 22 official Indian languages**.

---

## ✨ Changes in v2.0 (National Edition)

- **🚀 National Scope**: Expanded from Rajasthan-only to covered **36 States & UTs**.
- **🗣️ 23 Languages**: Support for **all 22 official languages** + English (previously only 3).
- **📚 Massive Knowledge Base**: Covers all state boards, 50+ competitive exams, and 150+ government portals.
- **⚡ Enhanced Translation**: Switched to Google Translate for faster, free, and more accurate multilingual support.

---

## 🌟 Key Features

### 🤖 **AI-Powered Assistance**
- **Education-Focused**: Strictly scoped to answer only education, career, and admission-related queries.
- **RAG (Retrieval Augmented Generation)**: Answers from verified national knowledge base.
- **Groq LLM**: Lightning-fast inference using Llama 3.3.
- **Concept Explanations**: Simplifies complex topics for Class 8-12 students.

### 📱 **Telegram Bot Integration**
- Full-featured Telegram bot for easy access on mobile.
- Supports voice/text queries in multiple languages.
- Delivers YouTube video recommendations directly in chat.

### 🌐 **Truly Multilingual (22+ Languages)**
- English, Hindi, Bengali, Telugu, Marathi, Tamil, Gujarati, Kannada, Malayalam, Odia, Punjabi...
- Assamese, Urdu, Sanskrit, Nepali, and more!
- **Auto-detection**: Speak in your mother tongue, get answers in your mother tongue.

### 📚 **Robust Knowledge Base**
- **Fault-Tolerant Ingestion**: Resume-capable document processing.
- **Comprehensive Data**:
  - Competitive exams (JEE, NEET, GATE, CAT, UPSC, SSC).
  - Scholarships & Financial Aid (National & State).
  - College Admissions (All India).

---

## 💻 System Requirements

### Hardware
- **RAM**: Minimum 8GB (16GB recommended for large vector databases).
- **Storage**: 2GB+ free space.
- **Internet**: Active connection for LLM and Translation APIs.

### Software
- **Operating System**: macOS, Linux, or Windows (WSL recommended).
- **Python**: Version 3.9 or higher.
- **Node.js**: Version 18 (LTS) or higher.

---

## 🚀 Quick Start

### Installation

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd YuvaSaarthi
   ```

2. **Run Setup Script**
   This script installs Python/Node dependencies and sets up the environment.
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Configure Environment**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` file and add your keys:
     - `GROQ_API_KEY`: Required.
     - `TELEGRAM_BOT_TOKEN`: Optional (for Bot).
     - `YOUTUBE_API_KEY`: Optional (for Videos).

4. **Ingest Documents**
   Process your educational documents into the knowledge base.
   ```bash
   python3 ingest_documents.py
   ```
   *Note: Use `python3 ingest_missed.py` to retry failed files if needed.*

5. **Start the Application**

   **Option A: Web Application**
   
   Terminal 1 (Backend):
   ```bash
   python3 api_server.py
   ```
   
   Terminal 2 (Frontend):
   ```bash
   cd frontend
   npm run dev
   ```
   Access at [http://localhost:3000](http://localhost:3000)

   **Option B: Telegram Bot**
   
   Terminal 3:
   ```bash
   python3 telegram_bot.py
   ```

---

## 📁 Project Structure

```
YuvaSaarthi/
├── backend/
│   ├── chatbot_engine.py      # Main chatbot logic
│   ├── document_processor.py  # RAG & PDF processing
│   ├── llm_handler.py         # Groq LLM integration
│   ├── google_translator.py   # New Google Translate service
│   └── youtube_search.py      # YouTube API
├── frontend/                  # Next.js Web App
│   ├── app/                   # App Router
│   ├── components/            # React Components
│   └── lib/                   # Utilities
├── data/
│   ├── documents/             # PDFs/Markdown for ingestion
│   └── vectorstore/           # ChromeDB files
├── api_server.py              # FastAPI Backend Server
├── telegram_bot.py            # Telegram Bot Interface
├── ingest_documents.py        # Main ingestion script
├── ingest_missed.py           # Recovery script for missed files
├── MAJOR_UPDATE.md            # Details of v2.0 changes
├── setup.sh                   # Setup script
└── requirements.txt           # Python dependencies
```

---

## 🔧 Configuration

Customize behavior in `.env`:

```env
# API Keys
GROQ_API_KEY=your_key_here
TELEGRAM_BOT_TOKEN=your_token_here

# Bot Settings
BOT_PERSONALITY=mix          # formal/friendly/mix
DEFAULT_LANGUAGE=hi

# RAG Settings
CHUNK_SIZE=1000
TOP_K_RESULTS=4
```

---

## 🛡️ License

MIT License - Free to use for educational purposes.

---

**Made with ❤️ for Students of India 🇮🇳**