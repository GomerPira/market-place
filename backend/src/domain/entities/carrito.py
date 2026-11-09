"""
Carrito — Representa los productos que un comprador ha seleccionado para comprar.

El carrito es mutable: el comprador puede añadir o quitar ítems.
Cuando se confirma el pedido, el carrito se vacía automáticamente.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional

from ..value_objects import ItemNoValido, ProductoNoValido


@dataclass
class ItemCarrito:
    """
    Línea de carrito.
    """

    id: str
    producto_id: str
    producto_titulo: str
    variante_id: Optional[str]
    cantidad: int
    precio_unitario: Decimal

    def __post_init__(self):
        if self.cantidad <= 0:
            raise ItemNoValido("La cantidad debe ser mayor que 0.")

    @property
    def subtotal(self) -> Decimal:
        return self.precio_unitario * self.cantidad


@dataclass
class Carrito:
    """
    Contenedor de los productos que un comprador está eligiendo.
    """

    id: str
    comprador_id: str
    items: list[ItemCarrito] = field(default_factory=list)

    def agregar(self, item: ItemCarrito) -> "Carrito":
        """
        Añade un ítem al carrito.
        Si el producto ya está en el carrito, suma la cantidad.
        """
        nuevo_items = list(self.items)
        for idx, existing in enumerate(nuevo_items):
            if existing.producto_id == item.producto_id and existing.variante_id == item.variante_id:
                nuevo_items[idx] = ItemCarrito(
                    id=existing.id,
                    producto_id=existing.producto_id,
                    producto_titulo=existing.producto_titulo,
                    variante_id=existing.variante_id,
                    cantidad=existing.cantidad + item.cantidad,
                    precio_unitario=existing.precio_unitario,
                )
                return Carrito(id=self.id, comprador_id=self.comprador_id, items=nuevo_items)

        nuevo_items.append(item)
        return Carrito(id=self.id, comprador_id=self.comprador_id, items=nuevo_items)

    def quitar(self, producto_id: str, variante_id: Optional[str]) -> "Carrito":
        """
        Elimina un ítem del carrito.
        """
        nuevo_items = [
            i for i in self.items
            if not (i.producto_id == producto_id and i.variante_id == variante_id)
        ]
        return Carrito(id=self.id, comprador_id=self.comprador_id, items=nuevo_items)

    @property
    def total(self) -> Decimal:
        return sum(item.subtotal for item in self.items)

    @property
    def cantidad_items(self) -> int:
        return sum(item.cantidad for item in self.items)

    @property
    def esta_vacio(self) -> bool:
        return self.cantidad_items == 0
