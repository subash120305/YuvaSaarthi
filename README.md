```
# 🎓 YuvaSaarthi
## AI-Powered National Educational Assistant for India

YuvaSaarthi is an intelligent multilingual chatbot designed to help students across India with educational queries, competitive exam guidance, scholarship information, and concept explanations in all 22 official Indian languages.

---

## ✨ Features

### 🤖 **AI-Powered Assistance**
- Answers questions about admissions, courses, exams, and fees
- Explains difficult concepts in simple terms
- Provides study guidance and tips
- Context-aware responses using RAG (Retrieval Augmented Generation)

### 🌐 **Multilingual Support**
- **All 22 Official Indian Languages** 🇮🇳
  - Hindi, Bengali, Telugu, Marathi, Tamil, Gujarati, Kannada, Malayalam, Odia, Punjabi
  - Assamese, Urdu, Kashmiri, Sindhi, Sanskrit, Nepali, Maithili, Konkani, Manipuri, Dogri, Santali, Bodo
- **English** 🇬🇧
- Auto-language detection
- Seamless translation using Google Translate
- Regional language support for local accessibility

### 📺 **YouTube Integration**
- Recommends relevant educational videos
- Searches in preferred language
- Curated educational content

### 💬 **Multiple Interfaces**
- **Telegram Bot** - Chat on-the-go
- **Web Interface** - Clean Streamlit UI

### 📚 **Comprehensive Knowledge Base**
- All Indian education boards (CBSE, ICSE, State boards)
- Competitive exam guidance (JEE, NEET, CUET, CLAT, UPSC, etc.)
- National & state scholarships information
- Government college admissions
- Reservation policies across all states
- 150+ verified official portals & links

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+** ([Download](https://www.python.org/downloads/))
- **Windows 10/11** (or Mac/Linux with minor modifications)
- **16GB RAM** recommended
- **2GB free disk space**

### Installation

1. **Clone or Download** this project

2. **Run Setup Script**
   ```bash
   setup.bat
   ```

3. **Configure API Keys**
   - Edit `.env` file
   - Add your API keys (see [API Setup Guide](docs/API_SETUP.md))

4. **Create Sample Data** (optional)
   ```bash
   python create_sample_data.py
   ```

5. **Ingest Documents**
   ```bash
   python ingest_documents.py
   ```

6. **Start the Bot**

   **Option A: Telegram Bot**
   ```bash
   python telegram_bot.py
   ```

   **Option B: Web Interface**
   ```bash
   streamlit run streamlit_app.py
   ```

---

## 📖 Documentation

- **[Installation Guide](docs/INSTALLATION.md)** - Detailed setup instructions
- **[API Setup Guide](docs/API_SETUP.md)** - How to get API keys
- **[Usage Guide](docs/USAGE.md)** - How to use the chatbot
- **[Demo Guide](docs/DEMO_GUIDE.md)** - Tips for presentations
- **[Architecture](docs/ARCHITECTURE.md)** - System design details

---

## 🔑 API Keys Required

| Service | Purpose | Cost | Required? |
|---------|---------|------|-----------|
| **Groq** | LLM (AI Brain) | FREE | ✅ Yes |
| **Bhashini** | Translation | FREE | ⚠️ Optional |
| **YouTube** | Video Search | FREE | ⚠️ Optional |
| **Telegram** | Bot Interface | FREE | ⚠️ If using Telegram |

**Note:** Only Groq API is mandatory. Others enhance functionality.

---

## 📁 Project Structure

```
YuvaSaarthi/
├── backend/
│   ├── chatbot_engine.py      # Main chatbot logic
│   ├── document_processor.py  # PDF processing & RAG
│   ├── llm_handler.py          # Groq LLM integration
│   ├── translator.py           # Bhashini translation
│   └── youtube_search.py       # YouTube API
├── frontend/
│   ├── telegram_bot.py         # Telegram interface
│   └── streamlit_app.py        # Web interface
├── utils/
│   ├── config.py               # Configuration
│   └── language_detector.py    # Language detection
├── data/
│   └── documents/              # PDF files go here
│       ├── textbooks/
│       ├── polytechnic/
│       ├── engineering/
│       └── administrative/
├── docs/                       # Documentation
├── requirements.txt            # Dependencies
├── .env.example                # Environment template
├── setup.bat                   # Setup script
└── README.md                   # This file
```

---

## 💡 Usage Examples

### Adding Your Textbooks

1. Place PDF files in `data/documents/textbooks/`
2. Name them: `class_10_mathematics.pdf`, `class_11_physics.pdf`, etc.
3. Run: `python ingest_documents.py`
4. Done! The chatbot can now answer from your books

### Sample Questions

**English:**
- "What are the admission requirements for polytechnic?"
- "Explain Pythagoras theorem in simple terms"
- "When are the semester exams?"

**Hindi:**
- "पॉलिटेक्निक में प्रवेश की आवश्यकताएं क्या हैं?"
- "पाइथागोरस प्रमेय को सरल शब्दों में समझाओ"
- "सेमेस्टर की परीक्षाएं कब हैं?"

**Rajasthani:**
- "दाखिलो री जरूरत कांई है?"
- "परीक्षा कद होसी?"

---

## 🎯 Key Components

### RAG System
- Retrieves relevant context from your documents
- Uses semantic search with embeddings
- Supports multilingual documents

### LLM (Groq)
- Lightning-fast responses
- Context-aware answers
- Personality: Mix of formal (admin) and friendly (study help)

### Translation (Google Translate)
- All 22 official Indian languages
- Auto language detection
- Free and reliable
- Regional language support

### YouTube Integration
- Educational video recommendations
- Language-specific searches
- Safe search enabled

---

## 🔧 Configuration

Edit `.env` file to customize:

```env
# Bot Settings
BOT_NAME=YuvaSaarthi
BOT_PERSONALITY=mix          # formal/friendly/mix
DEFAULT_LANGUAGE=hi          # en/hi/raj

