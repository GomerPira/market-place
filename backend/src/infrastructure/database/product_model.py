"""
Modelo SQLAlchemy de Producto (MySQL).

Este archivo mapea la tabla `productos` a un objeto de SQLAlchemy.
Es un "adaptador de persistencia": traduce el dominio (Producto) a
filas de MySQL y viceversa.

No contiene reglas de negocio. Solo estructura de tabla.
"""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, DECIMAL, Enum, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class ProductModel(Base):
    """
    Tabla `productos` en MySQL.
    """

    __tablename__ = "productos"

    id = Column(String(36), primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=False)
    tipo = Column(Enum("FISICO", "DIGITAL", name="tipo_producto"), nullable=False)
    precio_base_cantidad = Column(DECIMAL(12, 2), nullable=False)
    precio_base_moneda = Column(String(3), nullable=False, default="COP")
    estado = Column(Enum("DRAFT", "PENDIENTE", "PUBLICADO", "SUSPENDIDO", "DESCONTINUADO", name="estado_producto"), nullable=False)
    imagenes = Column(String(400), nullable=True)  # separada por coma
    peso_kg = Column(DECIMAL(10, 3), nullable=True)
    dimensiones = Column(Text, nullable=True)  # JSON serializado
    creado_en = Column(DateTime, default=lambda: datetime.utcnow(), nullable=False)
    actualizado_en = Column(DateTime, nullable=True)
    vendedor_id = Column(String(36), nullable=True)

    # Relación unidireccional con variantes (versión simple)
    variantes = relationship(
        "VarianteModel",
        back_populates="producto",
        cascade="all, delete-orphan",
    )

    @property
    def precio_base(self):
        """
        Devuelve un objeto Precio (domain) a partir del precio en MySQL.
        """
        from ...domain.value_objects.precio import Precio
        return Precio(
            moneda=self.precio_base_moneda,
            cantidad=Decimal(self.precio_base_cantidad),
        )

    @property
    def estado_producto(self):
        return self.estado
