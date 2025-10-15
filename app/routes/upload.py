from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from pathlib import Path
import shutil
from uuid import uuid4
from sqlmodel import Session
from app.db import get_session
from app.models import Document

router = APIRouter()
UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/")
async def upload_file(file: UploadFile= File(...), session: Session = Depends(get_session)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file")
    ext = Path(file.filename).suffix
    dest = UPLOAD_DIR / f"{uuid4().hex}{ext}"
    with dest.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    #processing
    document = Document(name_file= file.filename, path= str(dest))
    session.add(document)
    session.commit()
    session.refresh(document)
    return {"id": document.id, "name_file": document.name_file, "path": document.path}
