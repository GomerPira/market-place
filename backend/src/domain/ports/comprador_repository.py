"""
CompradorRepository — Puerto de salida para compradores.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.comprador import Comprador


class CompradorRepositoryOutputPort(ABC):
    """
    Contrato de persistencia para compradores.
    """

    @abstractmethod
    def guardar(self, comprador: Comprador) -> Comprador:
        """
        Crea o actualiza un comprador.
        """
        pass

    @abstractmethod
    def buscar_por_id(self, id_comprador: str) -> Optional[Comprador]:
        """
        Busca un comprador por su ID.
        Devuelve None si no existe.
        """
        pass

    @abstractmethod
    def buscar_por_correo(self, correo: str) -> Optional[Comprador]:
        """
        Busca un comprador por su correo.
        """
        pass

    @abstractmethod
    def listar_activos(self) -> List[Comprador]:
        """
        Lista los compradores con estado ACTIVO.
        """
        pass
