# core/state.py — auto-detects project state from filesystem + database
import os
import sqlite3
import datetime
from core.config import ROOT, DB_PATH, CHROMA_PATH


def get_built_components() -> list:
    checks = [
        ("core/voice.py",             "Voice pipeline — Whisper STT + Kokoro TTS"),
        ("core/tasks.py",             "Task manager — SQLite"),
        ("core/memory.py",            "Memory + Context Engine — event logging, patterns"),
        ("knowledge/ingestor.py",     "RAG Knowledge Engine — LlamaIndex + ChromaDB"),
        ("agents/router.py",          "LangGraph multi-agent system — 5 agents"),
        ("frontend/src/App.jsx",      "React + FastAPI premium UI"),
        ("core/proactive.py",         "Proactive intelligence — morning briefing, nudges"),
        ("core/personality.py",       "Personality engine — Hinglish, tone adaptation"),
        ("mobile/telegram_bot.py",    "Telegram bot — mobile access"),
    ]
    return [label for path, label in checks
            if os.path.exists(os.path.join(ROOT, path))]


def get_not_built() -> list:
    checks = [
        ("core/voice.py",             "Voice pipeline"),
        ("core/tasks.py",             "Task manager"),
        ("core/memory.py",            "Memory system"),
        ("knowledge/ingestor.py",     "RAG knowledge engine"),
        ("agents/router.py",          "LangGraph agents"),
        ("frontend/src/App.jsx",      "React UI"),
        ("core/proactive.py",
         "Layer 5: Proactive intelligence — morning briefing, hourly nudges, cron jobs"),
        ("core/personality.py",
         "Layer 6: Personality engine — Hinglish mode, tone adaptation, strict/chill"),
        ("mobile/telegram_bot.py",
         "Layer 7: Telegram bot — mobile access from phone"),
    ]
    return [label for path, label in checks
            if not os.path.exists(os.path.join(ROOT, path))]


def get_todays_activity() -> str:
    try:
        conn  = sqlite3.connect(DB_PATH)
        today = datetime.date.today().isoformat()
        rows  = conn.execute(
            "SELECT type, content FROM events "
            "WHERE timestamp LIKE ? ORDER BY id DESC LIMIT 30",
            (f"{today}%",)
        ).fetchall()
        conn.close()

        if not rows:
            return "No activity logged yet today."

        queries   = [c for t, c in rows if t == "query"]
        created   = [c for t, c in rows if t == "task_created"]
        completed = [c for t, c in rows if t == "task_completed"]
        voice     = [c for t, c in rows if t == "voice_used"]

        lines = [f"Today ({today}) — {len(rows)} total interactions"]
        if queries:
            lines.append(f"Questions asked ({len(queries)}): {', '.join(queries[:5])}")
        if created:
            lines.append(f"Tasks created: {', '.join(created)}")
        if completed:
            lines.append(f"Tasks completed: {', '.join(completed)}")
        if voice:
            lines.append(f"Voice conversations: {len(voice)}")
        return "\n".join(lines)

    except Exception:
        return "Activity data not available."


def get_pending_tasks() -> str:
    try:
        conn = sqlite3.connect(DB_PATH)
        rows = conn.execute(
            "SELECT task, deadline FROM tasks WHERE done=0 ORDER BY id"
        ).fetchall()
        conn.close()
        if not rows:
            return "No pending tasks."
        return "\n".join([f"- {r[0]} (due {r[1]})" for r in rows])
    except Exception:
        return "Tasks not available."


def get_full_state() -> str:
    built     = get_built_components()
    not_built = get_not_built()
    activity  = get_todays_activity()
    tasks     = get_pending_tasks()

    rag_info = "Knowledge base: not built"
    try:
        import chromadb
        client   = chromadb.PersistentClient(path=CHROMA_PATH)
        col      = client.get_or_create_collection("sameer_knowledge")
        rag_info = f"Knowledge base: {col.count()} chunks indexed"
    except Exception:
        pass

    return f"""
════════ AUTO-DETECTED PROJECT STATE ════════
(filesystem + database — always accurate, never manual)

BUILT AND WORKING ({len(built)}):
{chr(10).join(f'  + {b}' for b in built)}

NOT BUILT YET — SUGGEST ONLY THESE AS NEXT STEPS ({len(not_built)}):
{chr(10).join(f'  → {nb}' for nb in not_built)}

{rag_info}

PENDING TASKS:
{tasks}

TODAY'S ACTIVITY (auto-learned):
{activity}

STRICT RULES:
- ONLY suggest items from NOT BUILT YET as next steps
- NEVER suggest anything from BUILT AND WORKING
- Use TODAY'S ACTIVITY to personalize every response
- If asked what was done today — use the activity log above
════════════════════════════════════════════
"""
