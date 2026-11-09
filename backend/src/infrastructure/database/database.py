"""
Servicio de conexión a la base de datos (infrastructure).

Este módulo configura SQLAlchemy y la sesión.
El uso del `settings` permite leer las variables de entorno (o el archivo .env)
sin que el dominio tenga que saber de ello.

Configuración esperada:
    DATABASE_HOST=localhost
    DATABASE_PORT=3306
    DATABASE_NAME=nexusmarket
    DATABASE_USER=root
    DATABASE_PASSWORD=root_password
"""

from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from ...domain.value_objects.errors import DominioError


# ---------------------------------------------------------------------------
# Lectura de variables de entorno (simplificado: se lee directamente).
# Si se necesita .env, se puede usar `python-dotenv` o `pydantic-settings`.
# ---------------------------------------------------------------------------


class Settings:
    def __init__(self):
        self._db_user = self._leer_vars("DATABASE_USER", "root")
        self._db_password = self._leer_vars("DATABASE_PASSWORD", "root_password")
        self._db_host = self._leer_vars("DATABASE_HOST", "localhost")
        self._db_port = self._leer_vars("DATABASE_PORT", "3306")
        self._db_name = self._leer_vars("DATABASE_NAME", "nexusmarket")
        self._db_url = (
            f"mysql+pymysql://{self._db_user}:{self._db_password}"
            f"@{self._db_host}:{self._db_port}/{self._db_name}"
        )
        self._server_port = self._leer_vars("SERVER_PORT", "8000")

    @staticmethod
    def _leer_vars(nombre: str, valor_por_defecto: str) -> str:
        """
        Lee una variable de entorno.
        Si no está definida, usa el valor por defecto.
        """
        import os
        valor = os.getenv(nombre)
        return valor if valor is not None else valor_por_defecto


_settings = Settings()

DATABASE_URL = _settings._db_url
SERVER_PORT = int(_settings._server_port)

# -------------------------------------------------------------------------
# Engine y sesión
# -------------------------------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,          # Verifica que la BD esté viva antes de usar la conexión
    pool_recycle=3600,           # Reconexión automática cada hora
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# -------------------------------------------------------------------------
# Modelo declarativo (mapeado a tablas)
# -------------------------------------------------------------------------

Base = declarative_base()


def get_session():
    """
    Función retornable de sesión (singleton simple).
    Usada por FastAPI dependientes, por ejemplo.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
