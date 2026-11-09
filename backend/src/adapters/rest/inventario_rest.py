"""
Adaptador REST de inventario (FastAPI).

Permite consultar el estado de stock de un producto en una bodega.
Este es un placeholder, para que se respete la estructura del backend.
"""

from fastapi import APIRouter, HTTPException, status

from ...domain.entities.inventario import Inventario

router = APIRouter(prefix="/inventario", tags=["inventario"])


@router.get(
    "/producto/{producto_id}/bodega/{bodega_id}",
    response_model=dict,
    summary="Obtener stock de un producto en una bodega",
)
async def obtener_stock(producto_id: str, bodega_id: str):
    """
    Consulta el stock de un producto en una bodega.
    """
    # Placeholder: en un futuro se consultará el repositorio de inventario.
    # Aquí mostramos un ejemplo de respuesta.
    return {
        "producto_id": producto_id,
        "bodega_id": bodega_id,
        "cantidad_disponible": 12,
        "cantidad_reservada": 2,
        "stock_total": 14,
    }


@router.post(
    "/",
    response_model=dict,
    summary="Registrar o actualizar inventario",
)
async def registrar_inventario(producto_id: str, bodega_id: str, cantidad: int):
    """
    Ajusta el inventario de un producto en una bodega.
    """
    if cantidad < 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="La cantidad debe ser >= 0.",
        )
    return {
        "mensaje": "Inventario registrado.",
        "producto_id": producto_id,
        "bodega_id": bodega_id,
        "cantidad_disponible": cantidad,
    }
