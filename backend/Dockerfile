# NexusMarket Backend — Docker
#
# Estado del proyecto:
# - Python 3.12 (solo se permite 3.12)
# - FastAPI + uvicorn como servidor
# - SQLAlchemy + Pydantic
#
# Referencia de uso:
#   docker build -t nexusmarket-backend .
#   docker run --rm -p 8000:8000 --env-file .env nexusmarket-backend
#
# Levantamiento completo (backend + MySQL + MongoDB):
#   docker compose up --build -d

FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Sistema de dependencias y paquetes que FastAPI necesita
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar y construir entorno virtual dentro del contenedor
COPY requirements.txt .
RUN python -m venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY src ./src
COPY main.py .

# Exponer puerto de la API
EXPOSE 8000

# Comando por defecto
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
