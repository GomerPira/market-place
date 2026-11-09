"""
EstadoProducto — Tipos controlados para el estado de un producto.

El estado define cómo se comporta el producto en el catálogo:
- DRAFT: todavía no está listo
- PENDIENTE: está listo pero no publicado aún
- PUBLICADO: visible y vendible
- SUSPENDIDO: temporalmente no se vende
- DESCONTINUADO: ya no se vende
"""

from __future__ import annotations

from enum import Enum


class EstadoProducto(str, Enum):
    DRAFT = "DRAFT"
    PENDIENTE = "PENDIENTE"
    PUBLICADO = "PUBLICADO"
    SUSPENDIDO = "SUSPENDIDO"
    DESCONTINUADO = "DESCONTINUADO"
