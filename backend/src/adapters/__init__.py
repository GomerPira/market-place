"""
Adaptadores de NexusMarket.
"""

from src.adapters.persistence import persistence_adapters
from src.adapters.rest import register_rest_adapters

adapters = [
    register_rest_adapters,
    persistence_adapters,
]