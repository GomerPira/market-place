"""
InventarioRepositoryMySql — Adaptador de persistencia para inventario (MySQL).

Este archivo implementa el puerto `InventarioRepositoryOutputPort`.
Al igual que el repositorio de productos, es un placeholder mientras se
desarrolla el modelo de SQLAlchemy.
"""

from typing import List, Optional

from src.domain.entities.inventario import Inventario
from src.domain.ports.inventario_repository import InventarioRepositoryOutputPort
from src.application.repositories import ProductoRepoInMemory


class InventarioRepositoryMySql(InventarioRepositoryOutputPort):
    """
    Implementación del repositorio de inventario usando MySQL.
    Actualmente usamos una estructura en memoria por simplificación.
    """

    def __init__(self):
        # Temporal: repositorio en memoria
        self._inventarios: dict[str, Inventario] = {}

    def guardar(self, inventario: Inventario) -> Inventario:
        self._inventarios[inventario.id] = inventario
        return inventario

    def buscar_por_producto_y_bodega(
        self, producto_id: str, bodega_id: str
    ) -> Optional[Inventario]:
        for inv in self._inventarios.values():
            if inv.producto_id == producto_id and inv.bodega_id == bodega_id:
                return inv
        return None

    def listar_por_producto(self, producto_id: str) -> List[Inventario]:
        return [
            inv for inv in self._inventarios.values()
            if inv.producto_id == producto_id
        ]

    def listar_activos(self) -> List[Inventario]:
        return list(self._inventarios.values())
