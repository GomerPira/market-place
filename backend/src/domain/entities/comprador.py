"""
Comprador — Representa a una persona que compra productos.

El comprador puede tener:
- Dirección principal de entrega
- Direcciones adicionales
- Productos en carrito
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from ..value_objects import (
    CompradorNoValido,
    EstadoNoValido,
    DireccionNoValida,
)


@dataclass
class Comprador:
    """
    Representa al usuario que compra en el marketplace.
    """

    id: str
    nombre_completo: str
    correo_electronico: str
    telefono: str
    direccion_principal: str
    direcciones_adicionales: List[str] = field(default_factory=list)
    estado_comercial: str = "ACTIVO"

    def __post_init__(self):
        if self.estado_comercial not in ("ACTIVO", "SUSPENDIDO", "INACTIVO"):
            raise EstadoNoValido(
                f"Estado comercial no válido: {self.estado_comercial}."
            )
        if not self.nombre_completo or not self.nombre_completo.strip():
            raise CompradorNoValido("El nombre completo del comprador es obligatorio.")
        if "@" not in self.correo_electronico:
            raise CompradorNoValido("El correo electrónico no es válido.")

    def agregar_direccion_adicional(self, direccion: str) -> "Comprador":
        if not direccion or not direccion.strip():
            raise DireccionNoValida("La dirección adicional no puede estar vacía.")
        nuevo = Comprador(
            id=self.id,
            nombre_completo=self.nombre_completo,
            correo_electronico=self.correo_electronico,
            telefono=self.telefono,
            direccion_principal=self.direccion_principal,
            direcciones_adicionales=list(self.direcciones_adicionales) + [direccion],
            estado_comercial=self.estado_comercial,
        )
        return nuevo

    def quitar_direccion_adicional(self, direccion: str) -> "Comprador":
        nuevo = Comprador(
            id=self.id,
            nombre_completo=self.nombre_completo,
            correo_electronico=self.correo_electronico,
            telefono=self.telefono,
            direccion_principal=self.direccion_principal,
            direcciones_adicionales=[
                d for d in self.direcciones_adicionales if d != direccion
            ],
            estado_comercial=self.estado_comercial,
        )
        return nuevo

    @property
    def tiene_direccion_principal(self) -> bool:
        return bool(self.direccion_principal and self.direccion_principal.strip())

    @property
    def puede_comprar(self) -> bool:
        """
        Un comprador puede comprar si está en estado ACTIVO.
        """
        return self.estado_comercial == "ACTIVO"

    def suspender(self) -> "Comprador":
        if self.estado_comercial == "ACTIVO":
            nuevo = Comprador(
                id=self.id,
                nombre_completo=self.nombre_completo,
                correo_electronico=self.correo_electronico,
                telefono=self.telefono,
                direccion_principal=self.direccion_principal,
                direcciones_adicionales=list(self.direcciones_adicionales),
                estado_comercial="SUSPENDIDO",
            )
            return nuevo
        return self

    def reactivar(self) -> "Comprador":
        if self.estado_comercial in ("SUSPENDIDO", "INACTIVO"):
            nuevo = Comprador(
                id=self.id,
                nombre_completo=self.nombre_completo,
                correo_electronico=self.correo_electronico,
                telefono=self.telefono,
                direccion_principal=self.direccion_principal,
                direcciones_adicionales=list(self.direcciones_adicionales),
                estado_comercial="ACTIVO",
            )
            return nuevo
        return self
