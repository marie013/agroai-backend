from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db import get_session
from app.schemas import ChatRequest, ChatResponse
from app.models import ChatLog
""" from pydantic import BaseModel
from typing import Optional
import time, json
from pathlib import Path """

router = APIRouter()

@router.post("/", response_model=ChatResponse)
def chat(req: ChatRequest, session: Session = Depends(get_session)):
    #llamar al LLM + RAG
    response_text = f"Echo: {req.prompt}"
    chat_log = ChatLog(user_id=req.user_id, prompt=req.prompt, response=response_text)
    session.add(chat_log)
    session.commit()

    return {"response": response_text, "source": "local-echo"}