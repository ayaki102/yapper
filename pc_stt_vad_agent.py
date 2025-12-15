import sounddevice as sd
import numpy as np
import requests
from faster_whisper import WhisperModel
import queue
import time

SERVER = "http://127.0.0.1:42069"
SAMPLE_RATE = 16000
BLOCK_SECONDS = 2  # co ile sekund robi STT

audio_q = queue.Queue()

def audio_callback(indata, frames, time_info, status):
    audio_q.put(indata.copy())

print("🔊 Ładowanie modelu Whisper...")
model = WhisperModel("small", compute_type="int8")
print("🟢 Gotowe, nasłuchuję mikrofonu")

with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=audio_callback):
    buffer = np.zeros((0, 1), dtype=np.float32)

    while True:
        buffer = np.concatenate([buffer, audio_q.get()])

        if len(buffer) >= SAMPLE_RATE * BLOCK_SECONDS:
            audio = buffer[: SAMPLE_RATE * BLOCK_SECONDS]
            buffer = buffer[SAMPLE_RATE * BLOCK_SECONDS :]

            # ---- STT ----
            segments, _ = model.transcribe(audio.flatten(), language="pl")
            text = " ".join(seg.text for seg in segments).strip()

            if text:  # tylko jeśli coś zostało rozpoznane
                print("🗣", text)
                requests.post(f"{SERVER}/send_stt", json={"text": text})

        time.sleep(0.05)

