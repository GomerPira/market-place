"""
ProductUseCases — Puertos de entrada para productos.

Caso de uso:
- Registrar un producto
- Listar productos
- Consutar un producto
- Modificar estado (publicar, suspender, etc.)
- Buscar productos activos
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.product import Producto

class RegistrarProductoInputPort(ABC):
    """
    Caso de uso: registrar un producto en el catálogo.
    """

    @abstractmethod
    def ejecutar(
        self,
        titulo: str,
        descripcion: str,
        tipo: str,
        precio_base: str,
        vendedor_id: Optional[str] = None,
    ) -> Producto:
        """
        Crea un producto (puede ser de prueba o por defecto DRAFT).
        Retorna el producto creado.
        """
        pass


class ListarProductosInputPort(ABC):
    """
    Caso de uso: listar productos.
    """

    @abstractmethod
    def ejecutar(self, solo_activos: bool = True) -> List[Producto]:
        """
        Retorna la lista de productos.
        Si solo_activos=True, solo devuelve productos que pueden venderse.
        """
        pass


class BuscarProductoPorIdInputPort(ABC):
    """
    Caso de uso: consultar un producto por ID.
    """

    @abstractmethod
    def ejecutar(self, id_producto: str) -> Optional[Producto]:
        """
        Retorna el producto o None si no existe.
        """
        pass
