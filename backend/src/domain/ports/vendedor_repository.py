"""
VendedorRepository — Puerto de salida para vendedores.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from ...entities.vendedor import Vendedor


class VendedorRepositoryOutputPort(ABC):
    """
    Contrato de persistencia para vendedores.
    """

    @abstractmethod
    def guardar(self, vendedor: Vendedor) -> Vendedor:
        """
        Crea o actualiza un vendedor.
        """
        pass

    @abstractmethod
    def buscar_por_id(self, id_vendedor: str) -> Optional[Vendedor]:
        """
        Busca un vendedor por su ID.
        """
        pass

    @abstractmethod
    def buscar_por_nit(self, nit: str) -> Optional[Vendedor]:
        """
        Busca un vendedor por su NIT o documento fiscal.
        """
        pass

    @abstractmethod
    def listar_activos(self) -> List[Vendedor]:
        """
        Lista los vendedores con estado ACTIVO.
        """
        pass
