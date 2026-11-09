"""
Product — Entidad del dominio de productos (NexusMarket).

El Producto está compuesto por:
- Un producto base (físico o digital)
- Cero o más variantes

Esta clase contiene únicamente la lógica del dominio:
- Validación de reglas de negocio
- Inmutabilidad de los datos básicos (donde corresponda)
- Representación de un producto dentro del catálogo

No importa si estamos en memoria, MySQL, PostgreSQL, etc.
Nadie debe llamar a métodos de SQLAlchemy desde aquí.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from ..value_objects import TipoProducto, EstadoProducto, PrecioNoValido, EstadoNoValido
from ..value_objects.precio import Precio


@dataclass
class Producto:
    """
    Representa un producto publicado en el catálogo de NexusMarket.

    Además de un producto base, puede tener variantes (talla, color, modelo...).
    Cada variante puede tener su propio precio adicional.
    """

    id: str
    titulo: str
    descripcion: str
    tipo: TipoProducto
    precio_base: Precio
    estado: EstadoProducto = EstadoProducto.DRAFT
    imagenes: Optional[List[str]] = None
    peso_kg: Optional[Decimal] = None
    dimensiones: Optional[dict] = None
    creado_en: datetime = field(default_factory=datetime.utcnow)
    actualizado_en: Optional[datetime] = None
    variantes: List["VarianteProducto"] = field(default_factory=list)
    vendedor_id: Optional[str] = None

    def __post_init__(self):
        """Valida la entidad al crearse o modificarla."""
        # La validación se centraliza en value objects, pero mantenemos
        # comprobaciones defensivas en la entidad también.
        if self.estado not in EstadoProducto:
            raise EstadoNoValido(
                f"Estado no válido: {self.estado}. "
                f"Valores permitidos: {[e.value for e in EstadoProducto]}"
            )

        if self.tipo not in TipoProducto:
            raise TipoNoValido(
                f"Tipo no válido: {self.tipo}. "
                f"Valores permitidos: {[t.value for t in TipoProducto]}"
            )

        self.precio_base = Precio(self.precio_base.moneda, self.precio_base.cantidad)

    def activar(self) -> "Producto":
        """Publica el producto (pasa de DRAFT a PUBLICADO)."""
        return self._cambiar_estado(EstadoProducto.PUBLICADO)

    def suspender(self) -> "Producto":
        """Pausa la publicación del producto."""
        return self._cambiar_estado(EstadoProducto.SUSPENDIDO)

    def eliminarlo(self) -> "Producto":
        """Marca el producto como eliminado."""
        return self._cambiar_estado(EstadoProducto.DESCONTINUADO)

    def _cambiar_estado(self, nuevo_estado: EstadoProducto) -> "Producto":
        nuevo = Producto(
            id=self.id,
            titulo=self.titulo,
            descripcion=self.descripcion,
            tipo=self.tipo,
            precio_base=self.precio_base,
            estado=nuevo_estado,
            imagenes=self.imagenes,
            peso_kg=self.peso_kg,
            dimensiones=self.dimensiones,
            creado_en=self.creado_en,
            actualizado_en=datetime.utcnow(),
            variantes=list(self.variantes),
            vendedor_id=self.vendedor_id,
        )
        return nuevo

    def agregar_variante(self, variante: "VarianteProducto") -> "Producto":
        """Añade una variante y devuelve una copia con el cambio."""
        nuevas_variantess = list(self.variantes) + [variante]
        return Producto(
            id=self.id,
            titulo=self.titulo,
            descripcion=self.descripcion,
            tipo=self.tipo,
            precio_base=self.precio_base,
            estado=self.estado,
            imagenes=self.imagenes,
            peso_kg=self.peso_kg,
            dimensiones=self.dimensiones,
            creado_en=self.creado_en,
            actualizado_en=datetime.utcnow(),
            variantes=nuevas_variantess,
            vendedor_id=self.vendedor_id,
        )

    def calcular_precio_variante(self, variante: "VarianteProducto") -> Precio:
        """
        Calcula el precio final de una variante.
        El precio base + el precio adicional de la variante.
        """
        return self.precio_base + variante.precio_adicional

    @property
    def es_activo(self) -> bool:
        """Un producto está activo si no está en estado BORRADOR, SUSPENDIDO ni ELIMINADO."""
        return self.estado in (
            EstadoProducto.PUBLICADO,
            EstadoProducto.PENDIENTE,
        )

    @property
    def es_fisico(self) -> bool:
        return self.tipo == TipoProducto.FISICO

    @property
    def es_digital(self) -> bool:
        return self.tipo == TipoProducto.DIGITAL
