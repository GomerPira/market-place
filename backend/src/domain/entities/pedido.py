"""
Pedido — Representa el compromiso comercial de compra.

El pedido pasa por un ciclo de vida:
  PENDIENTE_PAGO -> PAGADO -> ENTREGADO / CANCELADO

Reglas:
- No se puede modificar un pedido entregado o cancelado.
- Solo un comprador activo puede crear pedidos.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from ..value_objects import (
    EstadoNoValido,
    PedidoNoValido,
    CompradorNoValido,
)


@dataclass
class ItemPedido:
    """
    Línea de un pedido.
    Referencia al producto, la variante (opcional) y la cantidad pedida.
    """

    id: str
    producto_id: str
    producto_titulo: str
    variante_id: Optional[str]
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal
    bodega_id: Optional[str] = None


@dataclass
class Pedido:
    """
    Representa un pedido realizado por un comprador.
    """

    id: str
    comprador_id: str
    direccion_envio: str
    items: List[ItemPedido] = field(default_factory=list)
    monto_total: Decimal = Decimal("0.00")
    estado: str = "PENDIENTE_PAGO"
    fecha_creacion: datetime = field(default_factory=datetime.utcnow)
    fecha_pago: Optional[datetime] = None
    fecha_entrega: Optional[datetime] = None
    detalles_pago: Optional[dict] = None
    observaciones: Optional[str] = None

    def __post_init__(self):
        if self.estado not in ("PENDIENTE_PAGO", "PAGADO", "ENTREGADO", "CANCELADO"):
            raise EstadoNoValido(
                f"Estado no válido: {self.estado}."
            )

    def calcular_total(self) -> Decimal:
        """
        Recalcula el total a partir de las líneas.
        """
        total = Decimal("0.00")
        for item in self.items:
            total += item.subtotal
        return total

    def agregar_item(self, item: ItemPedido) -> "Pedido":
        """
        Añade un ítem y recalcula el total.
        """
        nuevo = Pedido(
            id=self.id,
            comprador_id=self.comprador_id,
            direccion_envio=self.direccion_envio,
            items=list(self.items) + [item],
            monto_total=self.calcular_total(),
            estado=self.estado,
            fecha_creacion=self.fecha_creacion,
        )
        return nuevo

    def eliminar_item(self, item_id: str) -> "Pedido":
        """
        Elimina un ítem; si el item no existe, devuelve el mismo pedido.
        """
        nuevo_items = [i for i in self.items if i.id != item_id]
        if len(nuevo_items) == len(self.items):
            return self

        nuevo = Pedido(
            id=self.id,
            comprador_id=self.comprador_id,
            direccion_envio=self.direccion_envio,
            items=nuevo_items,
            monto_total=self.calcular_total(),
            estado=self.estado,
            fecha_creacion=self.fecha_creacion,
        )
        return nuevo

    def confirmar_pago(self, referencia_pago: str) -> "Pedido":
        """
        Cambia el estado a PAGADO y registra la referencia.
        """
        if self.estado in ("ENTREGADO", "CANCELADO"):
            raise PedidoNoValido("No se puede pagar un pedido entregado o cancelado.")

        nuevo = Pedido(
            id=self.id,
            comprador_id=self.comprador_id,
            direccion_envio=self.direccion_envio,
            items=self.items,
            monto_total=self.calcular_total(),
            estado="PAGADO",
            fecha_pago=datetime.utcnow(),
            detalles_pago={"referencia_pago": referencia_pago},
            observaciones=self.observaciones,
        )
        return nuevo

    def cancelar(self, motivo: str) -> "Pedido":
        """
        Cancela el pedido si aún puede cancelarse.
        """
        if self.estado == "ENTREGADO":
            raise PedidoNoValido("No se puede cancelar un pedido entregado.")

        nuevo = Pedido(
            id=self.id,
            comprador_id=self.comprador_id,
            direccion_envio=self.direccion_envio,
            items=self.items,
            monto_total=self.calcular_total(),
            estado="CANCELADO",
            observaciones=motivo,
            fecha_pago=self.fecha_pago,
        )
        return nuevo

    @property
    def es_pagado(self) -> bool:
        return self.estado == "PAGADO"

    @property
    def es_cancelado(self) -> bool:
        return self.estado == "CANCELADO"

    @property
    def es_entregado(self) -> bool:
        return self.estado == "ENTREGADO"
