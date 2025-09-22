from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    quantity: int = 0
    category: Optional[str] = None
    unit: Optional[str] = None
    description: Optional[str] = None

#Documents
class Document(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name_file: str
    path: str
    date_upload: datetime = Field(default_factory=datetime.utcnow)

#Chatlogs
class ChatLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = None
    prompt: str
    response: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)