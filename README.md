> ⚠️ This project has moved. The new and improved version is [Zeno](https://github.com/sameersharma06/zeno) — cleaner architecture, better product, actively maintained.

---

# 🧠 SAMEER AI TWIN — Personal AI Operating System

![Local](https://img.shields.io/badge/100%25_Local-brightgreen)
![Apple Silicon](https://img.shields.io/badge/Apple_Silicon-black)
![Voice](https://img.shields.io/badge/Voice_Enabled-orange)
![Agents](https://img.shields.io/badge/LangGraph_Agents-5-purple)
![Status](https://img.shields.io/badge/Status-Active_Development-blue)
![Built in India](https://img.shields.io/badge/Built_in-Haryana_India-ff69b4)
![Stars](https://img.shields.io/github/stars/sameersharma06/sameer-ai-twin?style=social)

> **The most advanced personal AI OS built on Apple Silicon.**
> Voice + Memory + RAG + 5 Agents + Local LLM.
> No cloud. No subscriptions. No data leaving your machine.
> Built by one person in Haryana, India.

---

## Demo

> 🎬 Demo video coming soon — follow to get notified

---

## What makes this different

Every AI tool today requires internet, charges monthly, and sends your
data to servers you don't control.

SAMEER AI TWIN runs entirely on your MacBook. Every conversation,
every task, every memory — stays on your machine. Forever.

This is not a chatbot wrapper. This is a personal AI operating system
with memory, knowledge, agents, and voice — built from scratch.

---

## What it does (v1 — March 2026)

### 🎤 Voice Pipeline
Speak naturally → Whisper transcribes → AI thinks → Kokoro speaks back.
Full offline voice conversation. No internet. No API calls.

### 🧠 Dual Model Brain
- Qwen2.5-7B for text responses (15 seconds)
- Qwen2.5-3B for voice responses (8 seconds)
- Decision engine with 4 modes: assistant, strategist, coach, analyst

### 📅 Task Intelligence
- SQLite-backed task manager with deadlines
- Voice task listing — "what are my tasks?" reads directly from database
- Pattern detection — knows your most active hour and work preferences

### 🧠 Memory + Context Engine
- Logs every interaction — queries, tasks, voice sessions
- Builds daily activity summary automatically
- Detects behavioral patterns over time
- AI knows what you did today without being told

### 📚 RAG Knowledge Engine
- Answers from your own notes, PDFs, and documents
- Fully local embeddings — no OpenAI, no internet
- Similarity threshold — never hallucinates missing knowledge
- Add any file to ~/Notes → AI instantly knows it

### 🤖 5-Agent LangGraph System
| Agent | What it does |
|-------|-------------|
| TaskAgent | Manages SQLite tasks via natural language |
| ResearchAgent | Queries your notes, falls back to LLM |
| CodingAgent | Writes code for your exact stack |
| AutomationAgent | Opens 30+ Mac apps via voice |
| Brain | Planning, strategy, decision making |

### 🖥️ Mac Automation
Open any app by voice. 30+ aliases supported.
"Open VS Code", "Open Brave", "Open Spotify" — all work.

---

## Roadmap (building live — follow for updates)

| Phase | Feature | Status |
|-------|---------|--------|
| v1 | Voice + Brain + Tasks + Dashboard + 5 Agents | ✅ Complete |
| v2 | RAG Knowledge Engine — LlamaIndex + ChromaDB | ✅ Complete |
| v3 | LangGraph Multi-Agent System | ✅ Complete |
| v4 | Coming soon | 🔨 Building |

---

## Tech stack

| Layer | Technology |
|-------|-----------|
| LLM (text) | Qwen2.5-7B-Instruct-4bit via mlx_lm |
| LLM (voice) | Qwen2.5-3B-Instruct-4bit via mlx_lm |
| Speech to text | whisper-large-v3-turbo via mlx-audio |
| Text to speech | Kokoro-82M-bf16 via mlx-audio |
| Knowledge / RAG | LlamaIndex v0.10+ + ChromaDB |
| Embeddings | BAAI/bge-small-en-v1.5 (fully local) |
| Agents | LangGraph StateGraph |
| UI | Streamlit |
| Storage | SQLite |
| Hardware | Apple Silicon M-series (MLX native) |

---

## Run it yourself

**Requirements:** Mac with Apple Silicon (M1/M2/M3/M4) · 16 GB RAM minimum
```bash
git clone https://github.com/sameersharma06/sameer-ai-twin
cd sameer-ai-twin
pip install -r requirements.txt
streamlit run app.py
```

First run downloads ~6 GB of models once. Fully offline after that.
No API keys. No accounts. No internet required after setup.

---

## Add your own knowledge
```bash
# Drop any .txt .md .pdf into ~/Notes
cp your_notes.md ~/Notes/

# Rebuild the index — takes 30 seconds
python knowledge/ingestor.py

# Your AI now knows everything in those files
```

---

## Architecture
```
User Input (voice or text)
        ↓
   Router (LangGraph)
        ↓
┌───────────────────────┐
│  TaskAgent            │ → SQLite database
│  ResearchAgent        │ → ~/Notes (ChromaDB)
│  CodingAgent          │ → LLM (7B)
│  AutomationAgent      │ → Mac (subprocess)
│  Brain                │ → LLM (7B) + context
└───────────────────────┘
        ↓
   Memory Logger → SQLite events table
        ↓
   Response → Text + Voice (Kokoro TTS)
```

---

## Sponsorship

This project is built and maintained by one student in Haryana, India.

If SAMEER AI TWIN helped you or you want to support local AI development:

**Sponsor this project:**
- GitHub Sponsors — coming soon
- for sponser [sameersharmaa95@gmail.com]

**For companies:**
If your company builds AI tools, developer tools, or Apple Silicon products
and wants to be featured in this README — reach out.

Contact: [sameersharmaa95@gmail.com] · [https://www.linkedin.com/in/sameersharma0028/]

**What sponsors get:**
- Logo in README (seen by every developer who finds this)
- Mention in every LinkedIn/Twitter update
- Early access to Pro features
- Direct feedback channel

---

## Contributing

This is an open-source personal AI project. Contributions welcome.

Areas where help is needed:
- Windows/Linux port (currently Mac only)
- Better embedding models for Indian languages
- Voice model improvements
- UI enhancements

Open an issue or PR — all contributions acknowledged.

---

## Pro Version (coming soon)

The public repo contains the core open-source system.

Interested in early access? [sameersharmaa95@gmail.com]

---

## Open to Opportunities

I am a solo AI builder from Haryana, India actively looking for:

- AI/ML Engineering Internship (remote or Delhi-NCR)
- Research Internship (AI, LLM, Agents)
- Part-time AI consulting
- Open source collaboration

**What I bring:**
- Built a full local AI OS from scratch — voice, memory, RAG, agents
- Deep hands-on experience with MLX, LangGraph, LlamaIndex, Whisper, TTS
- Apple Silicon ML stack (rare skill in India)
- Ships fast, builds in public, learns daily

**Stack I work with:**
Python · MLX · LangGraph · LlamaIndex · ChromaDB · Streamlit · SQLite · 
Whisper · Kokoro TTS · Qwen2.5 · Apple Silicon

**If you are building AI products and need someone who:**
- Understands local LLM deployment
- Can build multi-agent systems
- Moves fast and ships working code

→ Reach out directly:

📧 Email: [sameersharmaa95@gmail.com]
💼 LinkedIn: [https://www.linkedin.com/in/sameersharma0028/]
🐦 Twitter/X: [sameersharma28_]
📍 Location: Haryana, India · Open to remote globally · Available for in-office roles

---

*Star ⭐ this repo if you want your own personal AI OS.*
*Follow for weekly updates as I build this live.*


