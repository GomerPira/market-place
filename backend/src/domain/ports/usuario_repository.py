"""
UsuarioRepository — Puerto de salida para usuarios.
"""

from abc import ABC, abstractmethod
from typing import Optional

from ..entities.usuario import Usuario


class UsuarioRepositoryOutputPort(ABC):
    """
    Contrato de persistencia para usuarios (login y roles).
    """

    @abstractmethod
    def guardar(self, usuario: Usuario) -> Usuario:
        """
        Crea o actualiza un usuario.
        """
        pass

    @abstractmethod
    def buscar_por_id(self, id_usuario: str) -> Optional[Usuario]:
        """
        Busca un usuario por su ID.
        """
        pass

    @abstractmethod
    def buscar_por_correo(self, correo: str) -> Optional[Usuario]:
        """
        Busca un usuario por su correo electrónico.
        """
        pass
