"""
Capa de aplicación de NexusMarket (casos de uso y repositorios).
"""

from src.application.use_cases.use_cases_producto import ProductUseCases
from src.application.repositories import ProductoRepoInMemory

application = [
    ProductUseCases,
    ProductoRepoInMemory,
]
