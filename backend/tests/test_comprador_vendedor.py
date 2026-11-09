"""
Pruebas de Comprador y Vendedor.
"""

import pytest

from src.domain.entities.comprador import Comprador
from src.domain.entities.vendedor import Vendedor
from src.domain.value_objects.errors import CompradorNoValido, VendedorNoValido


class TestComprador:
    def test_crear_comprador_activo(self):
        comp = Comprador(
            id="comp_1",
            nombre_completo="Ana García",
            correo_electronico="ana@email.com",
            telefono="3001234567",
            direccion_principal="Calle 1 # 2 - 3",
        )
        assert comp.puede_comprar is True

    def test_comprador_suspendido_no_puede_comprar(self):
        comp = Comprador(
            id="comp_1",
            nombre_completo="Ana García",
            correo_electronico="ana@email.com",
            telefono="3001234567",
            direccion_principal="Calle 1 # 2 - 3",
            estado_comercial="SUSPENDIDO",
        )
        assert comp.puede_comprar is False

    def test_comprador_agregar_direccion(self):
        comp = Comprador(
            id="comp_1",
            nombre_completo="Ana García",
            correo_electronico="ana@email.com",
            telefono="3001234567",
            direccion_principal="Calle 1 # 2 - 3",
        )
        comp2 = comp.agregar_direccion_adicional("Av. 1 # 2 - 3")
        assert len(comp2.direcciones_adicionales) == 1


class TestVendedor:
    def test_crear_vendedor_activo(self):
        v = Vendedor(
            id="ven_1",
            nombre_comercial="Tecnología SAS",
            nit_identificacion_fiscal="123456789-1",
            correo_electronico="contacto@tec.com",
            estado_vendedor="ACTIVO",
        )
        assert v.es_activo is True

    def test_vendedor_suspendido(self):
        v = Vendedor(
            id="ven_1",
            nombre_comercial="Tecnología SAS",
            nit_identificacion_fiscal="123456789-1",
            estado_vendedor="ACTIVO",
        )
        v2 = v.suspender()
        assert v2.estado_vendedor == "SUSPENDIDO"
