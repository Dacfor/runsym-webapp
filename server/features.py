import numpy as np
from pose import PAIRS, IDX

def compute_mirror_mse(landmarks):
    # landmarks: 33 x 4 (x,y,vis,conf)
    mse_sum = 0.0
    count = 0
    for nameL, nameR in PAIRS:
        iL, iR = IDX[nameL], IDX[nameR]
        xL, yL = landmarks[iL, 0], landmarks[iL, 1]
        xR, yR = landmarks[iR, 0], landmarks[iR, 1]
        xR_mirror = 1.0 - xR
        err = (xL - xR_mirror)**2 + (yL - yR)**2
        mse_sum += err
        count += 1
    return mse_sum / count if count > 0 else 0.0

def compute_mpjpe(landmarks):
    dist_sum = 0.0
    count = 0
    for nameL, nameR in PAIRS:
        iL, iR = IDX[nameL], IDX[nameR]
        xL, yL = landmarks[iL, 0], landmarks[iL, 1]
        xR, yR = landmarks[iR, 0], landmarks[iR, 1]
        xR_mirror = 1.0 - xR
        d = np.sqrt((xL - xR_mirror)**2 + (yL - yR)**2)
        dist_sum += d
        count += 1
    return dist_sum / count if count > 0 else 0.0

def compute_cadence(signal_y, fs):
    from scipy.signal import stft
    if len(signal_y) < 256:
        return np.nan
    f, t, Zxx = stft(signal_y, fs=fs, nperseg=256)
    power = np.abs(Zxx).mean(axis=1)
    peak_f = f[np.argmax(power)]
    return peak_f * 60.0  # spm

def compute_plv(phiL, phiR):
    diff = np.exp(1j * (phiL - phiR))
    return np.abs(np.mean(diff))

def compute_phase_delay(signalL, signalR, fs):
    from scipy.signal import correlate
    if len(signalL) < 10 or len(signalR) < 10:
        return np.nan
    corr = correlate(signalL - signalL.mean(), signalR - signalR.mean(), mode="full")
    lag = np.argmax(corr) - (len(signalL) - 1)
    return (lag / fs) * 1000.0  # ms

def detect_strides(ankle_y_seq, fs):
    # Rileva stride da picchi di ankle_y (semplice euristica)
    from scipy.signal import find_peaks
    # Inverti segnale: picchi quando ankle è più alto (fase di swing)
    signal = -ankle_y_seq
    peaks, _ = find_peaks(signal, distance=int(fs*0.3))
    return peaks
