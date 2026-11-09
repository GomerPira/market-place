"""
Pruebas de Inventario y Carrito.
"""

import pytest
from decimal import Decimal

from src.domain.entities.inventario import Inventario
from src.domain.entities.carrito import Carrito, ItemCarrito
from src.domain.value_objects.errors import InventarioNoValido


class TestInventario:
    def test_crear_inventario_valido(self):
        inv = Inventario(
            id="inv_1",
            producto_id="prod_1",
            bodega_id="bodega_1",
            cantidad_disponible=10,
            cantidad_reservada=2,
        )
        assert inv.cantidad_disponible == 10
        assert inv.stock_total == 12

    def test_reserva_excede_disponible(self):
        inv = Inventario(
            id="inv_1",
            producto_id="prod_1",
            bodega_id="bodega_1",
            cantidad_disponible=5,
            cantidad_reservada=0,
        )
        with pytest.raises(InventarioNoValido):
            inv.reservar(cantidad=10)

    def test_agregar_stock(self):
        inv = Inventario(
            id="inv_1",
            producto_id="prod_1",
            bodega_id="bodega_1",
            cantidad_disponible=5,
            cantidad_reservada=0,
        )
        inv2 = inv.agregar_stock(3)
        assert inv2.cantidad_disponible == 8
        assert inv2.stock_total == 8


class TestCarrito:
    def test_crear_carrito(self):
        item = ItemCarrito(
            id="it_1",
            producto_id="prod_1",
            producto_titulo="Laptop",
            variante_id=None,
            cantidad=1,
            precio_unitario=Decimal("1500000.00"),
        )
        carrito = Carrito(id="car_1", comprador_id="comp_1", items=[item])
        assert carrito.total == Decimal("1500000.00")
        assert carrito.esta_vacio is False

    def test_agregar_item_a_carrito(self):
        item1 = ItemCarrito(
            id="it_1",
            producto_id="prod_1",
            producto_titulo="Laptop",
            variante_id=None,
            cantidad=1,
            precio_unitario=Decimal("2500000.00"),
        )
        item2 = ItemCarrito(
            id="it_2",
            producto_id="prod_2",
            producto_titulo="Mouse",
            variante_id=None,
            cantidad=1,
            precio_unitario=Decimal("70000.00"),
        )
        carrito = Carrito(id="car_1", comprador_id="comp_1", items=[item1])
        carrito2 = carrito.agregar(item2)
        assert carrito2.cantidad_items == 2
        assert carrito2.total == Decimal("2570000.00")
