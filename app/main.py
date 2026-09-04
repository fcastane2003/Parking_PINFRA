"""
app/main.py

Responsabilidad:
- Inicializar la aplicación FastAPI y registrar routers.
- Exponer endpoint /health.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

# Import routers
from app.api import vehicles, boletas, auth, employees

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
    return {"status": "ok"}


# Incluir routers
app.include_router(vehicles.router)
app.include_router(boletas.router)
app.include_router(auth.router)
app.include_router(employees.router)
