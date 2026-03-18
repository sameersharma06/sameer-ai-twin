# app.py — SAMEER AI TWIN — fully updated
import streamlit as st
import datetime
from agents.router import run_agents
from core.tasks import get_tasks, add_task, mark_done
from core.brain import get_response
from core.voice import record_audio, transcribe, speak
from core.memory import log_event, generate_daily_summary, detect_patterns

st.set_page_config(page_title="SAMEER AI TWIN", layout="wide", page_icon="🧠")
st.title("🧠 SAMEER AI TWIN")
st.caption("Personal AI OS · 100% Local · Apple Silicon · v2 — Memory + Context Engine")

col1, col2, col3 = st.columns([2, 1.5, 1.5])

with col1:
    st.subheader("📅 Today's Tasks")
    tasks = get_tasks()
    if not tasks:
        st.info("No tasks yet. Add one below.")
    to_complete = []
    for task_id, task_text, deadline in tasks:
        if st.checkbox(f"{task_text}  —  {deadline}", key=f"t_{task_id}"):
            to_complete.append(task_id)

    if st.button("✅ Mark Done") and to_complete:
        for tid in to_complete:
            mark_done(tid)
            log_event("task_completed", f"task id {tid}")
        st.rerun()

    new_task = st.text_input("New task")
    deadline = st.date_input("Deadline", value=datetime.date.today())
    if st.button("➕ Add") and new_task:
        add_task(new_task, deadline.strftime("%d %b"))
        log_event("task_created", new_task)
        st.rerun()

with col2:
    st.subheader("🎤 Voice Mode")
    st.caption("Press the big button below to start")

with col3:
    st.subheader("💡 Daily Insight")
    if st.button("Get insight"):
        tasks_text = "\n".join([f"- {t[1]} (due {t[2]})" for t in get_tasks()])
        with st.spinner("Thinking..."):
            insight = get_response(
                "Give me one short powerful tip based on my tasks and recent activity.",
                tasks_text
            )
        st.success(insight)

    st.subheader("🧠 Memory")
    if st.button("Show patterns"):
        patterns = detect_patterns()
        if patterns:
            for p in patterns:
                st.info(p)
        else:
            st.info("Use the app for a few days to detect patterns.")

    if st.button("End of day summary"):
        summary = generate_daily_summary()
        st.success(summary)

st.divider()

if st.button("🎙️ Start Voice Conversation (5 sec)", type="primary", use_container_width=True):
    try:
        with st.spinner("🎤 Listening... speak now"):
            audio_path = record_audio()

        with st.spinner("Transcribing..."):
            user_said = transcribe(audio_path)

        st.success(f"You said: **{user_said}**")
        log_event("voice_used", user_said[:100])

        # Always fresh from database
        tasks_text = "\n".join([f"- {t[1]} (due {t[2]})" for t in get_tasks()])

        # Detect task questions — answer directly from DB, skip LLM
        task_trigger_words = [
            "my tasks", "all tasks", "what tasks", "list tasks",
            "show tasks", "pending tasks", "today's tasks",
            "what are my", "tell me my tasks", "mere tasks",
            "tasks batao", "kya tasks", "all my tasks"
        ]
        user_lower = user_said.lower()

        if any(trigger in user_lower for trigger in task_trigger_words):
            all_tasks = get_tasks()
            if not all_tasks:
                reply = "You have no pending tasks right now."
            else:
                task_lines = ", ".join([f"{t[1]}" for t in all_tasks])
                reply = f"You have {len(all_tasks)} tasks: {task_lines}."
        else:
            with st.spinner("🧠 Thinking..."):
                reply = get_response(user_said, tasks_text, voice_mode=True)

        st.write("**Sameer AI:**", reply)

        with st.spinner("🔊 Speaking..."):
            audio_out = speak(reply)

        st.audio(audio_out, format="audio/wav", autoplay=True)

    except RuntimeError as e:
        st.error(str(e))
    except ValueError as e:
        st.warning(str(e))

st.divider()

user_text = st.text_input("Or type here...")
if user_text:
    # Always fresh from database
    tasks_text = "\n".join([f"- {t[1]} (due {t[2]})" for t in get_tasks()])
    with st.spinner("Thinking..."):
        reply, agent_used = run_agents(user_text, tasks_text)
    st.caption(f"Agent: {agent_used}")
    st.write("**Sameer AI:**", reply)

    