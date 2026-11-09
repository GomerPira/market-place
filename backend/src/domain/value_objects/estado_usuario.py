"""
EstadoUsuario — Estados operativos del usuario.

- ACTIVO: puede ejecutar operaciones
- BLOQUEADO: no puede acceder
- PENDIENTE: aun no se ha validado
"""

from __future__ import annotations

from enum import Enum


class EstadoUsuario(str, Enum):
    ACTIVO = "ACTIVO"
    BLOQUEADO = "BLOQUEADO"
    PENDIENTE = "PENDIENTE"
