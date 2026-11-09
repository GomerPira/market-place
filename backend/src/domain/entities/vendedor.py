"""
Vendedor — Representa a un proveedor comercial.

Cada vendedor tiene:
- NIT / documento fiscal
- Dirección (comercial) opcional
- Lista de productos
- Estado operativo
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from ..value_objects import (
    VendedorNoValido,
    EstadoNoValido,
    NitNoValido,
    DocumentoNoValido,
)


@dataclass
class Vendedor:
    """
    Representa a un vendedor/proveedor de productos.
    """

    id: str
    nombre_comercial: str
    nit_identificacion_fiscal: str
    correo_electronico: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    estado_vendedor: str = "ACTIVO"
    productos: List[str] = field(default_factory=list)

    def __post_init__(self):
        if self.estado_vendedor not in ("ACTIVO", "SUSPENDIDO", "INACTIVO"):
            raise EstadoNoValido(
                f"Estado de vendedor no válido: {self.estado_vendedor}."
            )
        if self.es_nit():
            if not self._es_nit_valido(self.nit_identificacion_fiscal):
                raise NitNoValido("El NIT no parece válido.")
        else:
            if not self._es_documento_valido(self.nit_identificacion_fiscal):
                raise DocumentoNoValido(
                    "El documento de identificación no parece válido."
                )

    def _es_nit_valido(self, nit: str) -> bool:
        """
        Regla muy básica para verificar un NIT colombiano.
        Un NIT legítimo suele ser: XXXXX-XXX o XXXXXXXX (solo dígitos).
        Aquí usamos una validación simple; la real se ajustaría con un algoritmo.
        """
        nit_limpio = nit.replace("-", "").replace(" ", "")
        return nit_limpio.isdigit() and 8 <= len(nit_limpio) <= 10

    def _es_documento_valido(self, documento: str) -> bool:
        return len(documento.replace(" ", "")) >= 6

    @property
    def es_nit(self) -> bool:
        """
        Si el documento termina en '-' o tiene más de 10 dígitos,
        se considera un NIT.
        """
        return "-" in self.nit_identificacion_fiscal or len(self.nit_identificacion_fiscal.replace("-", "")) > 10

    def suspender(self) -> "Vendedor":
        return self._cambiar_estado("SUSPENDIDO")

    def reactivar(self) -> "Vendedor":
        return self._cambiar_estado("ACTIVO")

    def deshabilitar(self) -> "Vendedor":
        return self._cambiar_estado("INACTIVO")

    def _cambiar_estado(self, nuevo_estado: str) -> "Vendedor":
        if nuevo_estado not in ("ACTIVO", "SUSPENDIDO", "INACTIVO"):
            raise EstadoNoValido(f"Estado de vendedor no válido: {nuevo_estado}.")
        return Vendedor(
            id=self.id,
            nombre_comercial=self.nombre_comercial,
            nit_identificacion_fiscal=self.nit_identificacion_fiscal,
            correo_electronico=self.correo_electronico,
            telefono=self.telefono,
            direccion=self.direccion,
            estado_vendedor=nuevo_estado,
            productos=list(self.productos),
        )

    @property
    def es_activo(self) -> bool:
        return self.estado_vendedor == "ACTIVO"

    @property
    def productos_id(self) -> List[str]:
        return list(self.productos)
