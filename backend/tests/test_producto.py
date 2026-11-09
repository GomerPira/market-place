"""
Pruebas de Producto.
"""

import pytest

from src.domain.entities.product import Producto
from src.domain.value_objects.precio import Precio
from src.domain.value_objects.estado_producto import EstadoProducto
from src.domain.value_objects.tipo_producto import TipoProducto
from src.domain.value_objects.errors import PrecioNoValido, TipoNoValido


class TestProducto:
    def test_crea_producto_basico(self):
        p = Producto(
            id="prod_1",
            titulo="Laptop",
            descripcion="Una laptop",
            tipo=TipoProducto.FISICO,
            precio_base=Precio(moneda="COP", cantidad=Decimal("1500000.00")),
            estado=EstadoProducto.PUBLICADO,
        )
        assert p.titulo == "Laptop"
        assert p.es_fisico is True
        assert p.es_activo is True
        assert p.es_digital is False

    def test_precio_base_se_valida_negativo(self):
        with pytest.raises(PrecioNoValido):
            Producto(
                id="prod_1",
                titulo="Laptop",
                descripcion="Una laptop",
                tipo=TipoProducto.FISICO,
                precio_base=Precio(moneda="COP", cantidad=Decimal("-1000.00")),
                estado=EstadoProducto.PUBLICADO,
            )

    def test_agregar_variante(self):
        p = Producto(
            id="prod_1",
            titulo="Remera",
            descripcion="Remera de algodón",
            tipo=TipoProducto.FISICO,
            precio_base=Precio(moneda="COP", cantidad=Decimal("50000.00")),
            estado=EstadoProducto.PUBLICADO,
        )
        variante = Producto(
            id="var_1",
            titulo="Talla L",
            descripcion="Variante",
            tipo=TipoProducto.FISICO,
            precio_base=Precio(moneda="COP", cantidad=Decimal("0.00")),
            estado=EstadoProducto.PUBLICADO,
        )
        p2 = p.agregar_variante(variante)
        assert len(p2.variantes) == 1
