"""
Repositorios de aplicación (adaptadores de persistencia).

Aquí se define cómo se guardan los datos antes de pasar a la implementación
final con SQLAlchemy/MySQL.
"""

from typing import List, Optional

from src.domain.entities.product import Producto


class ProductoRepoInMemory:
    """
    Repositorio en memoria para productos.
    Es una implementación simple para probar la arquitectura.
    """

    def __init__(self):
        self._productos: dict[str, Producto] = {}

    def guardar(self, producto: Producto) -> Producto:
        self._productos[producto.id] = producto
        return producto

    def buscar_por_id(self, id_producto: str) -> Optional[Producto]:
        return self._productos.get(id_producto)

    def listar(self, solo_activos: bool = True) -> List[Producto]:
        if solo_activos:
            return [
                p for p in self._productos.values()
                if p.estado.value in ("DRAFT", "PENDIENTE", "PUBLICADO")
            ]

        return list(self._productos.values())

    def listar_por_vendedor(self, id_vendedor: str) -> List[Producto]:
        return [
            p for p in self._productos.values()
            if p.vendedor_id == id_vendedor
        ]

    def existe(self, id_producto: str) -> bool:
        return id_producto in self._productos

    def actualizar(self, producto: Producto) -> Producto:
        """
        Actualiza un producto existente en el repositorio en memoria.
        Si el producto no existe, lanza un KeyError.
        """
        if producto.id not in self._productos:
            raise KeyError(f"Producto no encontrado: {producto.id}")
        self._productos[producto.id] = producto
        return producto
