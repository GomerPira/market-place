"""
Pruebas de Pedido.
"""

import pytest
from decimal import Decimal

from src.domain.entities.pedido import Pedido, ItemPedido
from src.domain.value_objects.errors import PedidoNoValido


class TestPedido:
    def test_crear_pedido(self):
        item = ItemPedido(
            id="it_1",
            producto_id="prod_1",
            producto_titulo="Laptop",
            variante_id=None,
            cantidad=1,
            precio_unitario=Decimal("1500000.00"),
            subtotal=Decimal("1500000.00"),
        )
        pedido = Pedido(
            id="ped_1",
            comprador_id="comp_1",
            direccion_envio="Calle 1 # 2 - 3",
            items=[item],
            monto_total=Decimal("1500000.00"),
        )
        assert pedido.es_pagado is False
        assert pedido.estado == "PENDIENTE_PAGO"

    def test_confirmar_pago(self):
        item = ItemPedido(
            id="it_1",
            producto_id="prod_1",
            producto_titulo="Laptop",
            variante_id=None,
            cantidad=1,
            precio_unitario=Decimal("1500000.00"),
            subtotal=Decimal("1500000.00"),
        )
        pedido = Pedido(
            id="ped_1",
            comprador_id="comp_1",
            direccion_envio="Calle 1 # 2 - 3",
            items=[item],
            monto_total=Decimal("1500000.00"),
        )
        pedido2 = pedido.confirmar_pago(referencia_pago="PAYG-123")
        assert pedido2.estado == "PAGADO"
        assert pedido2.fecha_pago is not None

    def test_cancelar_pedido_entregado(self):
        item = ItemPedido(
            id="it_1",
            producto_id="prod_1",
            producto_titulo="Laptop",
            variante_id=None,
            cantidad=1,
            precio_unitario=Decimal("1500000.00"),
            subtotal=Decimal("1500000.00"),
        )
        # No es un estado válido del dominio; se usa para forzar la excepción
        pedido = Pedido(
            id="ped_1",
            comprador_id="comp_1",
            direccion_envio="Calle 1 # 2 - 3",
            items=[item],
            monto_total=Decimal("1500000.00"),
            estado="ENTREGADO",
        )
        with pytest.raises(PedidoNoValido):
            pedido.cancelar(motivo="Cancelar por defecto")
