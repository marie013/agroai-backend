from pydantic import BaseModel
from typing import Optional
from datetime import datetime

#Product
class ProductoCreate(BaseModel):
    name: str
    quantity: int = 0
    category: Optional[str] = None
    unit: Optional[str] = None
    description: Optional[str] = None

class ProductoRead(ProductoCreate):
    id: int

class ProductoUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[int] = None
    category: Optional[str] = None
    unit: Optional[str] = None
    description: Optional[str] = None

#Document

class DocumentRead(BaseModel):
    id: int
    name_file: str
    path: str
    date_upload: datetime
#Chat

class ChatRequest(BaseModel):
    prompt: str
    user_id: Optional[int] = None

class ChatResponse(BaseModel):
    response: str
    source: Optional[str] = None