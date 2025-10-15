from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db import get_session
from app.schemas import ChatRequest, ChatResponse
from app.models import ChatLog
from app.services.rag import rag_answer
""" from pydantic import BaseModel
from typing import Optional
import time, json
from pathlib import Path """

router = APIRouter()

@router.post("/", response_model=ChatResponse)
def chat(req: ChatRequest, session: Session = Depends(get_session)):
    try:
        answer = rag_answer(req.prompt)
    except Exception as e:
        answer = f"[Error LLM] {str(e)}"
  
    #llamar al LLM + RAG
    chat_log = ChatLog(user_id=req.user_id, prompt=req.prompt, response=answer)
    session.add(chat_log)
    session.commit()

    return {"response": answer, "source": "RAG"}
