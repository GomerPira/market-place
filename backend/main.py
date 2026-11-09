"""
Market Place — Backend principal (NexusMarket)

Punto de entrada de la aplicación. Crea las tablas en MySQL (si no existen),
inicia el servidor de OpenAPI con uvicorn y expone la API REST.

Este módulo actúa como el "Adaptador de Entrada" (REST) principal: recibe las
peticiones HTTP, las valida, y delega a los casos de uso de la capa de
aplicación. No contiene reglas de negocio propias.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.infrastructure.database.database import Base, engine
from src.adapters.rest import register_rest_adapters


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Crea las tablas al iniciar el contenedor y limpia recursos al cerrarlo."""
    # Sincroniza el modelo con la base de datos
    Base.metadata.create_all(bind=engine)
    yield
    # En un entorno de producción se deberían cerrar conexiones aquí
    # (p. ej. engine.dispose()).


app = FastAPI(
    title="NexusMarket — Marketplace Backend",
    version="1.0.0",
    description="API REST del Marketplace NexusMarket (DDD + Arquitectura Hexagonal en Python).",
    lifespan=lifespan,
)


@app.get("/", include_in_schema=False)
def root():
    """Endpoint de bienvenida sin metadata de Swagger."""
    return JSONResponse(
        status_code=200,
        content={
            "service": "nexus-market-backend",
            "version": "1.0.0",
            "message": "Bienvenido al Marketplace NexusMarket.",
            "docs": "/docs",
            "health": "/health",
        },
    )


@app.get("/health", include_in_schema=False)
def health():
    """Endpoint de salud para healthchecks y monitorización."""
    return JSONResponse(
        status_code=200,
        content={
            "status": "ok",
            "service": "nexus-market-backend",
        },
    )


# Registra los adaptadores REST
register_rest_adapters(app)
