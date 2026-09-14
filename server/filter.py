import numpy as np
from scipy.signal import butter, filtfilt

def butter_lowpass(cutoff, fs, order=4):
    nyq = 0.5 * fs
    normal = cutoff / nyq
    b, a = butter(order, normal, btype='low', analog=False)
    return b, a

def smooth_landmarks_seq(landmarks_seq, cutoff=8.0, fs=60.0):
    # landmarks_seq: T x 33 x 4
    if len(landmarks_seq) == 0:
        return np.array(landmarks_seq)
    landmarks_seq = np.array(landmarks_seq)
    b, a = butter_lowpass(cutoff, fs)
    smoothed = np.zeros_like(landmarks_seq)
    for k in range(landmarks_seq.shape[1]):
        for dim in range(2):  # x,y
            smoothed[:, k, dim] = filtfilt(b, a, landmarks_seq[:, k, dim])
        smoothed[:, k, 2:] = landmarks_seq[:, k, 2:]  # vis,conf
    return smoothed
