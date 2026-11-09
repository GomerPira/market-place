"""
Usuario — Representa la identidad de acceso (login) del sistema.

Cada usuario tiene un rol: Comprador, Vendedor, OperadorLogístico, Administrador o Supervisor.
¿El usuario puede acceder se decide con estado (Activo, Bloqueado, Pendiente).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..value_objects import (
    UsuarioNoValido,
    RolNoValido,
    EstadoNoValido,
)


@dataclass
class Usuario:
    """
    Representa a un usuario del sistema.
    """

    id: str
    correo_electronico: str
    contrasena_hash: str
    rol: str
    estado: str = "ACTIVO"
    persona_asociada_id: Optional[str] = None

    def __post_init__(self):
        if self.rol not in ("COMPRADOR", "VENDEDOR", "OPERADOR_LOGISTICO", "ADMINISTRADOR", "SUPERVISOR"):
            raise RolNoValido(f"Rol no válido: {self.rol}.")
        if self.estado not in ("ACTIVO", "BLOQUEADO", "PENDIENTE"):
            raise EstadoNoValido(f"Estado no válido: {self.estado}.")

    def activar(self) -> "Usuario":
        return self._cambiar_estado("ACTIVO")

    def bloquear(self) -> "Usuario":
        return self._cambiar_estado("BLOQUEADO")

    def _cambiar_estado(self, nuevo_estado: str) -> "Usuario":
        return Usuario(
            id=self.id,
            correo_electronico=self.correo_electronico,
            contrasena_hash=self.contrasena_hash,
            rol=self.rol,
            estado=nuevo_estado,
            persona_asociada_id=self.persona_asociada_id,
        )

    @property
    def puede_acceder(self) -> bool:
        """
        Solo los usuarios con estado ACTIVO pueden autenticarse.
        """
        return self.estado == "ACTIVO"

    def __str__(self) -> str:
        return f"Usuario({self.rol}, {self.correo_electronico}, {self.estado})"
