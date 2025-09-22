from fastapi import APIRouter, File, UploadFile, HTTPException
from pathlib import Path
import shutil
from uuid import uuid4

router = APIRouter()
UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/")
async def upload_file(file: UploadFile= File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file")
    ext = Path(file.filename).suffix
    dest = UPLOAD_DIR / f"{uuid4().hex}{ext}"
    with dest.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    #processing
    return {"filename" : dest.name, "path": str(dest)}
