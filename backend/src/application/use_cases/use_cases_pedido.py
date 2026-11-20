
from decimal import Decimal
from uuid import uuid4

from src.domain.entities.pedido import Pedido, ItemPedido


class PedidoUseCases:

    def __init__(self, pedido_repo, producto_repo):
        self.pedido_repo = pedido_repo
        self.producto_repo = producto_repo

    def crear_pedido(
        self,
        comprador_id: str,
        direccion_envio: str,
        items: list
    ) -> Pedido:

        if not comprador_id or not direccion_envio:
            raise ValueError(
                "El comprador y la dirección son obligatorios."
            )

        if not items:
            raise ValueError("El pedido debe tener productos.")

        pedido_items = []
        total = Decimal("0.00")

        for dato in items:
            producto_id = dato.get("producto_id")
            cantidad = dato.get("cantidad")
            variante_id = dato.get("variante_id")

            if not isinstance(cantidad, int) or cantidad <= 0:
                raise ValueError("La cantidad debe ser un entero positivo.")

            producto = self.producto_repo.buscar_por_id(producto_id)

            if producto is None:
                raise ValueError(
                    f"No existe el producto {producto_id}."
                )

            if producto.estado.value != "PUBLICADO":
                raise ValueError(
                    f"El producto {producto.titulo} no está publicado."
                )

            variante = None
            precio_unitario = producto.precio_base.cantidad

            if variante_id:
                variante = next(
                    (
                        v for v in producto.variantes
                        if v.id == variante_id
                    ),
                    None
                )

                if variante is None:
                    raise ValueError(
                        f"La variante {variante_id} no pertenece al producto."
                    )

                precio_calculado = producto.calcular_precio_variante(
                    variante
                )

                precio_unitario = (
                    precio_calculado.cantidad
                    if hasattr(precio_calculado, "cantidad")
                    else precio_calculado
                )

            subtotal = precio_unitario * cantidad
            total += subtotal

            pedido_items.append(
                ItemPedido(
                    id=str(uuid4()),
                    producto_id=producto.id,
                    producto_titulo=producto.titulo,
                    variante_id=variante_id,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                    subtotal=subtotal
                )
            )

        pedido = Pedido(
            id=str(uuid4()),
            comprador_id=comprador_id,
            direccion_envio=direccion_envio,
            items=pedido_items,
            monto_total=total,
            estado="PENDIENTE_PAGO"
        )

        return self.pedido_repo.guardar(pedido)
