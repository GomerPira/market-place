"""
ProductUseCasesApp — Implementación de los casos de uso de producto.

Esta clase coordina el dominio y los repositorios.
No conoce de HTTP (FastAPI), ni de MySQL, ni de SQLAlchemy.
Solo usa los contratos definidos en `src.domain.ports`.
"""

from typing import List, Optional

from ...domain.ports.product_repository import ProductRepositoryOutputPort
from ...domain.entities.product import Producto
from ...domain.ports import ProductRepositoryOutputPort, RegistrarProductoInputPort, ListarProductosInputPort, BuscarProductoPorIdInputPort


class ProductUseCases:
    """
    Casos de uso de productos.
    Los casos de uso delegan a un repositorio (que puede ser en memoria, MySQL, etc.).
    """

    def __init__(self, repo: ProductRepositoryOutputPort):
        self.repo = repo

    def registrar(self, titulo, descripcion, tipo, precio_base, vendedor_id=None):
        """
        Registra un producto.
        """
        # Aquí va la lógica de registro (validación, generación de ID, etc.)
        # Por ahora, creamos un producto simple y lo guardamos.
        producto = Producto(
            id=f"prod_{self._generar_id()}"[:36],
            titulo=titulo,
            descripcion=descripcion,
            tipo=tipo,
            precio_base=precio_base,
            estado="DRAFT",
            vendedor_id=vendedor_id,
            imagenes=None,
            peso_kg=None,
            dimensiones=None,
            variantes=[],
        )
        return self.repo.guardar(producto)

    def listar(self, solo_activos=True):
        """
        Listar productos.
        """
        return self.repo.listar(solo_activos=solo_activos)

    def buscar(self, id_producto: str) -> Optional[Producto]:
        """
        Buscar un producto por ID.
        """
        return self.repo.buscar_por_id(id_producto)

    @staticmethod
    def _generar_id():
        import uuid
        return uuid.uuid4().hex
