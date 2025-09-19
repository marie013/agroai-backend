from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select 
from app.db import get_session
from sqlmodel import Session
from app.models import Producto
from app.schemas import ProductoCreate, ProductoRead, ProductoUpdate

router = APIRouter()

#CRUD DE PRODUCTO

@router.post("/", response_model=ProductoRead)
def create_product(playload: ProductoCreate, session: Session = Depends(get_session)):
    producto = Producto.from_orm(playload)
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto

@router.get("/", response_model=list[ProductoRead])
def list_productos(session : Session = Depends(get_session)):
    productos = session.exec(select(Producto)).all()
    return productos

@router.get("/{producto_id}", response_model=ProductoRead)
def get_producto(producto_id: int, session : Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not Producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")
    return producto

@router.put("/{producto_id}", response_model=ProductoRead)
def update_producto(producto_id: int, playload: ProductoUpdate, session: Session = Depends(get_session)):
    producto= session.set(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code= 404, detail="Producto no encontrado.")
    producto_data= playload.dict(exclude_unset=True)
    for key, value in producto_data.items():
        setattr(producto, key, value)
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto

@router.delete("/{producto_id}")
def delete_producto(producto_id : int, session : Session = Depends(get_session)):
    producto= session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")
    session.delete(producto)
    session.commit()
    return {"ok" : True}
