# 🎓 YuvaSaarthi
## AI Educational Assistant - Department of Technical Education, Rajasthan

**Complete RAG-based chatbot with multilingual support (English/Hindi/Rajasthani)**

---

## ⚡ Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add API key to .env
GROQ_API_KEY=your_key_here

# 3. Launch (choose one)
streamlit run streamlit_app.py          # Web interface
python telegram_bot.py                  # Telegram bot
```

**✅ Vector Store Ready:** 15,685 embeddings from 402 documents already loaded!

---

## ✨ Features

### Core Capabilities
- **🤖 AI-Powered Q&A** - RAG + Groq LLM (Llama 3.3 70B)
- **📚 402 Documents Indexed** - 393 RBSE textbooks (Class 8-10) + Knowledge bases
- **🌐 Multilingual** - English, Hindi, Rajasthani support
- **🎯 Education-Focused** - Politely declines non-education queries
- **📱 Multiple Interfaces** - Web UI (Streamlit) + Telegram Bot
- **💬 Modern Chat UI** - Clean interface with action buttons

### Smart Features
- **📺 YouTube Videos** - 2 educational videos per concept (optional, free API key)
- **📚 Web Articles** - 3 educational articles per concept (DuckDuckGo, no API needed)
- **🎓 Subject Coverage** - Class 8-12, Engineering, Polytechnic, Technical Education
- **🔍 Deep Retrieval** - Answers from actual textbook content, not hallucinations
- **✅ Health Monitoring** - System status check for all components

### Latest UI Updates
- **Modern Chat Layout** - User messages right-aligned, assistant messages left-aligned
- **Action Buttons** - Copy, Like, Dislike, Regenerate, Share on each assistant message
- **Smart Suggestions** - 3 quick suggestions with real-time filtering
- **Compact Controls** - Language dropdown and settings gear icon beside search box
- **Bilingual Welcome** - Helpful introduction message on first load

---

## 📦 What's Included

### Documents (402 Files)

**🎓 RBSE Textbooks (393 PDFs):**
- **Class 8**: English, Hindi, Maths, Science, Social Science (multiple books each)
- **Class 9**: English, Hindi, Maths, Science, Social Science (multiple books each)
- **Class 10**: English, Hindi, Maths, Science, Social Science (multiple books each)
- Both English and Hindi medium textbooks

**📚 Knowledge Bases:**
- `complete-kb-final.md` - Comprehensive Rajasthan education KB
  - RBSE syllabus, exam patterns, grading systems
  - Reservation policies (SC/ST/OBC/EWS/PwD with exact percentages)
  - Scholarship programs and eligibility criteria
  - Engineering, Medical, Law admission processes
  - Income limits, domicile requirements
- `rajasthan_education_kb_complete.json` - Structured hierarchical KB

**📋 Administrative Documents:**
- Admission guidelines and information
- Scholarship schemes and application process
- Fee structures and payment details

**📊 Vector Store:** 15,685 embeddings ready for instant retrieval

---

## 🔑 API Setup

### Required: Groq API (FREE)
1. Visit: https://console.groq.com
2. Sign up with Google/GitHub
3. Create API key
4. Add to `.env`:
   ```env
   GROQ_API_KEY=gsk_your_key_here
   ```

### Optional: YouTube API (FREE - 100 searches/day)
1. Visit: https://console.cloud.google.com
2. Create project and enable YouTube Data API v3
3. Create API key
4. Add to `.env`:
   ```env
   YOUTUBE_API_KEY=your_key_here
   ```

### Optional: Telegram Bot (FREE)
1. Open Telegram, search `@BotFather`
2. Send `/newbot` and follow instructions
3. Copy token to `.env`:
   ```env
   TELEGRAM_BOT_TOKEN=your_token_here
   ```

**Note:** Web search (DuckDuckGo) and translation (Google Translate) are completely free with no API keys required!

---

## 🚀 Usage

### Web Interface
```bash
streamlit run streamlit_app.py
```
Opens at http://localhost:8501

**Features:**
- Modern chat interface with message history
- Language selector (English/Hindi/Rajasthani)
- Quick suggestion buttons with real-time filtering
- Action buttons (Copy, Like, Dislike, Regenerate, Share)
- Settings menu (Check Status, Clear Chat)
- Video and article recommendations
- Bilingual welcome message

### Telegram Bot
```bash
python telegram_bot.py
```

**Commands:**
- `/start` - Welcome message with your Telegram name
- `/help` - Show all commands
- `/language` - Change language (EN/HI/RAJ)
- `/clear` - Clear conversation history
- `/videos` - Toggle video recommendations

**Features:**
- Personalized greetings: "Hello {your_name}!"
- Same smart Q&A as web interface
- Mobile-friendly experience
- Works on any device

### System Health Check
```bash
python -c "from backend.chatbot_engine import get_chatbot; print(get_chatbot().get_system_health())"
```

Expected output:
```
LLM: healthy
YouTube: not_configured (optional)
Web Search: healthy
Translation: fallback (Google Translate active)
Vector Store: healthy (15,685 embeddings)
```

---

## 💡 Sample Queries

### Will Answer ✅

**Administrative & Admissions:**
- "What is SC reservation percentage in Rajasthan?"
- "What are admission requirements for polytechnic?"
- "Tell me about EWS income limit"
- "What scholarships are available?"

**Educational & Textbooks:**
- "Explain Pythagoras theorem"
- "What is photosynthesis?"
- "Summarize quadratic equations chapter"
- "What subjects are in CSE?"

**Study Guidance:**
- "How do I prepare for Class 10 math exam?"
- "Which branch should I choose for software development?"
- "What is the best way to learn physics?"

**Multilingual:**
- English: "What is the admission process?"
- Hindi: "प्रवेश की प्रक्रिया क्या है?"
- Rajasthani: "दाखिलो री प्रक्रिया बताओ"

### Will Politely Decline ❌

**Non-Education Queries:**
- Sports scores, entertainment, movies, music
- Current news, politics, weather
- Cooking, health tips, lifestyle
- Shopping, recipes, general knowledge

**Polite Response:**
> "मैं युवासारथी हूँ, केवल शिक्षा से संबंधित प्रश्नों में मदद के लिए बनाया गया। मैं आपकी सहायता कर सकता हूँ:
> • शैक्षणिक विषय (कक्षा 8-12, इंजीनियरिंग)
> • प्रवेश, फीस, छात्रवृत्ति, आरक्षण
> • परीक्षा, परिणाम, पाठ्यक्रम
> • अध्ययन मार्गदर्शन और करियर सलाह
>
> कृपया शिक्षा से जुड़े प्रश्न पूछें!"

---

## 🎯 User Experience

### Query Example: "What is Pythagoras theorem?"

**1. Text Answer** (from textbook or LLM knowledge):
> "पाइथागोरस प्रमेय कहता है कि एक समकोण त्रिभुज में, कर्ण का वर्ग दोनों अन्य भुजाओं के वर्गों के योग के बराबर होता है..."

**2. 📺 YouTube Videos** (2 videos - if API key configured):
- "Pythagoras Theorem Explained | Khan Academy Hindi"
- "Complete Proof of Pythagoras Theorem | Byju's"

**3. 📚 Web Articles** (3 articles - always available):
- Khan Academy: "Pythagoras Theorem"
- Wikipedia: "Pythagorean theorem"
- NCERT: "Baudhayan Theorem"

**Action Buttons:**
- ⎘ Copy - Copy response to clipboard
- 👍 Like - Mark as helpful
- 👎 Dislike - Mark for improvement
- ↻ Regenerate - Get new response
- ⇗ Share - Share response (requires deployment)

---

## 🛠️ Technical Stack

- **LLM**: Groq (Llama 3.3 70B) - Fast, free inference
- **RAG**: LangChain + ChromaDB
- **Embeddings**: HuggingFace (paraphrase-multilingual-mpnet-base-v2)
- **Translation**: Google Translate (free, no API key)
- **Web Search**: DuckDuckGo (free, no API key)
- **YouTube**: YouTube Data API v3 (optional, free)
- **Frontend**: Streamlit (web) + python-telegram-bot
- **Backend**: Python 3.9+

---

## 📁 Project Structure

```
YuvaSaarthi/
├── README.md                  ← Complete documentation
├── requirements.txt           ← All dependencies
├── .env                       ← Your API keys
│
├── backend/                   ← AI Engine
│   ├── chatbot_engine.py     ← Main orchestration
│   ├── rag_system.py         ← RAG implementation
│   ├── llm_handler.py        ← Groq LLM integration
│   ├── document_processor.py ← PDF processing + embeddings
│   ├── translator.py         ← Translation (Google Translate)
│   ├── youtube_search.py     ← Video recommendations
│   └── web_search.py         ← Article search (DuckDuckGo)
│
├── utils/
│   ├── config.py             ← Settings & system prompt
│   └── logging_config.py     ← Logging setup
│
├── data/
│   ├── documents/            ← 402 documents
│   │   ├── textbooks/       ← 393 RBSE PDFs
│   │   │   ├── class_8/
│   │   │   ├── class_9/
│   │   │   └── class_10/
│   │   └── administrative/  ← Knowledge bases
│   └── vectorstore/         ← ChromaDB (15,685 embeddings)
│
├── streamlit_app.py          ← Web interface
├── telegram_bot.py           ← Telegram bot
├── ingest_documents.py       ← Document ingestion (already done)
└── test_system.py            ← Health check script
```

---

## 🔧 Configuration

### Environment Variables (.env)

```env
# Required
GROQ_API_KEY=gsk_your_key_here

