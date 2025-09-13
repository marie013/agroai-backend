import re
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse

PII_PATTERNS = [
    re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"),  # email
    re.compile(r"\b\d{7,8}\b"),  # DNI (Argentina) 7-8 dígitos
    re.compile(r"\+?\d{7,15}\b"),  # teléfono básico
]

class PiiMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method in ("POST", "PUT"):
            body = await request.body()
            text = body.decode("utf-8", errors="ignore")
            for p in PII_PATTERNS:
                if p.search(text):
                    return JSONResponse(status_code=400,
                                        content={"detail": "PII detected in request. Remove personal data before sending."})
        return await call_next(request)