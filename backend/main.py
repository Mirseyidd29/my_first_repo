import json
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
from backend.chat import get_reply, PRODUCTS

app = FastAPI(title="Atlas AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND = Path(__file__).parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=str(FRONTEND)), name="static")


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: List[Message] = []


@app.get("/")
def index():
    return FileResponse(str(FRONTEND / "index.html"))


@app.post("/chat")
def chat(req: ChatRequest):
    reply = get_reply(req.message, req.history)
    return {"reply": reply}


@app.get("/products")
def products():
    return PRODUCTS


@app.get("/health")
def health():
    return {"status": "ok"}
