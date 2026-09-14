from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import cv2
import numpy as np
import base64
from pose import estimate_pose
from filter import smooth_landmarks
from features import compute_mirror_mse, compute_mpjpe
from export import save_frame_csv, save_session_metadata

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

session_store = {}

def decode_b64_image(b64_str):
    img_bytes = base64.b64decode(b64_str)
    nparr = np.frombuffer(img_bytes, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

@socketio.on("frame")
def handle_frame(data):
    # data: {frame_id, timestamp_ms, image_b64, session_id}
    session_id = data.get("session_id", "default")
    if session_id not in session_store:
        session_store[session_id] = {"frames": [], "landmarks_seq": [], "timestamps": []}
    sess = session_store[session_id]

    img = decode_b64_image(data["image_b64"])
    landmarks = estimate_pose(img)  # 33 x 4 or None
    if landmarks is None:
        emit("metrics", {"mirror_mse": None, "mpjpe": None, "error": "no_pose"})
        return

    # smoothing sequenziale (richiede sequenza; qui semplificato per-frame)
    sess["landmarks_seq"].append(landmarks)
    sess["timestamps"].append(data["timestamp_ms"])
    sess["frames"].append(img)

    # Per MVP: calcolo per-frame senza filtro temporale completo
    metrics = {
        "mirror_mse": float(compute_mirror_mse(landmarks)),
        "mpjpe": float(compute_mpjpe(landmarks)),
    }
    save_frame_csv(session_id, data["frame_id"], data["timestamp_ms"], landmarks, metrics)
    emit("metrics", metrics)

@socketio.on("start_session")
def start_session(data):
    # data: {session_id, cam_view, fps, width, height}
    session_id = data["session_id"]
    session_store[session_id] = {"frames": [], "landmarks_seq": [], "timestamps": [], "meta": data}
    save_session_metadata(session_id, data)
    emit("session_started", {"status": "ok", "session_id": session_id})

@socketio.on("end_session")
def end_session(data):
    session_id = data["session_id"]
    # Qui si calcoleranno batch metrics (cadence, PLV, phase_delay) su finestra
    # Per MVP: segna sessione chiusa
    emit("session_ended", {"status": "ok", "session_id": session_id})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
