"""
Adaptador REST de productos (FastAPI).

Este archivo conecta la API HTTP con los casos de uso de la app.
El adaptador recibe la petición HTTP, la valida, llama al caso de uso del
dominio, y devuelve una respuesta HTTP.

Es el único archivo que debería estar preocupado por los códigos HTTP
(200, 404, 422, etc.) y por los serializadores.
"""

from fastapi import APIRouter, HTTPException, status

from ...application.use_cases.use_cases_producto import ProductUseCases
from ...domain.entities.product import Producto
from ...domain.value_objects.errors import ProductoNoValido, TipoNoValido, EstadoNoValido

router = APIRouter(prefix="/productos", tags=["productos"])


def crear_producto_use_case(repo):
    """
    Crea el caso de uso de producto con un repositorio.
    """
    return ProductUseCases(repo)


@router.post(
    "/",
    response_model=dict,
    summary="Crear un producto",
    description="Permite a un vendedor registrar un producto en el catálogo.",
)
async def crear_producto(
    titulo: str,
    descripcion: str,
    tipo: str,
    precio_base: float,
    vendedor_id: str | None = None,
):
    """
    Crear un producto (dummy por ahora).
    """
    try:
        # Aquí normalmente validaríamos que vendedor_id exista y esté activo.
        # Como aún no tenemos la autenticación, no validamos vendedor_id.
        if tipo not in ("FISICO", "DIGITAL"):
            raise TipoNoValido(f"Tipo no válido: {tipo}. Valores permitidos: FISICO, DIGITAL.")

        use_case = ProductUseCases(repo=None)  # En el futuro se inyecta el repositorio real
        producto = use_case.registrar(titulo, descripcion, tipo, precio_base, vendedor_id)
        return {"mensaje": "Producto creado", "id": producto.id}
    except TipoNoValido as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ProductoNoValido as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/",
    response_model=list,
    summary="Listar productos",
    description="Obtiene la lista de productos del catálogo.",
)
async def listar_productos(solo_activos: bool = True):
    """
    Listar todos los productos.
    """
    # Dado que aún no tenemos la BD, devolvemos un mensaje de ejemplo.
    # En la implementación final, se llama al caso de uso con el repositorio real.
    return [
        {
            "id": "demo-1",
            "titulo": "Laptop Dell XPS 13",
            "descripcion": "Computadora portátil de alta gama.",
            "tipo": "FISICO",
            "precio_base": 2500000.00,
            "estado": "PUBLICADO",
            "creado_en": "2026-01-15T00:00:00",
        }
    ]


@router.get(
    "/{id_producto}",
    response_model=dict,
    summary="Consultar un producto",
    description="Obtiene la información de un producto por su ID.",
)
async def obtener_producto(id_producto: str):
    """
    Consultar un producto por ID.
    """
    # Por ahora devolvemos un producto de ejemplo.
    return {
        "id": id_producto,
        "titulo": "Laptop Dell XPS 13",
        "descripcion": "Computadora portátil de alta gama.",
        "tipo": "FISICO",
        "precio_base": 2500000.00,
        "estado": "PUBLICADO",
        "creado_en": "2026-01-15T00:00:00",
    }
