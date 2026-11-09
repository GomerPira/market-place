"""
Adaptadores de NexusMarket.
"""

from src.adapters.rest import rest_routers
from src.adapters.persistence import persistence_adapters

adapters = [
    rest_routers,
    persistence_adapters,
]
