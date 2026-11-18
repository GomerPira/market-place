"""
Modelo SQLAlchemy de VarianteProducto (MySQL).

Mapea la tabla variantes y establece su relación con productos.
"""

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.mysql import DECIMAL
from sqlalchemy.orm import relationship

from .database import Base


class VarianteModel(Base):
    """
    Tabla variantes en MySQL.
    """

    __tablename__ = "variantes"

    id = Column(String(36), primary_key=True, index=True)
    producto_id = Column(
        String(36),
        ForeignKey("productos.id", ondelete="CASCADE"),
        nullable=False
    )
    sku = Column(String(100), nullable=False, unique=True)
    atributo = Column(String(100), nullable=False)
    valor = Column(String(150), nullable=False)
    precio_adicional = Column(DECIMAL(12, 2), nullable=False, default=0)

    producto = relationship(
        "ProductModel",
        back_populates="variantes"
    )

