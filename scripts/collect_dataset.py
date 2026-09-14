# Utility per generare sessioni simulate (test offline)
import pandas as pd
import numpy as np
import os

DATA_RAW = "../data/raw"

def generate_fake_session(session_id="test_001", frames=600):
    rows = []
    for f in range(frames):
        row = {"session_id": session_id, "frame_id": f, "timestamp_ms": f * 16}
        for i in range(33):
            row[f"lm_{i}_x"] = np.random.rand()
            row[f"lm_{i}_y"] = np.random.rand()
            row[f"lm_{i}_vis"] = 1.0
            row[f"lm_{i}_conf"] = 0.9
        row["mirror_mse"] = np.random.rand() * 0.02
        row["mpjpe"] = np.random.rand() * 0.15
        rows.append(row)
    df = pd.DataFrame(rows)
    os.makedirs(DATA_RAW, exist_ok=True)
    df.to_csv(os.path.join(DATA_RAW, f"{session_id}.csv"), index=False)

if __name__ == "__main__":
    generate_fake_session()
