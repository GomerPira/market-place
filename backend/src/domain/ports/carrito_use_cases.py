"""
CarritoUseCases — Puertos de entrada para gestión de carrito.
"""

from abc import ABC, abstractmethod
from typing import Optional

from ..entities.carrito import Carrito


class AgregarAlCarritoInputPort(ABC):
    """
    Caso de uso: agregar un producto al carrito.
    """

    @abstractmethod
    def ejecutar(
        self,
        comprador_id: str,
        producto_id: str,
        cantidad: int,
        variante_id: Optional[str] = None,
    ) -> Carrito:
        """
        Agrega o incrementa una cantidad del producto en el carrito.
        """
        pass


class QuitarDelCarritoInputPort(ABC):
    """
    Caso de uso: quitar un producto del carrito.
    """

    @abstractmethod
    def ejecutar(
        self,
        comprador_id: str,
        producto_id: str,
        variante_id: Optional[str] = None,
    ) -> Carrito:
        """
        Elimina un producto del carrito.
        """
        pass


class ListarCarritoInputPort(ABC):
    """
    Caso de uso: listar los productos del carrito.
    """

    @abstractmethod
    def ejecutar(self, comprador_id: str) -> Carrito:
        """
        Retorna el carrito del comprador.
        """
        pass
