
from decimal import Decimal

from src.domain.entities.product import Product


def test_crear_producto():
    product = Product(
        id=None,
        name="Teclado mecánico",
        description="Teclado para computador",
        price=Decimal("150000"),
        stock=10,
        seller_id=1
    )

    assert product.name == "Teclado mecánico"
    assert product.price == Decimal("150000")
    assert product.stock == 10


def test_no_permitir_precio_cero():
    try:
        Product(
            id=None,
            name="Mouse",
            description="Mouse inalámbrico",
            price=Decimal("0"),
            stock=5,
            seller_id=1
        )
        assert False, "Debió rechazar el precio"
    except ValueError:
        pass
