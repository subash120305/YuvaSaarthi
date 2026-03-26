# YuvaSaarthi 2.0 - Presentation Cheatsheet & Documentation

## 1. Project Overview
**Title:** YuvaSaarthi 2.0 - National AI-Powered Multilingual Education Assistant
**Mission:** To democratize access to educational guidance for every Indian student, bridging the language and information gap.
**Tagline:** "Empowering Indian Students with Knowledge."

## 2. The Problem Statement
- **Language Barrier:** Most quality educational content is in English. Rural students struggle to access it.
- **Information Overload:** Students are confused by dispersed information about exams, scholarships, and careers.
- **Lack of Personal Guidance:** 1 counselor per 100,000 students in India.

## 3. The Solution: YuvaSaarthi
- A **Multilingual AI Chatbot** that speaks 23 Indian Languages.
- Acts as a personal counselor for:
  - **Exams:** JEE, NEET, UPSC, Boards.
  - **Admissions:** College processes, eligibility.
  - **Concept Learning:** Explains complex topics simply.
  - **Scholarships:** Finds financial aid.

## 4. Key Features (The "Wow" Factors)
1.  **Bharat-First Language Support:**
    - Supports **23 Official Languages** (Hindi, Kannada, Tamil, Marathi, Rajasthani, etc.).
    - Uses specialized "Bhashini" concepts (Government of India initiative emulation).
    - **Dynamic Keyboard:** Telegram bot allows instant language switching.

2.  **Hybrid RAG Architecture (Retrieval Augmented Generation):**
    - Doesn't just hallucinate; retrieves facts from a curated knowledge base (PDFs, Docs).
    - If answer is not in docs, uses LLM intelligence (Llama-3-70b).

3.  **Video Integration:**
    - "Don't just read, watch."
    - Automatically finds highly relevant **YouTube Tutorials** for concepts.
    - Filters for educational quality (excludes shorts).

4.  **Omni-Channel Availability:**
    - **Web App:** Modern, Glassmorphism UI (Next.js).
    - **Telegram Bot:** Accessible on low-end devices without installing new apps.

## 5. Technology Stack (Technical Deep Dive)
- **Frontend:** 
  - Next.js 16 (React Framework)
  - Tailwind CSS (Styling)
  - Lucide React (Icons)
  - Glassmorphism Design System

- **Backend ( The "Brain"):**
  - **FastAPI:** High-performance Python web server.
  - **LangChain:** Orchestrates the AI logic.
  - **ChromaDB:** Vector Database to store and retrieve knowledge.

- **AI & ML Models:**
  - **LLM:** Llama-3.3-70b-versatile (via Groq API) for reasoning.
  - **Embeddings:** `paraphrase-multilingual-mpnet-base-v2` (Best for Indian languages).
  - **Translation:** `deep-translator` (Google Translate API).

- **Integrations:**
  - **Telegram Bot API:** For the chat interface.
  - **YouTube Data API:** For video recommendations.

## 6. System Architecture Flow
1.  **User asks Query** (e.g., "JEE dates?" in Hindi).
2.  **Language Detection:** System identifies "Hindi".
3.  **Translation:** Translates query to English ("What are JEE dates?").
4.  **Vector Search:** ChromaDB finds the official NTA notification doc.
5.  **RAG Generation:** LLM generates answer using the doc.
6.  **Translation:** Answer translated back to Hindi.
7.  **Video Search:** Fetches "JEE Preparation" videos.
8.  **Response:** User gets Hindi text + Video Links.

## 7. Setup & Deployment (How to Run)
1.  **Prerequisites:** Python 3.9+, Node.js 18+.
2.  **Environment Variables:** `.env` file with Keys (Groq, Telegram, YouTube).
3.  **Backend:** `python3 api_server.py` (Runs on Port 8000).
4.  **Frontend:** `npm run dev` (Runs on Port 3000).
5.  **Bot:** `python3 telegram_bot.py`.

## 8. Future Roadmap
- **Voice Mode:** Speak to the bot in native dialect.
- **Image Analysis:** scan homework questions to get answers.
- **Personalized Learning Paths:** AI generates a 3-month study plan.

## 9. Conclusion
YuvaSaarthi is not just a chatbot; it's a **Digital Public Good** for India's education sector, ensuring no student is left behind due to language or geography.
