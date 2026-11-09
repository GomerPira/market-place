"""
Precio — Value Object inmutable para el precio de un producto.

Un precio representa una cantidad en una moneda determinada.
Es inmutable: no se puede cambiar una vez creado.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

from .errors import PrecioNoValido


@dataclass(frozen=True)
class Precio:
    """
    Representa un precio con moneda y cantidad exacta.
    La cantidad se almacena como Decimal para evitar errores de punto flotante.
    """

    moneda: str
    cantidad: Decimal

    def __post_init__(self):
        if self.cantidad is None or self.cantidad < 0:
            raise PrecioNoValido(
                f"El precio no puede ser negativo: {self.cantidad}"
            )
        # Redondea a 2 decimales para evitar errores de precisión
        object.__setattr__(self, "cantidad", self.cantidad.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

    def __add__(self, otro: "Precio") -> "Precio":
        if not isinstance(otro, Precio):
            return NotImplemented
        if self.moneda != otro.moneda:
            raise TypeError(
                f"No se puede sumar {self.moneda} con {otro.moneda}. "
                f"Monedas deben coincidir."
            )
        return Precio(moneda=self.moneda, cantidad=self.cantidad + otro.cantidad)

    def __sub__(self, otro: "Precio") -> "Precio":
        if not isinstance(otro, Precio):
            return NotImplemented
        if self.moneda != otro.moneda:
            raise TypeError(
                f"No se puede restar {self.moneda} con {otro.moneda}. "
                f"Monedas deben coincidir."
            )
        resultado = self.cantidad - otro.cantidad
        if resultado < 0:
            raise PrecioNoValido("El resultado de la resta no puede ser negativo.")
        return Precio(moneda=self.moneda, cantidad=resultado)

    def __mul__(self, factor: Decimal) -> "Precio":
        if not isinstance(factor, Decimal):
            return NotImplemented
        return Precio(
            moneda=self.moneda,
            cantidad=(self.cantidad * factor).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        )

    def __truediv__(self, divisor: Decimal) -> "Precio":
        if not isinstance(divisor, Decimal):
            return NotImplemented
        if divisor == Decimal("0"):
            raise PrecioNoValido("No se puede dividir entre cero.")
        return Precio(
            moneda=self.moneda,
            cantidad=(self.cantidad / divisor).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        )

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Precio):
            return NotImplemented
        return self.moneda == otro.moneda and self.cantidad == otro.cantidad

    def __str__(self) -> str:
        return f"{self.cantidad} {self.moneda}"

    @property
    def en_cents(self) -> int:
        """
        Para fines de almacenamiento o de pasarela de pago, se puede convertir a enteros.
        """
        return int(self.cantidad * 100)
