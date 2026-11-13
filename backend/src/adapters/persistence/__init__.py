"""
Adaptadores de persistencia (MySQL) de NexusMarket.
"""

from src.adapters.persistence.producto_repository_mysql import ProductoRepositoryMySql
from src.adapters.persistence.inventario_repository_mysql import InventarioRepositoryMySql

persistence_adapters = [
    ProductoRepositoryMySql,
    InventarioRepositoryMySql,
]