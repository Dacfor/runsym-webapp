const video = document.getElementById('video');
const canvas = document.getElementById('overlay');
const ctx = canvas.getContext('2d');
const socket = io(window.location.origin);

let streaming = false;
let sessionId = "session_" + Date.now();
let frameCount = 0;

document.getElementById('startBtn').addEventListener('click', async () => {
  document.getElementById('wizard').style.display = 'none';
  const stream = await navigator.mediaDevices.getUserMedia({
    video: { width: { ideal: 1280 }, height: { ideal: 720 }, frameRate: { ideal: 60 } },
    audio: false
  });
  video.srcObject = stream;
  await new Promise((resolve) => {
    video.onloadedmetadata = () => resolve();
  });
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;

  socket.emit("start_session", {
    session_id: sessionId,
    cam_view: "back",
    fps: 60,
    width: canvas.width,
    height: canvas.height
  });

  streaming = true;
  requestAnimationFrame(sendFrames);
});

function sendFrames() {
  if (!streaming) return;
  const frame = captureFrame(video);
  const b64 = frame.toDataURL('image/jpeg', 0.8).split(',')[1];
  socket.emit("frame", {
    frame_id: frameCount++,
    timestamp_ms: Date.now(),
    image_b64: b64,
    session_id: sessionId
  });
  requestAnimationFrame(sendFrames);
}

function captureFrame(video) {
  const c = document.createElement('canvas');
  c.width = video.videoWidth;
  c.height = video.videoHeight;
  const cx = c.getContext('2d');
  cx.drawImage(video, 0, 0);
  return c;
}

socket.on("session_started", (data) => {
  console.log("Session started:", data);
});

socket.on("metrics", (m) => {
  if (m.mirror_mse !== null && m.mirror_mse !== undefined) {
    document.getElementById('mse').textContent = m.mirror_mse.toFixed(4);
  }
  if (m.mpjpe !== null && m.mpjpe !== undefined) {
    document.getElementById('mpjpe').textContent = m.mpjpe.toFixed(4);
  }
});

// Overlay scheletro ( MVP: punti joint )
socket.on("pose_overlay", (data) => {
  // data: landmarks 33 x 4
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const r = 3;
  for (let i = 0; i < 33; i++) {
    const x = data[i][0] * canvas.width;
    const y = data[i][1] * canvas.height;
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fillStyle = (i % 2 === 0) ? "#3b82f6" : "#ef4444";
    ctx.fill();
  }
});
