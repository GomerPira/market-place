"""
Inventario — Representa las existencias de un producto en una bodega.

El Inventario tiene:
- cantidad disponible (puede venderse)
- cantidad reservada (temporalmente bloqueada por un pedido en curso)
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from ..value_objects import EstadoNoValido, InventarioNoValido


@dataclass
class Inventario:
    """
    Registra las existencias de un producto o variante en una bodega.

    Reglas de dominio:
    - No se puede tener inventario negativo.
    - No se puede reservar más de lo disponible.
    - El inventario tiene una unidad de medida (unidad física o unidad digital).
    """

    id: str
    producto_id: str
    bodega_id: str
    cantidad_disponible: int
    cantidad_reservada: int = 0
    variante_id: Optional[str] = None

    def __post_init__(self):
        if self.cantidad_disponible < 0:
            raise InventarioNoValido(
                f"Cantidad disponible inválida: {self.cantidad_disponible}. "
                f"Debe ser >= 0."
            )
        if self.cantidad_reservada < 0:
            raise InventarioNoValido(
                f"Cantidad reservada inválida: {self.cantidad_reservada}. "
                f"Debe ser >= 0."
            )
        if self.cantidad_reservada > self.cantidad_disponible:
            raise InventarioNoValido(
                f"Cantidad reservada ({self.cantidad_reservada}) "
                f"supera la cantidad disponible ({self.cantidad_disponible})."
            )

    def agregar_stock(self, cantidad: int) -> "Inventario":
        """
        Aumenta el stock disponible.
        Usado por logística cuando recibe mercancía.
        """
        if cantidad <= 0:
            raise InventarioNoValido("La cantidad a añadir debe ser positiva.")

        nuevo = Inventario(
            id=self.id,
            producto_id=self.producto_id,
            bodega_id=self.bodega_id,
            cantidad_disponible=self.cantidad_disponible + cantidad,
            cantidad_reservada=self.cantidad_reservada,
            variante_id=self.variante_id,
        )
        return nuevo

    def quitar_stock(self, cantidad: int) -> "Inventario":
        """
        Reduce el stock disponible.
        Usado por un pedido.
        """
        if cantidad <= 0:
            raise InventarioNoValido("La cantidad a quitar debe ser positiva.")
        if cantidad > self.cantidad_disponible:
            raise InventarioNoValido(
                f"No hay suficiente stock disponible. "
                f"Disponible: {self.cantidad_disponible}, pedido: {cantidad}."
            )

        nuevo = Inventario(
            id=self.id,
            producto_id=self.producto_id,
            bodega_id=self.bodega_id,
            cantidad_disponible=self.cantidad_disponible - cantidad,
            cantidad_reservada=self.cantidad_reservada,
            variante_id=self.variante_id,
        )
        return nuevo

    def reservar(self, cantidad: int) -> "Inventario":
        """
        Reserva stock para un pedido.
        Regla: no se puede reservar más de lo disponible.
        """
        if cantidad <= 0:
            raise InventarioNoValido("La cantidad a reservar debe ser positiva.")
        if cantidad > self.cantidad_disponible:
            raise InventarioNoValido(
                f"No hay suficiente stock disponible para reservar. "
                f"Disponible: {self.cantidad_disponible}, pedido: {cantidad}."
            )

        nuevo = Inventario(
            id=self.id,
            producto_id=self.producto_id,
            bodega_id=self.bodega_id,
            cantidad_disponible=self.cantidad_disponible - cantidad,
            cantidad_reservada=self.cantidad_reservada + cantidad,
            variante_id=self.variante_id,
        )
        return nuevo

    def liberar_reserva(self, cantidad: int) -> "Inventario":
        """
        Libera una reserva y devuelve el stock a disponible.
        Usado cuando un pedido se cancela.
        """
        if cantidad <= 0:
            raise InventarioNoValido("La cantidad a liberar debe ser positiva.")
        if cantidad > self.cantidad_reservada:
            raise InventarioNoValido(
                f"No se puede liberar más de lo reservado. "
                f"Reservado: {self.cantidad_reservada}, pedido: {cantidad}."
            )

        nuevo = Inventario(
            id=self.id,
            producto_id=self.producto_id,
            bodega_id=self.bodega_id,
            cantidad_disponible=self.cantidad_disponible + cantidad,
            cantidad_reservada=self.cantidad_reservada - cantidad,
            variante_id=self.variante_id,
        )
        return nuevo

    @property
    def stock_total(self) -> int:
        """Total físico = disponible + reservado."""
        return self.cantidad_disponible + self.cantidad_reservada

    @property
    def hay_stock(self) -> bool:
        return self.cantidad_disponible > 0
