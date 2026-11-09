"""
Puertos (contratos de entrada y salida) de NexusMarket.
"""

from src.domain.ports.product_repository import ProductRepositoryOutputPort
from src.domain.ports.inventario_repository import InventarioRepositoryOutputPort
from src.domain.ports.product_use_cases import (
    RegistrarProductoInputPort,
    ListarProductosInputPort,
    BuscarProductoPorIdInputPort,
)
from src.domain.ports.carrito_use_cases import (
    AgregarAlCarritoInputPort,
    QuitarDelCarritoInputPort,
    ListarCarritoInputPort,
)
from src.domain.ports.comprador_repository import CompradorRepositoryOutputPort
from src.domain.ports.vendedor_repository import VendedorRepositoryOutputPort
from src.domain.ports.usuario_repository import UsuarioRepositoryOutputPort

ports = [
    ProductRepositoryOutputPort,
    InventarioRepositoryOutputPort,
    RegistrarProductoInputPort,
    ListarProductosInputPort,
    BuscarProductoPorIdInputPort,
    AgregarAlCarritoInputPort,
    QuitarDelCarritoInputPort,
    ListarCarritoInputPort,
    CompradorRepositoryOutputPort,
    VendedorRepositoryOutputPort,
    UsuarioRepositoryOutputPort,
]