# Optional (free services)
YOUTUBE_API_KEY=your_youtube_key_here
TELEGRAM_BOT_TOKEN=your_telegram_token_here

# Auto-configured (no setup needed)
# - Google Translate (free, automatic)
# - DuckDuckGo Search (free, automatic)
```

### System Settings (utils/config.py)

- **Department Name**: Department of Technical Education
- **Default Language**: English
- **Embedding Model**: paraphrase-multilingual-mpnet-base-v2
- **LLM Model**: llama-3.3-70b-versatile
- **Chunk Size**: 1000 characters
- **Chunk Overlap**: 200 characters
- **Search Results**: Top 5 relevant chunks

---

## 📊 System Status

| Component | Status | Cost | Required |
|-----------|--------|------|----------|
| LLM (Groq) | ✅ Healthy | FREE | ✅ Required |
| Vector Store | ✅ 15,685 embeddings | FREE | ✅ Required |
| Web Search | ✅ DuckDuckGo | FREE | ✅ Always On |
| Translation | ✅ Google Translate | FREE | ✅ Always On |
| YouTube API | ⚠️ Not configured | FREE (optional) | ❌ Optional |
| Telegram Bot | ⚠️ Not configured | FREE (optional) | ❌ Optional |

**Total Monthly Cost: ₹0** 🎉

---

## 🎓 For Demo/Presentation

### 5-Minute Demo Flow

**1. System Overview** (1 minute)
- Show project structure
- Explain RAG architecture
- Mention 402 real documents (393 RBSE textbooks)

**2. Launch Web Interface** (30 seconds)
```bash
streamlit run streamlit_app.py
```

**3. Live Demo** (3 minutes)

Try these queries in order:
1. **"What is Pythagoras theorem?"**
   - Shows textbook answer + 3 articles
   - Proves RAG works with real content

2. **"What is SC reservation in Rajasthan?"**
   - Shows official KB data with exact percentages
   - Proves knowledge base integration

3. **"What is cricket score?"**
   - Politely declines with education-focused message
   - Proves scope filtering works

4. **Switch to Hindi**: "प्रकाश संश्लेषण क्या है?"
   - Gets Hindi response
   - Proves multilingual support

**4. Highlight Unique Features** (30 seconds)
- 393 actual RBSE textbooks, not generated samples
- Rajasthani language support (unique!)
- Education-focused (politely declines off-topic)
- Modern UI with action buttons
- Free resources (videos + articles)
- Production-ready architecture

### Key Selling Points

✅ **402 Real Documents** - Actual RBSE textbooks with official data
✅ **15,685 Embeddings** - Deep retrieval from any page/chapter
✅ **Education-Focused** - Smart scope filtering for relevant answers
✅ **Multilingual** - English/Hindi/Rajasthani (rare!)
✅ **Free Resources** - YouTube videos + web articles
✅ **Modern UI** - ChatGPT-style action buttons
✅ **Production-Ready** - Complete code, tested, documented
✅ **Zero Cost** - Completely free to run (₹0/month)

---

## 🧪 Testing & Verification

### Health Check
```bash
python test_system.py
```

### Test Queries
```bash
# Launch web interface
streamlit run streamlit_app.py

