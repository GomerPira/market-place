"""
Excepciones de dominio (Domain Errors).

Estas excepciones representan reglas de negocio incumplidas.
No son errores técnicos (no apuntan a bug de código), sino a violación de
reglas del negocio: precio incorrecto, estado inválido, venta de stock insuficiente, etc.

¿Para qué sirven?
- Separar errores de dominio de errores de infraestructura.
- Mostrar errores claros al frontend y a los tests.
- Mantener el dominio independiente de HTTP o BD.
"""


class DominioError(Exception):
    """Error base de dominio. No debería usarse directamente."""
    pass


class ProductoNoValido(DominioError):
    """El producto no cumple las reglas del dominio."""
    pass


class TipoNoValido(DominioError):
    """El tipo de producto no es válido."""
    pass


class EstadoNoValido(DominioError):
    """El estado no es válido."""
    pass


class PrecioNoValido(DominioError):
    """El precio no es válido."""
    pass


class ItemNoValido(DominioError):
    """El ítem del carrito no es válido."""
    pass


class PedidoNoValido(DominioError):
    """El pedido no es válido."""
    pass


class InventarioNoValido(DominioError):
    """El inventario no es válido."""
    pass


class BodegaNoValido(DominioError):
    """La bodega no es válida."""
    pass


class CompradorNoValido(DominioError):
    """El comprador no es válido."""
    pass


class VendedorNoValido(DominioError):
    """El vendedor no es válido."""
    pass


class UsuarioNoValido(DominioError):
    """El usuario no es válido."""
    pass


class DireccionNoValida(DominioError):
    """La dirección no es válida."""
    pass


class NitNoValido(DominioError):
    """El NIT no es válido."""
    pass


class DocumentoNoValido(DominioError):
    """El documento de identidad no es válido."""
    pass
