from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import os

app = FastAPI()

# --- API ---
tts_queue: List[str] = []
stt_queue: List[str] = []

class Msg(BaseModel):
    text: str

@app.post("/send_tts")
def send_tts(msg: Msg):
    tts_queue.append(msg.text)
    return {"ok": True}

@app.get("/get_tts")
def get_tts():
    if not tts_queue:
        return {"text": None}
    return {"text": tts_queue.pop(0)}

@app.post("/send_stt")
def send_stt(msg: Msg):
    stt_queue.append(msg.text)
    return {"ok": True}

@app.get("/get_stt")
def get_stt():
    if not stt_queue:
        return {"text": None}
    return {"text": stt_queue.pop(0)}

# --- STATIC FILES ---
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def index():
    return FileResponse(os.path.join("static", "index.html"))

