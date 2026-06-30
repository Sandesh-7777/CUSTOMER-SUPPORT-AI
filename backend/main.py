# main.py — FastAPI backend for Multi-Agent AI Chat
# Run with: uvicorn main:app --reload --port 8000

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os, uuid
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

from agents.router import detect_intent
from agents import billing, technical, product, complaint, faq
from fastapi import Depends, HTTPException, Header
from auth import hash_password, verify_password, create_access_token, decode_access_token

load_dotenv()

app = FastAPI(title="Multi-Agent AI Support API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-app-name.vercel.app",  # we'll update this after Step 6
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mongo_client = MongoClient(os.getenv("MONGODB_URI"))
db = mongo_client["support_ai"]
messages_col = db["messages"]
users_col = db["users"]

# Maps intent name -> the agent module that handles it
AGENT_MAP = {
    "billing": billing,
    "technical": technical,
    "product": product,
    "complaint": complaint,
    "faq": faq,
}


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    session_id: str
    agent_used: str
    timestamp: str

class SignupRequest(BaseModel):
    email: str
    password: str
    name: str


class LoginRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    token: str
    user_id: str
    name: str
    email: str

def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    """
    Reads the 'Authorization: Bearer <token>' header, verifies it,
    and returns the user's info. Raises 401 if invalid or missing.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    token = authorization.replace("Bearer ", "")
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Token expired or invalid")

    return {"user_id": payload["sub"], "email": payload["email"]}

def get_history(session_id: str) -> list:
    docs = messages_col.find(
        {"session_id": session_id}, {"_id": 0, "role": 1, "content": 1},
        sort=[("timestamp", 1)]
    )
    return [{"role": d["role"], "content": d["content"]} for d in docs]


def save_message(session_id: str, role: str, content: str):
    messages_col.insert_one({
        "session_id": session_id, "role": role,
        "content": content, "timestamp": datetime.utcnow()
    })


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, current_user: dict = Depends(get_current_user)):
    # Tie the session to this specific user
    session_id = req.session_id or f"{current_user['user_id']}_{uuid.uuid4()}"

    history = get_history(session_id)

    intent = detect_intent(req.message)
    agent_module = AGENT_MAP[intent]
    reply = agent_module.answer(req.message, history)

    save_message(session_id, "user", req.message)
    save_message(session_id, "assistant", reply)

    return ChatResponse(
        reply=reply, session_id=session_id,
        agent_used=intent, timestamp=datetime.utcnow().isoformat()
    )


@app.get("/history/{session_id}")
def history(session_id: str, current_user: dict = Depends(get_current_user)):
    return {"messages": get_history(session_id)}

@app.get("/my-sessions")
def my_sessions(current_user: dict = Depends(get_current_user)):
    """Returns all session IDs that belong to this user, most recent first."""
    prefix = current_user["user_id"]
    sessions = messages_col.distinct(
        "session_id",
        {"session_id": {"$regex": f"^{prefix}_"}}
    )
    return {"sessions": sessions}

@app.post("/auth/signup", response_model=AuthResponse)
def signup(req: SignupRequest):
    # Check if email already exists
    existing = users_col.find_one({"email": req.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_id = str(uuid.uuid4())
    users_col.insert_one({
        "user_id": user_id,
        "email": req.email,
        "name": req.name,
        "password_hash": hash_password(req.password),
        "created_at": datetime.utcnow(),
    })

    token = create_access_token(user_id, req.email)
    return AuthResponse(token=token, user_id=user_id, name=req.name, email=req.email)


@app.post("/auth/login", response_model=AuthResponse)
def login(req: LoginRequest):
    user = users_col.find_one({"email": req.email})
    if not user or not verify_password(req.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(user["user_id"], user["email"])
    return AuthResponse(
        token=token, user_id=user["user_id"],
        name=user["name"], email=user["email"]
    )