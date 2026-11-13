"""
ProductRepository — Puerto de salida para productos.

Define cómo se pueden obtener y guardar productos en el dominio.
La implementación concreta puede ser en memoria, MySQL, PostgreSQL, etc.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.product import Producto


class ProductRepositoryOutputPort(ABC):
    """
    Contrato para el acceso a la persistencia de productos.
    El dominio depende de este puerto, no del adaptador concreto.
    """

    @abstractmethod
    def guardar(self, producto: Producto) -> Producto:
        """
        Guarda o actualiza un producto.
        Si el ID ya existe, actualiza; si no, crea.
        """
        pass

    @abstractmethod
    def buscar_por_id(self, id_producto: str) -> Optional[Producto]:
        """
        Busca un producto por su ID.
        Devuelve None si no existe.
        """
        pass

    @abstractmethod
    def listar_activos(self) -> List[Producto]:
        """
        Lista los productos que podrían venderse actualmente.
        Normalmente filtra por estado PUBLICADO o PENDIENTE.
        """
        pass

    @abstractmethod
    def listar_por_vendedor(self, id_vendedor: str) -> List[Producto]:
        """
        Lista productos de un vendedor.
        """
        pass

    @abstractmethod
    def existe(self, id_producto: str) -> bool:
        """
        Indica si un producto con ese ID ya existe.
        """
        pass
