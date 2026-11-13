"""
Adaptadores de entrada (REST) de NexusMarket.
"""

from fastapi import FastAPI

from src.adapters.rest.productos_rest import router as productos_router
from src.adapters.rest.inventario_rest import router as inventario_router


def register_rest_adapters(app: FastAPI) -> None:
    """
    Registra todos los routers REST en la aplicación.
    """
    app.include_router(productos_router)
    app.include_router(inventario_router)
