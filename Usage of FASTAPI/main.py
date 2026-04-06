from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

conversation_history = [
    {"role": "system", "content": "You are a helpful assistant"}
]

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    conversation_history.append({
        "role": "user", 
        "content": req.message
    })
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=conversation_history
    )
    
    ai_reply = response.choices[0].message.content
    
    conversation_history.append({
        "role": "assistant",
        "content": ai_reply
    })
    
    return {"reply": ai_reply}

@app.get("/")
def root():
    return {"status": "AI API is running!"}