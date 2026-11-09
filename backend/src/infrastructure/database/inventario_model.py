"""
Modelo SQLAlchemy de Inventario (MySQL).

Mapea la tabla `inventarios`.
Esta tabla guarda las existencias de un producto o variante dentro de una bodega.
"""

from decimal import Decimal

from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.dialects.mysql import DECIMAL
from sqlalchemy.orm import relationship

from .database import Base


class InventarioModel(Base):
    """
    Tabla `inventarios` en MySQL.
    """

    __tablename__ = "inventarios"

    id = Column(String(36), primary_key=True, index=True)
    producto_id = Column(String(36), ForeignKey("productos.id", ondelete="CASCADE"), nullable=False)
    bodega_id = Column(String(36), nullable=False)
    cantidad_disponible = Column(Integer, nullable=False)
    cantidad_reservada = Column(Integer, default=0, nullable=False)
    variante_id = Column(String(36), nullable=True)

    # Relación con producto
    producto = relationship("ProductModel", backref="inventarios")

    @property
    def stock_total(self) -> int:
        """
        Devuelve el total físico disponible + reservado.
        """
        return self.cantidad_disponible + self.cantidad_reservada

    @property
    def hay_stock(self) -> bool:
        return self.cantidad_disponible > 0
