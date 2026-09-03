"""
Aplicación FastAPI mínima.

Responsabilidad:
- Inicializar aplicación FastAPI y middleware CORS.
- Proveer endpoint /health para verificación básica.
- Punto de entrada para futuras rutas (auth, vehicles, boletas, ocr).
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

app = FastAPI(
    title="Parking PINFRA API",
    version="0.1.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["diagnostic"])
async def health():
    """
    Endpoint de salud simple.
    """
    return {"status": "ok"}
