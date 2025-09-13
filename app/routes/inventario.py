from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select 
from app.db import get_session
from sqlmodel import Session
from app.models import Producto
from app.schemas import ProductoCreate, ProductoRead, ProductoUpdate

router = APIRouter()