# Try these:
# 1. "What is photosynthesis?"           → Educational answer
# 2. "SC reservation percentage?"        → KB data
# 3. "What is cricket?"                  → Polite decline
# 4. "प्रवेश की प्रक्रिया?"              → Hindi response
```

### Expected Results
- ✅ Educational queries → Detailed answers + resources
- ✅ KB queries → Accurate official data
- ✅ Non-education queries → Polite decline message
- ✅ Hindi queries → Hindi responses
- ✅ Action buttons → Functional (Copy, Like, Dislike, Regenerate)

---

## 🚀 Deployment Options

### Free Hosting Options

**Streamlit Cloud (Recommended):**
1. Push code to GitHub
2. Visit: https://streamlit.io/cloud
3. Connect GitHub repo
4. Add secrets (API keys)
5. Deploy!

**Railway:**
- Free tier: 500 hours/month
- Easy deployment with GitHub

**Render:**
- Free tier available
- Auto-deploy from GitHub

### Requirements for Deployment
- Add API keys in platform secrets/env variables
- Ensure `requirements.txt` is complete
- Vector store will be built on first run (one-time, 30-60 min)

---

## 🔮 Future Enhancements

### Planned Features
- [ ] Class 11-12 textbook coverage
- [ ] Voice input/output support
- [ ] PDF download of chat history
- [ ] Admin dashboard for analytics
- [ ] User feedback collection
- [ ] More regional languages

### Easy to Add
- More textbooks (just drop PDFs in data/documents/)
- Custom knowledge bases (MD or JSON files)
- Additional languages (configure in utils/config.py)
- Custom UI themes (modify streamlit_app.py CSS)

---

## 🆘 Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### "Groq API error"
- Check `.env` has correct `GROQ_API_KEY`
- Verify key is active at https://console.groq.com

### "Vector store not found"
- Already done! 15,685 embeddings ready
- If missing, run: `python backend/document_processor.py`

### "Translation: fallback"
- This is GOOD! Means Google Translate is working (free)
- No API key needed for translation

### "YouTube: not_configured"
- This is OPTIONAL - add YouTube API key only if you want videos
- Web articles work without it

### "Memory/page file too small"
- Embeddings use lazy loading (only load when needed)
- No changes needed - works automatically

### Web interface not updating
- Press `Ctrl+C` to stop Streamlit
- Run again: `streamlit run streamlit_app.py`

---

## 📚 Additional Resources

### Official Documentation
- **RBSE Textbooks**: https://rajeduboard.rajasthan.gov.in
- **DTE Rajasthan**: https://dte.rajasthan.gov.in
- **HTE Rajasthan**: https://hte.rajasthan.gov.in

### API Documentation
- **Groq**: https://console.groq.com/docs
- **YouTube API**: https://developers.google.com/youtube/v3
- **Telegram Bots**: https://core.telegram.org/bots

### Libraries Used
- **LangChain**: https://python.langchain.com
- **Streamlit**: https://docs.streamlit.io
- **ChromaDB**: https://docs.trychroma.com

---

## 📄 License

This project is created for educational purposes for the Department of Technical Education, Rajasthan.

---

## 🙏 Acknowledgments

- **RBSE** - For providing open educational resources
- **Groq** - For free LLM inference
- **Google** - For free translation services
- **DuckDuckGo** - For free web search
- **Open Source Community** - For amazing libraries

---

## 📞 Support

For issues or questions:
1. Check this README thoroughly
2. Verify `.env` file has correct API keys
3. Run health check: `python test_system.py`
4. Check system logs for detailed error messages

---

**Built with ❤️ for Students of Rajasthan**
**Project: YuvaSaarthi (युवासारथी) - Your Guide to Education**

**Version:** 2.0.0
**Status:** ✅ Production Ready
**Last Updated:** November 2025
**Total Cost:** ₹0/month (Completely Free!)
