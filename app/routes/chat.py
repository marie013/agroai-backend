from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import time, json
from pathlib import Path

router = APIRouter()
LOG_DIR = Path("data/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
CHAT_LOG = LOG_DIR / "chat.log"

class ChatRequest(BaseModel):
    prompt: str
    user_id: Optional[int] = None

class ChatResponse(BaseModel):
    response: str
    source: Optional[str] = None

@router.post("/", response_model=ChatResponse)
def chat(req: ChatRequest):
    #llamar al LLM + RAG
    response_text = f"Echo: {req.prompt}"
    with CHAT_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": time.time(), "user_id":req.user_id, "prompt": req.prompt, "response": response_text}) + "\n")
        return {"response": response_text, "source": "local-echo"}