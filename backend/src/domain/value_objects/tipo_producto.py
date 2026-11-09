"""
TipoProducto — Tipos controlados para los productos.

- FISICO: producto físico que requiere peso, dimensiones e inventario
- DIGITAL: producto digital, sin logística física
"""

from __future__ import annotations

from enum import Enum


class TipoProducto(str, Enum):
    FISICO = "FISICO"
    DIGITAL = "DIGITAL"
