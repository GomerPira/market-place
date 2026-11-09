"""
InventarioRepository — Puerto de salida para inventario.

Define cómo se pueden obtener y guardar existencias por bodega.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from ...entities.inventario import Inventario


class InventarioRepositoryOutputPort(ABC):
    """
    Contrato para el acceso a la persistencia de inventario.
    """

    @abstractmethod
    def guardar(self, inventario: Inventario) -> Inventario:
        """
        Guarda o actualiza un registro de inventario.
        """
        pass

    @abstractmethod
    def buscar_por_producto_y_bodega(
        self, producto_id: str, bodega_id: str
    ) -> Optional[Inventario]:
        """
        Busca inventario para un producto específico en una bodega.
        """
        pass

    @abstractmethod
    def listar_por_producto(self, producto_id: str) -> List[Inventario]:
        """
        Lista todos los inventarios de un producto (un producto puede estar en varias bodegas).
        """
        pass

    @abstractmethod
    def listar_activos(self) -> List[Inventario]:
        """
        Lista los inventarios activos.
        """
        pass
