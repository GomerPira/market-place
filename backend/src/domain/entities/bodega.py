"""
Bodega — Espacio físico donde se almacena inventario.

Puede ser:
- Bodega del Marketplace (es_bodega_marketplace = True)
- Bodega de un vendedor (es_bodega_marketplace = False)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..value_objects import BodegaNoValido, EstadoNoValido


@dataclass
class Bodega:
    """
    Representa un espacio físico de almacenamiento.
    """

    id: str
    nombre: str
    direccion: str
    es_bodega_marketplace: bool
    estado: str = "ACTIVA"
    id_vendedor_propietario: Optional[str] = None

    def __post_init__(self):
        if self.estado not in ("ACTIVA", "EN_MANTENIMIENTO", "SUSPENDIDA"):
            raise EstadoNoValido(
                f"Estado de bodega no válido: {self.estado}."
            )
        if not self.nombre or not self.nombre.strip():
            raise BodegaNoValido("El nombre de la bodega es obligatorio.")
        if not self.direccion or not self.direccion.strip():
            raise BodegaNoValido("La dirección de la bodega es obligatoria.")

    def activar(self) -> "Bodega":
        return _cambiar_estado(self, "ACTIVA")

    def poner_en_mantenimiento(self) -> "Bodega":
        return _cambiar_estado(self, "EN_MANTENIMIENTO")

    def suspender(self) -> "Bodega":
        return _cambiar_estado(self, "SUSPENDIDA")

    @property
    def es_activa(self) -> bool:
        return self.estado == "ACTIVA"
