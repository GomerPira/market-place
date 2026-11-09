"""
Dominio de NexusMarket (DDD).
"""

from src.domain.entities.product import Producto
from src.domain.entities.inventario import Inventario
from src.domain.entities.carrito import Carrito
from src.domain.entities.pedido import Pedido
from src.domain.entities.comprador import Comprador
from src.domain.entities.vendedor import Vendedor
from src.domain.entities.usuario import Usuario
from src.domain.entities.bodega import Bodega

domain_entities = [
    Producto,
    Inventario,
    Carrito,
    Pedido,
    Comprador,
    Vendedor,
    Usuario,
    Bodega,
]
