
from src.infrastructure.database.database import Base, engine
from src.infrastructure.database.product_model import ProductModel

Base.metadata.create_all(bind=engine)

print("Tabla products creada correctamente.")
    
