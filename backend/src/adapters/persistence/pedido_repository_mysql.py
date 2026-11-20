
from typing import List, Optional

from sqlalchemy.orm import Session

from src.domain.entities.pedido import Pedido, ItemPedido
from src.infrastructure.database.pedido_model import (
    PedidoModel,
    ItemPedidoModel
)


class PedidoRepositoryMySql:

    def __init__(self, session: Session):
        self.db = session

    def guardar(self, pedido: Pedido) -> Pedido:
        try:
            modelo = (
                self.db.query(PedidoModel)
                .filter(PedidoModel.id == pedido.id)
                .first()
            )

            if modelo is None:
                modelo = PedidoModel(id=pedido.id)
                self.db.add(modelo)

            modelo.comprador_id = pedido.comprador_id
            modelo.direccion_envio = pedido.direccion_envio
            modelo.monto_total = pedido.monto_total
            modelo.estado = pedido.estado

            modelo.items = [
                ItemPedidoModel(
                    id=item.id,
                    producto_id=item.producto_id,
                    producto_titulo=item.producto_titulo,
                    variante_id=item.variante_id,
                    cantidad=item.cantidad,
                    precio_unitario=item.precio_unitario,
                    subtotal=item.subtotal
                )
                for item in pedido.items
            ]

            self.db.commit()
            self.db.refresh(modelo)

            return self._convertir_a_dominio(modelo)

        except Exception:
            self.db.rollback()
            raise

    def buscar_por_id(self, pedido_id: str) -> Optional[Pedido]:
        modelo = (
            self.db.query(PedidoModel)
            .filter(PedidoModel.id == pedido_id)
            .first()
        )

        if modelo is None:
            return None

        return self._convertir_a_dominio(modelo)

    def listar_por_comprador(self, comprador_id: str) -> List[Pedido]:
        modelos = (
            self.db.query(PedidoModel)
            .filter(PedidoModel.comprador_id == comprador_id)
            .order_by(PedidoModel.fecha_creacion.desc())
            .all()
        )

        return [
            self._convertir_a_dominio(modelo)
            for modelo in modelos
        ]

    @staticmethod
    def _convertir_a_dominio(modelo: PedidoModel) -> Pedido:
        items = [
            ItemPedido(
                id=item.id,
                producto_id=item.producto_id,
                producto_titulo=item.producto_titulo,
                variante_id=item.variante_id,
                cantidad=item.cantidad,
                precio_unitario=item.precio_unitario,
                subtotal=item.subtotal
            )
            for item in modelo.items
        ]

        return Pedido(
            id=modelo.id,
            comprador_id=modelo.comprador_id,
            direccion_envio=modelo.direccion_envio,
            items=items,
            monto_total=modelo.monto_total,
            estado=modelo.estado,
            fecha_creacion=modelo.fecha_creacion
        )
