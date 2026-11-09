"""
RolUsuario — Roles permitidos en NexusMarket.

Cada rol define un perfil con capacidades distintas.
- COMPRADOR: compra productos
- VENDEDOR: publica y gestiona productos
- OPERADOR_LOGISTICO: gestiona envíos e inventario físico
- ADMINISTRADOR: configura el marketplace
- SUPERVISOR: supervisa operaciones
"""

from __future__ import annotations

from enum import Enum


class RolUsuario(str, Enum):
    COMPRADOR = "COMPRADOR"
    VENDEDOR = "VENDEDOR"
    OPERADOR_LOGISTICO = "OPERADOR_LOGISTICO"
    ADMINISTRADOR = "ADMINISTRADOR"
    SUPERVISOR = "SUPERVISOR"
