# Market Place — Backend Overview

## 1. Introducción

El backend de Market Place es el componente encargado de administrar la lógica del negocio, gestionar los productos, procesar las solicitudes de los usuarios y comunicarse con la base de datos.

El proyecto se desarrolla en Python utilizando una arquitectura basada en Domain-Driven Design (DDD) y Arquitectura Hexagonal.

El objetivo es construir un backend organizado, mantenible, escalable y fácil de probar.

## 2. Objetivos del backend

- Gestionar los productos publicados en el marketplace.
- Permitir la creación, consulta, actualización y desactivación de productos.
- Administrar el inventario y el stock disponible.
- Exponer funcionalidades mediante una API REST.
- Persistir la información en una base de datos MySQL.
- Mantener separadas las reglas del negocio, los casos de uso y los detalles técnicos.

## 3. Tecnologías

| Tecnología | Responsabilidad |
|---|---|
| Python | Lenguaje de programación principal. |
| FastAPI | Construcción de la API REST. |
| MySQL | Base de datos relacional. |
| SQLAlchemy | Comunicación entre Python y la base de datos. |
| Pydantic | Validación y estructura de los datos recibidos por la API. |
| Pytest | Ejecución de pruebas automatizadas. |
| JWT | Autenticación basada en tokens, prevista para una etapa posterior. |
| Docker | Preparación de un entorno reproducible para ejecutar la aplicación. |

## 4. Arquitectura

El backend utiliza dos enfoques complementarios:

### 4.1. Domain-Driven Design (DDD)

DDD permite organizar el software alrededor del dominio del negocio.

En Market Place, el dominio incluye conceptos como:

- Product: producto ofrecido en el marketplace.
- Seller: vendedor que publica productos.
- Buyer: comprador que consulta y adquiere productos.
- Order: pedido realizado por un comprador.
- Inventory: disponibilidad y control de existencias.

Estos conceptos se desarrollarán progresivamente según las necesidades del proyecto.

### 4.2. Arquitectura Hexagonal

La Arquitectura Hexagonal separa la lógica principal del negocio de los mecanismos técnicos utilizados para comunicarse con el exterior.

Sus componentes principales son:

- Dominio: entidades y reglas del negocio.
- Aplicación: coordinación de los casos de uso.
- Puertos: contratos que definen cómo se comunican los componentes.
- Adaptadores: implementaciones que conectan la aplicación con tecnologías externas.
- Infraestructura: configuración y servicios técnicos, como la base de datos.

La lógica del dominio no debe depender directamente de FastAPI, SQLAlchemy ni de una base de datos específica.

## 5. Estructura del backend

La estructura actual y prevista es la siguiente:

```text
backend/
├── main.py
├── src/
│   ├── domain/
│   │   ├── entities/
│   │   │   └── product.py
│   │   ├── value_objects/
│   │   └── ports/
│   │       ├── product_repository.py
│   │       └── product_use_cases.py
│   ├── application/
│   │   └── use_cases/
│   │       └── product_service.py
│   ├── adapters/
│   │   ├── rest/
│   │   └── persistence/
│   │       └── in_memory_product_repository.py
│   └── infrastructure/
│       └── database/
└── tests/
    └── test_product.py
```

Esta estructura evolucionará a medida que se incorporen nuevos componentes.

## 6. Estado actual del desarrollo

### Implementado

- Configuración inicial de FastAPI.
- Endpoint inicial de bienvenida y endpoint de salud.
- Documentación interactiva disponible en `/docs`.
- Entidad Product con validaciones básicas.
- Pruebas automatizadas para la creación de productos y la validación del precio.
- Puertos para el repositorio de productos y los casos de uso.
- Servicio de aplicación para crear, consultar y listar productos.
- Implementación inicial de un repositorio en memoria.

### Pendiente de implementar o verificar

- Integración completa del repositorio con la API REST.
- Endpoints para crear, consultar y listar productos.
- Validación de solicitudes y respuestas mediante Pydantic.
- Persistencia real con MySQL y SQLAlchemy.
- Pruebas de integración.
- Autenticación y autorización.
- Configuración con Docker.
- Gestión completa de vendedores, compradores, pedidos e inventario.

## 7. Criterios de diseño

1. Separar las responsabilidades de cada capa.
2. Mantener las reglas del negocio independientes de la tecnología.
3. Utilizar puertos para definir contratos entre componentes.
4. Implementar adaptadores intercambiables.
5. Automatizar las pruebas de las reglas del dominio.
6. Documentar las decisiones arquitectónicas a medida que se implementen.

## 8. Relación con la documentación SDD existente

La carpeta `SDD/Domain` contiene la documentación del dominio del negocio, incluyendo el modelo de dominio, los servicios, los objetos de valor y los puertos definidos inicialmente.

La carpeta `backendSDD` documenta cómo se implementará técnicamente ese diseño en Python.

Ambas documentaciones deben mantenerse alineadas. Si la implementación requiere modificar una regla del negocio o un contrato definido en el SDD original, el cambio debe revisarse y documentarse.

## 9. Próximas etapas

1. Completar el repositorio en memoria y conectarlo con el servicio.
2. Exponer los casos de uso mediante FastAPI.
3. Probar los endpoints.
4. Integrar MySQL con SQLAlchemy.
5. Añadir validaciones, autenticación y pruebas.
6. Documentar la configuración y el despliegue.
