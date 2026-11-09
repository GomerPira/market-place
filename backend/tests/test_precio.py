"""
Pruebas de los objetos de valor (Precio, Estados, etc.).
"""

import pytest
from decimal import Decimal

from src.domain.value_objects.precio import Precio
from src.domain.value_objects.errors import PrecioNoValido


class TestPrecio:
    def test_crea_precio_valido(self):
        p = Precio(moneda="COP", cantidad=Decimal("1000.50"))
        assert p.moneda == "COP"
        assert p.cantidad == Decimal("1000.50")

    def test_precio_negativo_lanza_excepcion(self):
        with pytest.raises(PrecioNoValido):
            Precio(moneda="COP", cantidad=Decimal("-10.0"))

    def test_suma_precio(self):
        p1 = Precio(moneda="COP", cantidad=Decimal("1000.00"))
        p2 = Precio(moneda="COP", cantidad=Decimal("500.25"))
        resultado = p1 + p2
        assert isinstance(resultado, Precio)
        assert resultado.cantidad == Decimal("1500.25")

    def test_suma_con_monedas_diferentes_lanza_excepcion(self):
        p1 = Precio(moneda="COP", cantidad=Decimal("1000.00"))
        p2 = Precio(moneda="USD", cantidad=Decimal("500.00"))
        with pytest.raises(TypeError):
            p1 + p2

    def test_mul_escalar(self):
        p = Precio(moneda="COP", cantidad=Decimal("1000.00"))
        resultado = p * Decimal("2")
        assert resultado.cantidad == Decimal("2000.00")
