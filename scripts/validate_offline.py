# Confronta metriche automatiche con misure manuali (es. cadence contato a mano)
import pandas as pd
import numpy as np

DATA_PROCESSED = "../data/processed"

def load_frames(path):
    return pd.read_csv(path)

def cadence_from_peaks(y_signal, fs):
    from scipy.signal import find_peaks
    if len(y_signal) < 10:
        return np.nan
    peaks, _ = find_peaks(y_signal, distance=int(fs*0.3))
    if len(peaks) < 2:
        return np.nan
    steps = len(peaks) - 1
    duration_s = (peaks[-1] - peaks[0]) / fs
    return (steps / duration_s) * 60.0

if __name__ == "__main__":
    df = load_frames(f"{DATA_PROCESSED}/frames.csv")
    # Esempio: estrai y ankle (indice 27/28) e stima cadence
    # Qui andrebbe implementata logica di segmentazione stride e confronto con ground truth
    print("Dataset caricato. Implementa logica di validazione specifica.")
