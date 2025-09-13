from pydantic import BaseModel
from typing import Optional

class ProductoCreate(BaseModel):
    nombre: str
    cantidad: int = 0
    categoria: Optional[str] = None
    unidad: Optional[str] = None
    descripcion: Optional[str] = None

class ProductoRead(ProductoCreate):
    id: int

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    cantidad: Optional[int] = None
    categoria: Optional[str] = None
    unidad: Optional[str] = None
    descripcion: Optional[str] = None