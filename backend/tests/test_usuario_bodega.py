"""
Pruebas de Usuario y Bodega.
"""

import pytest

from src.domain.entities.usuario import Usuario
from src.domain.entities.bodega import Bodega


class TestUsuario:
    def test_usuario_activo_puede_acceder(self):
        u = Usuario(
            id="usr_1",
            correo_electronico="admin@nexusmarket.com",
            contrasena_hash="$2b$12$xxx",  # dummy
            rol="ADMINISTRADOR",
            estado="ACTIVO",
        )
        assert u.puede_acceder is True

    def test_usuario_bloqueado_no_puede_acceder(self):
        u = Usuario(
            id="usr_1",
            correo_electronico="admin@nexusmarket.com",
            contrasena_hash="$2b$12$xxx",  # dummy
            rol="ADMINISTRADOR",
            estado="BLOQUEADO",
        )
        assert u.puede_acceder is False


class TestBodega:
    def test_crear_bodega_activa(self):
        b = Bodega(
            id="bodega_1",
            nombre="Almacén Principal",
            direccion="Calle 1 # 2 - 3",
            es_bodega_marketplace=True,
            estado="ACTIVA",
        )
        assert b.es_activa is True

    def test_bodega_en_mantenimiento(self):
        b = Bodega(
            id="bodega_1",
            nombre="Almacén Principal",
            direccion="Calle 1 # 2 - 3",
            es_bodega_marketplace=True,
            estado="EN_MANTENIMIENTO",
        )
        b2 = b.activar()
        assert b2.estado == "ACTIVA"
