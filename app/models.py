from typing import Optional
from sqlmodel import SQLModel, Field

class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    cantidad: int = 0
    categoria: Optional[str] = None
    unidad: Optional[str] = None
    descripcion: Optional[str] = None