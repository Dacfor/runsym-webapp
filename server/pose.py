import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, enable_segmentation=False, model_complexity=1)

# Mappatura indici landmark (MediaPipe Pose 33)
LANDMARK_NAMES = [
    "nose","left_eye_inner","left_eye","left_eye_outer","right_eye_inner","right_eye","right_eye_outer",
    "left_ear","right_ear","mouth_left","mouth_right",
    "left_shoulder","right_shoulder","left_elbow","right_elbow","left_wrist","right_wrist",
    "left_pinky","right_pinky","left_index","right_index","left_thumb","right_thumb",
    "left_hip","right_hip","left_knee","right_knee","left_ankle","right_ankle",
    "left_heel","right_heel","left_foot_index","right_foot_index"
]

IDX = {
    "left_shoulder": 11, "right_shoulder": 12,
    "left_elbow": 13, "right_elbow": 14,
    "left_wrist": 15, "right_wrist": 16,
    "left_hip": 23, "right_hip": 24,
    "left_knee": 25, "right_knee": 26,
    "left_ankle": 27, "right_ankle": 28,
}

PAIRS = [
    ("left_shoulder", "right_shoulder"),
    ("left_elbow", "right_elbow"),
    ("left_wrist", "right_wrist"),
    ("left_hip", "right_hip"),
    ("left_knee", "right_knee"),
    ("left_ankle", "right_ankle"),
]

def estimate_pose(frame_bgr):
    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    res = pose.process(rgb)
    if res.pose_landmarks is None:
        return None
    lm = res.pose_landmarks.landmark
    out = []
    for p in lm:
        # MediaPipe fornisce x,y normalized; vis/conf non diretti → usiamo visibility come proxy
        out.append([p.x, p.y, p.visibility, p.visibility])
    return np.array(out)  # 33 x 4
