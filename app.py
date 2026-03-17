import streamlit as st
import datetime
from core.tasks import get_tasks, add_task, mark_done
from core.brain import get_response
from core.voice import record_audio, transcribe, speak

st.set_page_config(page_title="SAMEER AI TWIN", layout="wide", page_icon="🧠")
st.title("🧠 SAMEER AI TWIN")
st.caption("Personal AI OS · 100% Local · Apple Silicon · v1")

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
        st.rerun()
    new_task = st.text_input("New task")
    deadline = st.date_input("Deadline", value=datetime.date.today())
    if st.button("➕ Add") and new_task:
        add_task(new_task, deadline.strftime("%d %b"))
        st.rerun()

with col2:
    st.subheader("🎤 Voice Mode")
    st.caption("Press the big button below to start")

with col3:
    st.subheader("💡 Daily Insight")
    if st.button("Get insight"):
        tasks_text = "\n".join([f"- {t[1]} ({t[2]})" for t in get_tasks()])
        with st.spinner("Thinking..."):
            insight = get_response(
                "Give me one short powerful tip for today based on my tasks.",
                tasks_text
            )
        st.success(insight)

st.divider()

if st.button("🎙️ Start Voice Conversation (8 sec)", type="primary", use_container_width=True):
    try:
        with st.spinner("🎤 Listening... speak now"):
            audio_path = record_audio()
        with st.spinner("Transcribing..."):
            user_said = transcribe(audio_path)
        st.success(f"You said: **{user_said}**")
        tasks_text = "\n".join([f"- {t[1]} ({t[2]})" for t in get_tasks()])
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
    tasks_text = "\n".join([f"- {t[1]} ({t[2]})" for t in get_tasks()])
    with st.spinner("Thinking..."):
        reply = get_response(user_text, tasks_text)
    st.write("**Sameer AI:**", reply)
