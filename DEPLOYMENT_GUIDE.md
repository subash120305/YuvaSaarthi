# YuvaSaarthi v2 — Zero-Cost Deployment Guide

The YuvaSaarthi v2 architecture was intentionally designed to operate highly efficiently, scaling to handle a significant influx of students without requiring expensive subscription fees. We have decoupled our logic so that every element—from the intelligent vector databases to the multimodal language models and state-persistence—can run reliably at $0/month.

This document serves to explain our "Zero-Cost Architecture" and outline the best deployment strategies for hosting the application.

---

## 🏗️ The "Zero-Cost" Architecture Design

To achieve an enterprise-grade application without the enterprise price tag, we made the following architectural choices:

1. **State-of-the-Art Language Models (LLMs) via Groq Cloud API**: 
   - Instead of routing requests through expensive OpenAI (GPT-4) or Anthropic endpoints, we utilize Groq's blazing-fast Inference Engine via their Generative AI free tier.
   - We specifically leverage `llama-3.3-70b-versatile` for deep educational reasoning, inference, and text generation.
   - For our **OCR ("Point and Ask")** capability, we utilize `llama-3.2-11b-vision-preview`, ensuring image parsing remains entirely free.
   - For **Speech-To-Text (Voice Notes)**, we pipe binary audio data directly into Groq's open-source `whisper-large-v3` implementation.
2. **Local Vector Database + Retrieval-Augmented Generation (RAG)**: 
   - We avoid costly managed databases (like Pinecone) by embedding `ChromaDB` directly into the backend process, pulling documents entirely from our server's internal memory.
3. **Internal Relational Datastore**:
   - Advanced features like *Syllabus Gap Tracker* and the *Spaced Repetition Engine* rely heavily on state retention. Instead of provisioning an expensive PostgreSQL cluster, we utilize deeply integrated, fast `SQLite3` files.
4. **Text-to-Speech (TTS) Framework**:
   - Rather than paying meter-rating APIs (like ElevenLabs or AWS Polly), we harness Google's `gTTS` library which operates completely free locally.

---

## 🚀 Deployment Strategies

Because the backend relies on internal file-state databases (ChromaDB & SQLite), serverless functions (like AWS Lambda) are insufficient for the Python engine. The backend must be run as a continuous running server. 

Here are the 3 best paths to deploy the system for maximum availability at lowest/zero cost.

### Option 1: The "Always Free" Virtual Machine + Vercel (Recommended ✨)
This is the optimal setup for a production-ready pilot. It keeps all persistent databases localized while delivering massive compute capacity.

* **The Frontend** (`/frontend` Next.js App)
  * Deploy directly to **Vercel** (`vercel.com`). 
  * Vercel's Hobby Tier allows generous bandwidth and lightning-fast edge rendering at **$0/month**.
* **The Backend** (`api_server.py` & `telegram_bot.py`)
  * Register for the **Oracle Cloud "Always Free" Tier**. Oracle uniquely provides up to 4 ARM Ampere A1 Compute instances with an incredible **24GB of RAM** and 200GB block storage at **$0/month, forever**.
  * *(Alternative)*: Google Cloud offers a strictly free `e2-micro` instance.
  * *Setup Guide*: Spin up the Ubuntu instance. Clone your repository. Install dependencies. Simply use a process manager like `pm2` or `tmux` to run both the FastAPI server (`api_server.py`) and the polling script (`telegram_bot.py`). Your entire backend will remain awake 24/7.

### Option 2: Render & Railway (PaaS Approach)
If managing a Linux server manually is not feasible, Platform-as-a-Service (PaaS) providers easily abstract the infrastructure via Docker and GitHub pipelines.

* **The Backend Server** (`api_server.py`):
   * Deploy as a **Web Service** on **Render.com**. Render offers a completely free tier. The tradeoff is cold-starts: the server will spin down after 15 minutes of inactivity, adding a ~40-second delay on the very first student query of the day.
* **The Telegram Bot** (`telegram_bot.py`):
   * Deploy as a **Background Worker**. Because Telegram operates via polling loops instead of incoming network HTTP requests, you can deploy the bot to Render (as a background process) or to **Railway.app** using their monthly developer trial limits. 
* *Estimated Cost: $0/month (with noticeable wake-up delays).*

### Option 3: Localhost Tunneling (Best for Demos & Testing)
If the primary goal is a controlled beta test or an investor/faculty presentation, deploying to the cloud is entirely optional.

* Run the frontend, backend, and Telegram bot concurrently on your local machine.
* Use **Cloudflare Tunnels** (which are 100% free and enterprise-grade) or **ngrok** to expose your local `8000` FastAPI port to a public HTTPS URL.
* Point your local Next.js frontend and Telegram Webhook to the Cloudflare URL.
* *Benefit:* You bypass all deployment complexities, utilizing your computer's high-performance CPU until you reliably hit 100+ daily active users. 
* *Estimated Cost: $0*

---
## Summary Dashboard

| Component | Provider Used | Usual Managed Cost | Our Architecture Cost |
| --- | --- | --- | --- |
| **Brain / LLM Base** | Groq API Free Tier | ~$30.00/mo | **$0.00** |
| **Speech-To-Text** | Groq API Whisper Free | ~$15.00/mo | **$0.00** |
| **Multimodal OCR** | Groq API Vision | ~$20.00/mo | **$0.00** |
| **Vector Database** | Local ChromaDB | ~$70.00/mo | **$0.00** |
| **SQL Database** | Local SQLite3 | ~$15.00/mo | **$0.00** |
| **Frontend Hosting** | Vercel Hobby Tier | ~$20.00/mo | **$0.00** |
| **Server Hosting (Prod)** | Oracle Cloud Always Free | ~$15.00/mo | **$0.00** |
| **Total Pilot Expenditure** | | | **$0.00/month** |
