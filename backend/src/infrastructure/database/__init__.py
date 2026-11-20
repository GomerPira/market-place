"""
Servicios de infraestructura: conexión con la base de datos.
"""

from src.infrastructure.database.variante_model import VarianteModel
from src.infrastructure.database.database import Base, engine, get_session
from src.infrastructure.database.product_model import ProductModel
from src.infrastructure.database.inventario_model import InventarioModel

__all__ = [
    "Base",
    "engine",
    "get_session",
    "ProductModel",
    "VarianteModel",
    "InventarioModel",
    "PedidoModel",
    "ItemPedidoModel"
]
from src.infrastructure.database.pedido_model import (
    PedidoModel,
    ItemPedidoModel
)