# Organization Details
ORGANIZATION_NAME=YuvaSaarthi - National Education Assistant
ORGANIZATION=India
WEBSITE=https://yuvasaarthi.gov.in

# Advanced Settings
CHUNK_SIZE=1000              # Document chunk size
TOP_K_RESULTS=4              # Number of context docs
TEMPERATURE=0.7              # LLM creativity (0-1)
```

---

## 🧪 Testing

Test individual components:

```bash
# Test RAG system
python -m backend.document_processor

# Test LLM
python -m backend.llm_handler

# Test translation
python -m backend.translator

# Test YouTube search
python -m backend.youtube_search

# Test full chatbot
python -m backend.chatbot_engine
```

---

## 🐛 Troubleshooting

### "Groq API key not configured"
- Edit `.env` file
- Add your Groq API key from [console.groq.com](https://console.groq.com)

### "Vector store not found"
- Run: `python ingest_documents.py`
- Make sure you have PDF files in `data/documents/`

### "No PDF files found"
- Run: `python create_sample_data.py` for demo data
- OR add your own PDFs to `data/documents/textbooks/`

### "Module not found" errors
- Activate virtual environment: `venv\Scripts\activate`
- Reinstall dependencies: `pip install -r requirements.txt`

---

## 📊 System Requirements

### Minimum:
- 8GB RAM
- 2GB free disk space
- Internet connection (for APIs)
- Python 3.9+

### Recommended:
- 16GB RAM
- 5GB free disk space (for larger document collections)
- Stable internet connection

---

## 🤝 Contributing

This is a college project, but suggestions are welcome!

1. Test the chatbot
2. Add more sample documents
3. Improve translations
4. Enhance UI/UX
5. Report bugs

---

## 📜 License

MIT License - Free to use for educational purposes

---

## 👥 Credits

**Developed by:** [Your Name]
**For:** Department of Technical Education, Government of Rajasthan
**Academic Year:** 2024-25
**Institution:** [Your College Name]

**Technologies Used:**
- LangChain - RAG framework
- Groq - Fast LLM inference
- Bhashini - Government translation API
- Streamlit - Web interface
- Python Telegram Bot - Telegram integration
- ChromaDB - Vector database
- Sentence Transformers - Embeddings

---

## 📞 Support

For issues or questions:
1. Check [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
2. Review [FAQ](docs/FAQ.md)
3. Create an issue on GitHub

---

## 🎓 For Professors/Evaluators

### Project Highlights:
- ✅ Real-world application for government department
- ✅ Multilingual support (3 languages)
- ✅ Modern AI/ML technologies (RAG, LLM, Embeddings)
- ✅ Scalable architecture
- ✅ Multiple user interfaces
- ✅ Complete documentation
- ✅ Easy to demo and extend

### Demo Tips:
1. Show multilingual capabilities (switch languages mid-conversation)
2. Demonstrate concept explanation with YouTube videos
3. Show document Q&A (answer from uploaded PDFs)
4. Highlight Rajasthani language support (unique!)
5. Explain RAG system and how it works

See [Demo Guide](docs/DEMO_GUIDE.md) for detailed presentation tips.

---

## 🚀 Future Enhancements

- [ ] Voice input/output
- [ ] Mobile app (React Native)
- [ ] WhatsApp integration
- [ ] Advanced analytics dashboard
- [ ] Student progress tracking
- [ ] Practice problem generation
- [ ] Exam preparation mode
- [ ] Integration with college ERP systems

---

## ⭐ Star This Project

If you find this useful, please give it a star! ⭐

---

**Made with ❤️ for Students of India 🇮🇳**

```