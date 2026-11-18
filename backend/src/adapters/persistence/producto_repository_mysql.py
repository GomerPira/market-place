
"""
ProductoRepositoryMySql — Adaptador de persistencia de productos.

Implementa ProductRepositoryOutputPort utilizando SQLAlchemy y MySQL.
Convierte las entidades del dominio en modelos de base de datos y viceversa.
"""

import json
from typing import List, Optional

from sqlalchemy.orm import Session

from src.domain.entities.product import Producto
from src.domain.entities.variante import VarianteProducto
from src.domain.value_objects import TipoProducto, EstadoProducto, Precio

from src.domain.ports.product_repository import ProductRepositoryOutputPort

from src.infrastructure.database.product_model import ProductModel
from src.infrastructure.database.variante_model import VarianteModel


class ProductoRepositoryMySql(ProductRepositoryOutputPort):

    def __init__(self, session: Session):
        self.db = session

    def guardar(self, producto: Producto) -> Producto:
        try:
            modelo = (
                self.db.query(ProductModel)
                .filter(ProductModel.id == producto.id)
                .first()
            )

            if modelo is None:
                modelo = ProductModel(id=producto.id)
                self.db.add(modelo)

            modelo.titulo = producto.titulo
            modelo.descripcion = producto.descripcion
            modelo.tipo = producto.tipo.value
            modelo.precio_base_cantidad = producto.precio_base.cantidad
            modelo.precio_base_moneda = producto.precio_base.moneda
            modelo.estado = producto.estado.value

            modelo.imagenes = (
                ",".join(producto.imagenes)
                if producto.imagenes else None
            )

            modelo.peso_kg = producto.peso_kg

            modelo.dimensiones = (
                json.dumps(producto.dimensiones)
                if producto.dimensiones else None
            )

            modelo.creado_en = producto.creado_en
            modelo.actualizado_en = producto.actualizado_en
            modelo.vendedor_id = producto.vendedor_id

            # Reemplazar las variantes del producto.
            modelo.variantes = [
                VarianteModel(
                    id=variante.id,
                    sku=variante.sku,
                    atributo=variante.atributo,
                    valor=variante.valor,
                    precio_adicional=variante.precio_adicional,
                )
                for variante in producto.variantes
            ]

            self.db.commit()
            self.db.refresh(modelo)

            return self._convertir_a_dominio(modelo)

        except Exception:
            self.db.rollback()
            raise

    def buscar_por_id(self, id_producto: str) -> Optional[Producto]:
        modelo = (
            self.db.query(ProductModel)
            .filter(ProductModel.id == id_producto)
            .first()
        )

        if modelo is None:
            return None

        return self._convertir_a_dominio(modelo)

    def listar(self, solo_activos: bool = True) -> List[Producto]:
        consulta = self.db.query(ProductModel)

        if solo_activos:
            consulta = consulta.filter(
                ProductModel.estado.in_(["PUBLICADO", "PENDIENTE"])
            )

        modelos = consulta.order_by(ProductModel.creado_en.desc()).all()

        return [
            self._convertir_a_dominio(modelo)
            for modelo in modelos
        ]

    def listar_por_vendedor(self, id_vendedor: str) -> List[Producto]:
        modelos = (
            self.db.query(ProductModel)
            .filter(ProductModel.vendedor_id == id_vendedor)
            .all()
        )

        return [
            self._convertir_a_dominio(modelo)
            for modelo in modelos
        ]

    def existe(self, id_producto: str) -> bool:
        return (
            self.db.query(ProductModel.id)
            .filter(ProductModel.id == id_producto)
            .first()
        ) is not None

    @staticmethod
    def _convertir_a_dominio(modelo: ProductModel) -> Producto:
        imagenes = (
            modelo.imagenes.split(",")
            if modelo.imagenes else None
        )

        dimensiones = (
            json.loads(modelo.dimensiones)
            if modelo.dimensiones else None
        )

        variantes = [
            VarianteProducto(
                id=variante.id,
                sku=variante.sku,
                atributo=variante.atributo,
                valor=variante.valor,
                precio_adicional=variante.precio_adicional,
            )
            for variante in modelo.variantes
        ]

        return Producto(
            id=modelo.id,
            titulo=modelo.titulo,
            descripcion=modelo.descripcion,
            tipo=TipoProducto(modelo.tipo),
            precio_base=Precio(
                moneda=modelo.precio_base_moneda,
                cantidad=modelo.precio_base_cantidad,
            ),
            estado=EstadoProducto(modelo.estado),
            imagenes=imagenes,
            peso_kg=modelo.peso_kg,
            dimensiones=dimensiones,
            creado_en=modelo.creado_en,
            actualizado_en=modelo.actualizado_en,
            variantes=variantes,
            vendedor_id=modelo.vendedor_id,
        )
