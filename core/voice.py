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

    # Catch empty transcription
    if not text:
        raise ValueError("No speech detected. Please speak clearly and try again.")

    # Catch Whisper hallucinations — repeated words or nonsense
    words = text.split()
    if len(words) > 3:
        unique_words = set(w.lower() for w in words)
        # If less than 20% unique words — it's hallucinating
        if len(unique_words) / len(words) < 0.2:
            raise ValueError("No clear speech detected. Please speak clearly and try again.")

    # Catch known Whisper hallucination phrases
    hallucination_phrases = [
        "www.", "fema.gov", "thank you for watching",
        "please subscribe", "visit our website",
        "for more information"
    ]
    text_lower = text.lower()
    if any(phrase in text_lower for phrase in hallucination_phrases):
        raise ValueError("No clear speech detected. Please speak clearly and try again.")

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