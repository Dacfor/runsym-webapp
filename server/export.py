import pandas as pd
import os
from datetime import datetime

DATA_DIR = "../data"
FRAMES_CSV = os.path.join(DATA_DIR, "processed", "frames.csv")
SESSIONS_CSV = os.path.join(DATA_DIR, "processed", "sessions.csv")
STRIDES_CSV = os.path.join(DATA_DIR, "processed", "strides.csv")

def ensure_dirs():
    os.makedirs(os.path.dirname(FRAMES_CSV), exist_ok=True)
    os.makedirs(os.path.dirname(SESSIONS_CSV), exist_ok=True)
    os.makedirs(os.path.dirname(STRIDES_CSV), exist_ok=True)

def save_session_metadata(session_id, meta):
    ensure_dirs()
    row = {
        "session_id": session_id,
        "created_at": datetime.utcnow().isoformat(),
        "cam_view": meta.get("cam_view", "unknown"),
        "fps": meta.get("fps", 60),
        "width": meta.get("width", 1280),
        "height": meta.get("height", 720),
    }
    df = pd.DataFrame([row])
    if not os.path.exists(SESSIONS_CSV):
        df.to_csv(SESSIONS_CSV, index=False)
    else:
        df.to_csv(SESSIONS_CSV, mode="a", header=False, index=False)

def save_frame_csv(session_id, frame_id, timestamp_ms, landmarks, metrics):
    ensure_dirs()
    row = {
        "session_id": session_id,
        "frame_id": frame_id,
        "timestamp_ms": timestamp_ms,
        "mirror_mse": metrics.get("mirror_mse"),
        "mpjpe": metrics.get("mpjpe"),
    }
    # espandi landmark in colonne
    for i in range(landmarks.shape[0]):
        row[f"lm_{i}_x"] = landmarks[i, 0]
        row[f"lm_{i}_y"] = landmarks[i, 1]
        row[f"lm_{i}_vis"] = landmarks[i, 2]
        row[f"lm_{i}_conf"] = landmarks[i, 3]
    df = pd.DataFrame([row])
    if not os.path.exists(FRAMES_CSV):
        df.to_csv(FRAMES_CSV, index=False)
    else:
        df.to_csv(FRAMES_CSV, mode="a", header=False, index=False)

def save_strides_csv(strides):
    ensure_dirs()
    df = pd.DataFrame(strides)
    if not os.path.exists(STRIDES_CSV):
        df.to_csv(STRIDES_CSV, index=False)
    else:
        df.to_csv(STRIDES_CSV, mode="a", header=False, index=False)
