
from datetime import datetime

from sqlalchemy import (
    Column, String, DateTime, DECIMAL, Text,
    ForeignKey, Integer
)
from sqlalchemy.orm import relationship

from .database import Base


class PedidoModel(Base):
    __tablename__ = "pedidos"

    id = Column(String(36), primary_key=True, index=True)
    comprador_id = Column(String(36), nullable=False)
    direccion_envio = Column(Text, nullable=False)
    monto_total = Column(DECIMAL(12, 2), nullable=False)
    estado = Column(
        String(30),
        nullable=False,
        default="PENDIENTE_PAGO"
    )
    fecha_creacion = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    items = relationship(
        "ItemPedidoModel",
        back_populates="pedido",
        cascade="all, delete-orphan"
    )


class ItemPedidoModel(Base):
    __tablename__ = "pedido_items"

    id = Column(String(36), primary_key=True, index=True)
    pedido_id = Column(
        String(36),
        ForeignKey("pedidos.id"),
        nullable=False
    )
    producto_id = Column(String(36), nullable=False)
    producto_titulo = Column(String(200), nullable=False)
    variante_id = Column(String(36), nullable=True)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(DECIMAL(12, 2), nullable=False)
    subtotal = Column(DECIMAL(12, 2), nullable=False)

    pedido = relationship(
        "PedidoModel",
        back_populates="items"
    )
