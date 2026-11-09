"""
Objetos de valor del dominio (DDD).

Incluye:
- Precios
- Estados de productos y usuarios
- Tipos de productos
- Roles de usuario
- Excepciones de dominio
"""

from src.domain.value_objects.precio import Precio
from src.domain.value_objects.estado_producto import EstadoProducto
from src.domain.value_objects.tipo_producto import TipoProducto
from src.domain.value_objects.rol_usuario import RolUsuario
from src.domain.value_objects.estado_usuario import EstadoUsuario
from src.domain.value_objects.errors import (
    DominioError,
    ProductoNoValido,
    TipoNoValido,
    EstadoNoValido,
    PrecioNoValido,
    ItemNoValido,
    PedidoNoValido,
    InventarioNoValido,
    BodegaNoValido,
    CompradorNoValido,
    VendedorNoValido,
    UsuarioNoValido,
    DireccionNoValida,
    NitNoValido,
    DocumentoNoValido,
    RolNoValido,
)

value_objects = [
    Precio,
    EstadoProducto,
    TipoProducto,
    RolUsuario,
    EstadoUsuario,
    DominioError,
    ProductoNoValido,
    TipoNoValido,
    EstadoNoValido,
    PrecioNoValido,
    ItemNoValido,
    PedidoNoValido,
    InventarioNoValido,
    BodegaNoValido,
    CompradorNoValido,
    VendedorNoValido,
    UsuarioNoValido,
    DireccionNoValida,
    NitNoValido,
    DocumentoNoValido,
    RolNoValido,
]
