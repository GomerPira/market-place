"""
ProductUseCasesApp - Implementación de los casos de uso de producto.

Esta clase coordina el dominio y los repositorios.
No conoce de HTTP (FastAPI), ni de MySQL, ni de SQLAlchemy.
Solo usa los contratos definidos en src.domain.ports.
"""
from decimal import Decimal
from typing import Any, Dict, List, Optional

from ...domain.value_objects import (
    TipoProducto,
    EstadoProducto,
    TipoNoValido,
    EstadoNoValido,
    PrecioNoValido,
)
from ...domain.value_objects.precio import Precio
from ...domain.entities.product import Producto
from ...domain.ports.product_repository import ProductRepositoryOutputPort


class ProductUseCases:
    """
    Casos de uso de productos.
    Los casos de uso delegan a un repositorio (que puede ser en memoria, MySQL, etc.).
    """

    def __init__(self, repo: ProductRepositoryOutputPort):
        self.repo = repo

    def registrar(self, titulo, descripcion, tipo, precio_base, vendedor_id=None):
        # Aquí va la lógica de registro (validación, generación de ID, etc.)
                    # Por ahora, creamos un producto simple y lo guardamos.

        producto = Producto(
            id=f"prod_{self._generar_id()}"[:36],
            titulo=titulo,
            descripcion=descripcion,
            tipo=TipoProducto(tipo),
            precio_base=Precio(
                moneda="COP",
                cantidad=Decimal(str(precio_base))
            ),
            estado=EstadoProducto.DRAFT,
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

    def actualizar(self, id_producto: str, data: Dict[str, Any]) -> Optional[Producto]:
        """
        Actualizar un producto existente.

        El caso de uso:
        1. Busca el producto existente.
        2. Valida los datos proporcionados.
        3. Construye una nueva instancia del dominio.
        4. Solicita al repositorio que lo actualice.

        Retorna el producto actualizado o None si no existe.
        """
        producto = self.repo.buscar_por_id(id_producto)
        if producto is None:
            return None

        # Extrae campos opcionales del cuerpo de la solicitud
        titulo = data.get('titulo')
        descripcion = data.get('descripcion')
        tipo = data.get('tipo')
        precio_base = data.get('precio_base')
        estado = data.get('estado')
        vendedor_id = data.get('vendedor_id')
        imagenes = data.get('imagenes')
        peso_kg = data.get('peso_kg')
        dimensiones = data.get('dimensiones')
        variantes = data.get('variantes')

        # Valida que los campos presentes sean compatibles con el dominio
        if tipo is not None and not isinstance(tipo, TipoProducto):
            try:
                tipo = TipoProducto(str(tipo).upper())
            except ValueError as exc:
                raise TipoNoValido(f'Tipo de producto no válido: {tipo}') from exc

        if estado is not None and not isinstance(estado, EstadoProducto):
            try:
                estado = EstadoProducto(str(estado).upper())
            except ValueError as exc:
                raise EstadoNoValido(f'Estado de producto no válido: {estado}') from exc

        if precio_base is not None:
            try:
                precio_base = Precio(
                    moneda=precio_base.get('moneda', 'COP'),
                    cantidad=Decimal(str(precio_base.get('cantidad', 0))),
                )
            except (TypeError, ValueError) as exc:
                raise PrecioNoValido(f'Precio base no válido: {precio_base}') from exc

        if titulo is not None and not isinstance(titulo, str):
            raise TipoNoValido('El campo titulo debe ser una cadena de texto.')

        if descripcion is not None and not isinstance(descripcion, str):
            raise TipoNoValido('El campo descripcion debe ser una cadena de texto.')

        # Construye los argumentos solo con los campos presentes en data
        # Construye los argumentos según los campos enviados

        campos = [
            'titulo', 'descripcion', 'tipo', 'precio_base', 'estado',
            'vendedor_id', 'imagenes', 'peso_kg', 'dimensiones', 'variantes'
        ]

        valores = {
            'titulo': titulo,
            'descripcion': descripcion,
            'tipo': tipo,
            'precio_base': precio_base,
            'estado': estado,
            'vendedor_id': vendedor_id,
            'imagenes': imagenes,
            'peso_kg': peso_kg,
            'dimensiones': dimensiones,
            'variantes': variantes,
        }

        args = {campo: valores[campo] for campo in campos if campo in data}
                
        producto_actualizado = producto.actualizar(**args)

        # Usa el contrato específico de actualización
        return self.repo.actualizar(producto_actualizado)

    def eliminar(self, id_producto: str) -> Optional[Producto]:
        """
        Elimina lógicamente un producto.
        """
        producto = self.repo.buscar_por_id(id_producto)

        if producto is None:
            return None

        producto_eliminado = producto.eliminarlo()

        return self.repo.actualizar(producto_eliminado)

    @staticmethod
    def _generar_id():
        import uuid
        return uuid.uuid4().hex
