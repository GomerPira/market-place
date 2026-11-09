# NexusMarket — Backend (Python)

API REST del Marketplace NexusMarket, implementada con **Python**, **FastAPI** y **SQLAlchemy**, siguiendo **DDD** y la **Arquitectura Hexagonal**.

## Estructura del proyecto

```text
backend/
├── main.py                  # Punto de entrada
├── src/
│   ├── domain/
│   │   ├── entities/        # Producto, VarianteProducto, Inventario, Pedido, Comprador, Vendedor
│   │   ├── value_objects/   # Estados, tipos y objetos inmutables
│   │   └── ports/           # Contratos (repositorios e interfaces)
│   ├── application/
│   │   └── use_cases/       # Lógica de casos de uso
│   ├── adapters/
│   │   ├── rest/            # Adaptadores HTTP (FastAPI)
│   │   └── persistence/     # Implementaciones de repositorios (MySQL)
│   └── infrastructure/      # Servicios técnicos (base de datos, caché, etc.)
├── tests/                   # Pruebas automatizadas
├── scripts/                 # Scripts de seeding y utilidades
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

## Tecnologías

| Tecnología | Responsabilidad |
| --- | --- |
| Python 3.12 | Lenguaje principal |
| FastAPI | Construcción de la API REST |
| SQLAlchemy 2.x | Mapeado y persistencia con MySQL |
| Pydantic | Validación de datos de entrada/salida |
| Pytest | Ejecución de pruebas automatizadas |
| Docker / Docker Compose | Entorno reproducible y levantamiento en contenedores |

## Correr local (sin Docker)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Editar .env con los valores adecuados
uvicorn main:app --reload --port 8000
```

La API estará disponible en http://localhost:8000.

## Correr con Docker

La imagen levanta MySQL y MongoDB automáticamente. No necesitas instalarlos.

```bash
docker compose up --build -d
```

Luego:
- Backend: http://localhost:8000
- MySQL (host): localhost:3306
- MongoDB (host): localhost:27017

Comprobar estado:
```bash
docker compose ps
docker compose logs -f bank-api
curl http://localhost:8000/health
```

## Documentación

- `/docs` → Interfaz interactiva de Swagger
- `/redoc` → Documentación alternativa
- `/health` → Healthcheck

## Pruebas

```bash
pytest
```

## Estado del backend

- ✅ Estructura Hexagonal (domain, application, adapters, infrastructure)
- ✅ Configuración de FastAPI e `uvicorn`
- ✅ Endpoints de bienvenida y salud
- ✅ Conexión a MySQL mediante entorno
- ✅ Contratos de puertos (input/output ports)
- ⏳ Endpoints CRUD de productos y catálogo
- ⏳ Agregados de inventario, pedidos, facturación y logística
- ⏳ Pruebas unitarias e integración
