from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uuid
import httpx
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")

sessions = {}

class ChatMessage(BaseModel):
    session_id: Optional[str] = None
    user_message: str

def is_sensitive(msg: str) -> bool:
    keywords = ["angry", "upset", "disappointed", "bad service", "frustrated", "refund", "hate"]
    return any(word in msg.lower() for word in keywords)

def construct_prompt(history: list, user_message: str) -> str:
    conversation = ""
    for turn in history:
        conversation += f"Customer: {turn['user']}\nAgent: {turn['bot']}\n"
    if is_sensitive(user_message):
        conversation += (
            f"Customer: {user_message}\n"
            f"Agent: I understand your concern, and I’m here to help. Let me assist you with that.\n"
        )
    else:
        conversation += f"Customer: {user_message}\nAgent:"
    return conversation

@app.post("/chat")
async def chat(message: ChatMessage):
    if message.session_id and message.session_id in sessions:
        session_id = message.session_id
        history = sessions[session_id]
    else:
        session_id = str(uuid.uuid4())
        history = []
        sessions[session_id] = history

    prompt = construct_prompt(history, message.user_message)

    try:
        start = time.time()
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "phi3:mini",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
        end = time.time()
        print(f"Model response time: {end - start:.2f} seconds")
        data = response.json()
        reply = data.get("response") or data.get("message") or "Sorry, no response from model."
    except Exception as e:
        reply = f"Sorry, there was an error contacting the model: {str(e)}"

    history.append({"user": message.user_message, "bot": reply})

    return {
        "session_id": session_id,
        "response": reply
    }