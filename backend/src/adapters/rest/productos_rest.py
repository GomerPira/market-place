
"""
Adaptador REST de productos (FastAPI).

Conecta las peticiones HTTP con los casos de uso
y el repositorio MySQL.
"""

from decimal import Decimal
from typing import Any, Dict, List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ...application.use_cases.use_cases_producto import ProductUseCases
from ...adapters.persistence.producto_repository_mysql import ProductoRepositoryMySql
from ...infrastructure.database.database import get_session
from ...domain.value_objects.errors import (
    ProductoNoValido,
    TipoNoValido,
    EstadoNoValido,
    PrecioNoValido,
)

router = APIRouter(prefix="/productos", tags=["productos"])


def crear_producto_use_case(session: Session):
    repo = ProductoRepositoryMySql(session)
    return ProductUseCases(repo)


def convertir_producto(producto):
    return {
        "id": producto.id,
        "titulo": producto.titulo,
        "descripcion": producto.descripcion,
        "tipo": producto.tipo.value,
        "precio_base": float(producto.precio_base.cantidad),
        "moneda": producto.precio_base.moneda,
        "estado": producto.estado.value,
        "imagenes": producto.imagenes,
        "peso_kg": (
            float(producto.peso_kg)
            if producto.peso_kg is not None else None
        ),
        "dimensiones": producto.dimensiones,
        "creado_en": producto.creado_en.isoformat(),
        "actualizado_en": (
            producto.actualizado_en.isoformat()
            if producto.actualizado_en else None
        ),
        "vendedor_id": producto.vendedor_id,
        "variantes": [
            {
                "id": variante.id,
                "sku": variante.sku,
                "atributo": variante.atributo,
                "valor": variante.valor,
                "precio_adicional": float(variante.precio_adicional),
            }
            for variante in producto.variantes
        ],
    }



@router.post(
    "/",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un producto",
)
async def crear_producto(
    titulo: str,
    descripcion: str,
    tipo: str,
    precio_base: Decimal,
    vendedor_id: str | None = None,
    session: Session = Depends(get_session),
):
    try:
        use_case = crear_producto_use_case(session)

        producto = use_case.registrar(
            titulo,
            descripcion,
            tipo,
            precio_base,
            vendedor_id,
        )

        return {
            "mensaje": "Producto creado correctamente",
            "producto": convertir_producto(producto),
        }

    except TipoNoValido as e:
        raise HTTPException(status_code=422, detail=str(e))
    except (ProductoNoValido, EstadoNoValido) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/",
    response_model=list,
    summary="Listar productos",
)
async def listar_productos(
    solo_activos: bool = True,
    session: Session = Depends(get_session),
):
    use_case = crear_producto_use_case(session)

    productos = use_case.listar(solo_activos=solo_activos)

    return [
        convertir_producto(producto)
        for producto in productos
    ]


@router.get(
    "/{id_producto}",
    response_model=dict,
    summary="Consultar un producto",
)
async def obtener_producto(
    id_producto: str,
    session: Session = Depends(get_session),
):
    use_case = crear_producto_use_case(session)

    producto = use_case.buscar(id_producto)

    if producto is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado",
        )

    return convertir_producto(producto)


class ActualizarProductoBody(BaseModel):
    """
    Modelo Pydantic para recibir los datos de actualización de un producto.

    Todos los campos son opcionales. Los valores omitidos se conservan.
    """

    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    tipo: Optional[str] = None
    precio_base: Optional[Dict[str, Any]] = None
    estado: Optional[str] = None
    vendedor_id: Optional[str] = None
    imagenes: Optional[List[str]] = None
    peso_kg: Optional[Union[Decimal, str]] = None
    dimensiones: Optional[Dict[str, Any]] = None
    variantes: Optional[List[Dict[str, Any]]] = None


@router.put(
    "/{id_producto}",
    response_model=dict,
    summary="Actualizar un producto existente",
    status_code=status.HTTP_200_OK,
)
async def actualizar_producto(
    id_producto: str,
    body: ActualizarProductoBody,
    session: Session = Depends(get_session),
):
    try:
        use_case = crear_producto_use_case(session)

        data = body.model_dump(exclude_unset=True)

        producto = use_case.actualizar(id_producto, data)

        if producto is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado",
            )

        return {
            "mensaje": "Producto actualizado correctamente",
            "producto": convertir_producto(producto),
        }

    except TipoNoValido as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except PrecioNoValido as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except (ProductoNoValido, EstadoNoValido) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete(
    "/{id_producto}",
    response_model=dict,
    summary="Eliminar un producto",
    status_code=status.HTTP_200_OK,
)
async def eliminar_producto(
    id_producto: str,
    session: Session = Depends(get_session),
):
    use_case = crear_producto_use_case(session)

    producto = use_case.eliminar(id_producto)

    if producto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado",
        )

    return {
        "mensaje": "Producto eliminado correctamente",
        "producto": convertir_producto(producto),
    }

