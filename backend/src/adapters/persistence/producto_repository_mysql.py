"""
ProductoRepositoryMySql — Adaptador de persistencia para productos (MySQL).

Este archivo implementa el puerto `ProductRepositoryOutputPort`.
Su objetivo es adaptar las consultas SQL a la capa de dominio.
"""
from typing import Optional

from src.domain.entities.product import Producto
from src.domain.ports.product_repository import ProductRepositoryOutputPort
from src.application.repositories import ProductoRepoInMemory


class ProductoRepositoryMySql(ProductRepositoryOutputPort):
    """
    Implementación del repositorio de productos usando MySQL.
    Actualmente usamos una implementación en memoria como placeholder.
    Cuando esté listo el modelo SQLAlchemy, aquí se realizarán consultas reales.
    """

    def __init__(self):
        # Temporal: repositorio en memoria
        self._repo = ProductoRepoInMemory()

    def guardar(self, producto: Producto) -> Producto:
        return self._repo.guardar(producto)

    def buscar_por_id(self, id_producto: str) -> Optional[Producto]:
        return self._repo.buscar_por_id(id_producto)

    def listar(self, solo_activos: bool = True) -> list[Producto]:
        return self._repo.listar(solo_activos=solo_activos)

    def listar_por_vendedor(self, id_vendedor: str) -> list[Producto]:
        return self._repo.listar_por_vendedor(id_vendedor)

    def existe(self, id_producto: str) -> bool:
        return self._repo.existe(id_producto)
