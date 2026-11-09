"""
Adaptadores de entrada (REST) de NexusMarket.
"""

from src.adapters.rest.productos_rest import router as productos_router
from src.adapters.rest.inventario_rest import router as inventario_router

rest_routers = [
    productos_router,
    inventario_router,
]
