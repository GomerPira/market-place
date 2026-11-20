
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import List, Optional

from src.infrastructure.database.database import get_session
from src.adapters.persistence.pedido_repository_mysql import PedidoRepositoryMySql
from src.adapters.persistence.producto_repository_mysql import ProductoRepositoryMySql
from src.application.use_cases.use_cases_pedido import PedidoUseCases


router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


class ItemPedidoRequest(BaseModel):
    producto_id: str
    cantidad: int = Field(gt=0)
    variante_id: Optional[str] = None


class CrearPedidoRequest(BaseModel):
    comprador_id: str
    direccion_envio: str
    items: List[ItemPedidoRequest]


@router.post("/")
def crear_pedido(
    datos: CrearPedidoRequest,
    session: Session = Depends(get_session)
):
    pedido_repo = PedidoRepositoryMySql(session)
    producto_repo = ProductoRepositoryMySql(session)

    caso_uso = PedidoUseCases(
        pedido_repo,
        producto_repo
    )

    try:
        pedido = caso_uso.crear_pedido(
            comprador_id=datos.comprador_id,
            direccion_envio=datos.direccion_envio,
            items=[
                item.model_dump()
                for item in datos.items
            ]
        )

        return {
            "mensaje": "Pedido creado correctamente",
            "pedido": {
                "id": pedido.id,
                "comprador_id": pedido.comprador_id,
                "direccion_envio": pedido.direccion_envio,
                "estado": pedido.estado,
                "monto_total": str(pedido.monto_total),
                "items": [
                    {
                        "producto_id": item.producto_id,
                        "producto_titulo": item.producto_titulo,
                        "cantidad": item.cantidad,
                        "precio_unitario": str(item.precio_unitario),
                        "subtotal": str(item.subtotal)
                    }
                    for item in pedido.items
                ]
            }
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
