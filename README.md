# RunSym WebApp

Web-app per analisi simmetria nella corsa con MediaPipe Pose, Mirror-MSE, MPJPE, cadence, PLV e phase delay.

## Caratteristiche
- Streaming video da mobile (browser) a server Python via WebSocket
- Estrazione pose 33-keypoint (MediaPipe)
- Metriche di simmetria: Mirror-MSE, MPJPE (per-frame)
- Batch metrics: cadence (STFT), PLV (Hilbert), phase delay (cross-corr)
- Export CSV (gold standard) e report per-stride
- Dashboard web con overlay scheletro (left=blu, right=rosso) e indicatori

## Setup
1. Clona la repo: `git clone https://github.com/Dacfor/runsym-webapp`
2. Installa dipendenze server: `cd runsym-webapp/server && pip install -r requirements.txt`
3. Avvia server: `python main.py`
4. Apri `web/index.html` in browser mobile (stessa LAN) puntando a `http://<IP-PC>:5000`

## Uso mobile
- Inquadratura: back view o front view, telefono a altezza anca, 2–4 m di distanza
- Setup: 60–120 fps, luce uniforme, corpo intero in frame, abiti aderenti
- Avvia sessione dal wizard; il browser streamma i frame al server
- Metriche real-time: Mirror-MSE, MPJPE; a fine sessione: cadence, PLV, phase delay

## Validazione
- Dataset locale: usa `scripts/collect_dataset.py` per generare sessioni simulate
- Confronta metriche automatiche con misure manuali (cadence contato a mano, step width/length)
- Calibra soglie (z-score > 1.5 per 3+ stride) e pesi score composito

## Roadmap
- Overlay scheletro completo in `app.js`
- Batch metrics (cadence/PLV/phase_delay) a fine sessione
- UX "Guided" (wizard avanzato, 3 indicatori: simmetria, cadence, overstriding)
- Integrazione YOLO-pose (Roboflow) come alternativa a MediaPipe

## Licenza
MIT
