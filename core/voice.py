import sounddevice as sd
import soundfile as sf
import numpy as np
import os
import streamlit as st
from mlx_audio.stt.generate import generate_transcription
from mlx_audio.tts.utils import load_model

@st.cache_resource
def _load_tts():
    return load_model("mlx-community/Kokoro-82M-bf16")

def record_audio(duration: int = 8, fs: int = 16000) -> str:
    os.makedirs("data", exist_ok=True)
    path = "data/temp_input.wav"
    try:
        audio = sd.rec(
            int(duration * fs), samplerate=fs, channels=1, dtype="float32"
        )
        sd.wait()
        sf.write(path, audio, fs)
        return path
    except Exception as e:
        raise RuntimeError(
            f"Mic error: {e}\n"
            "Fix: System Preferences → Privacy → Microphone → allow Terminal"
        )

def transcribe(audio_path: str) -> str:
    result = generate_transcription(
        model="mlx-community/whisper-large-v3-turbo-asr-fp16",
        audio=audio_path
    )
    text = result.text.strip()
    if not text:
        raise ValueError("No speech detected. Speak louder and try again.")
    return text

def speak(text: str) -> str:
    os.makedirs("data", exist_ok=True)
    output_path = "data/temp_reply.wav"
    tts = _load_tts()
    chunks = []
    for result in tts.generate(text=text, voice="af_heart", speed=1.0, lang_code="a"):
        chunks.append(np.array(result.audio).astype(np.float32))
    full = np.concatenate(chunks) if len(chunks) > 1 else chunks[0]
    sf.write(output_path, full, 24000)
    return output_path