"""
VarianteProducto — Representa una variante de un producto.

Un producto puede tener variantes: tallas, colores, modelos, etc.
Cada variante puede tener un precio adicional.

Esta clase sigue las mismas reglas que Producto:
- No conoce de persistencia
- No conoce de HTTP
- Solo reglas de dominio
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from ..value_objects import TipoNoValido, PrecioNoValido


@dataclass
class VarianteProducto:
    """
    Representa una variante de un producto.

    Ejemplo:
      - Producto: Remera
      - Variantes: "Talla L", "Color Azul", "Modelo X"
    """

    id: str
    sku: str
    atributo: str
    valor: str
    precio_adicional: Decimal

    def __post_init__(self):
        """Valida que el precio adicional sea correcto."""
        if self.precio_adicicional is None or self.precio_adicional < 0:
            raise PrecioNoValido(
                f"Precio adicional inválido: {self.precio_adicional}. "
                f"Debe ser >= 0."
            )

    @property
    def es_cero(self) -> bool:
        return self.precio_adicional == Decimal("0.00")

    def __str__(self) -> str:
        return f"{self.atributo}={self.valor}, precio adicional={self.precio_adicional}"
