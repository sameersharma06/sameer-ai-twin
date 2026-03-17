cat > README.md << 'EOF'
# 🧠 SAMEER AI TWIN — Personal AI Operating System

![Local](https://img.shields.io/badge/100%25_Local-brightgreen)
![Apple Silicon](https://img.shields.io/badge/Apple_Silicon-black)
![Voice](https://img.shields.io/badge/Voice_Enabled-orange)
![Status](https://img.shields.io/badge/Status-Active-blue)
![Built in India](https://img.shields.io/badge/Built_in-Haryana_India-ff69b4)

> A personal AI that knows me better than any app.
> Not a chatbot. A digital twin that manages my tasks,
> answers from my own notes, and talks back in voice.
> 100% private. 100% offline. Runs on my MacBook.

---

## Demo

> Recording demo video — coming soon

---

## What it does today (v1 · March 2026)

- Voice conversation — speak naturally, get instant voice reply, fully offline
- Smart task manager with deadlines backed by SQLite
- Life dashboard — tasks, insights, daily analytics
- AI brain with decision engine, execution coaching, and strategy modes
- Proactive daily insight button

## Full roadmap (building live)

| Phase | Feature | Status |
|-------|---------|--------|
| v1 | Voice + Tasks + Dashboard + Brain | ✅ Live |
| v2 | RAG — answers from my own notes and PDFs | 🔨 Building |
| v3 | LangGraph agents — Research, Coding, Automation | 📋 Planned |
| v4 | Proactive twin — hourly nudges, Mac automation | 📋 Planned |
| v5 | Always-listening + Vision + Telegram mobile | 📋 Planned |

## Tech stack

| Layer | Tech |
|-------|------|
| LLM | Qwen2.5-14B via MLX (Apple Silicon, 4-bit) |
| Speech to text | mlx-whisper (whisper-large-v3-turbo) |
| Text to speech | Kokoro-82M via mlx-audio |
| UI | Streamlit |
| Storage | SQLite |
| Knowledge (v2) | LlamaIndex v0.10+ + ChromaDB |
| Agents (v3) | LangGraph |

## Run it yourself

Requirements: Mac with Apple Silicon (M1/M2/M3/M4), 16 GB RAM minimum.
```bash
git clone https://github.com/sameersharma06/sameer-ai-twin
cd sameer-ai-twin
pip install -r requirements.txt
streamlit run app.py
```

First run downloads ~8 GB of models once. After that, fully offline.

## Why this exists

Most AI tools need internet, charge monthly, and send your data to servers.
This runs entirely on my MacBook. Every conversation, every task, every memory
stays on my machine. Private by design. Mine completely.

---

Built by Sameer · Haryana, India · Open to AI/ML internships (remote or Delhi-NCR)
EOF