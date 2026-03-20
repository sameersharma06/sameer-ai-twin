# core/config.py
import os

ROOT        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR    = os.path.join(ROOT, "data")
DB_PATH     = os.path.join(ROOT, "data", "sameer_ai.db")
CHROMA_PATH = os.path.join(ROOT, "data", "chroma_db")
NOTES_PATH  = os.path.expanduser("~/Notes")
AUDIO_IN    = os.path.join(ROOT, "data", "temp_input.wav")
AUDIO_OUT   = os.path.join(ROOT, "data", "temp_reply.wav")

os.makedirs(DATA_DIR, exist_ok=True)
