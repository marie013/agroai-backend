from fastapi import FastAPI
from app.db import init_db
from app.middleware import PiiMiddleware
from app.routes import inventario_router, upload_router, chat_router

app= FastAPI(title="agroAI Assistant - Backend")

app.add_middleware(PiiMiddleware)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(inventario_router, prefix="/inventario", tags=["inventario"])
app.include_router(upload_router, prefix="/upload", tags=["upload"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])