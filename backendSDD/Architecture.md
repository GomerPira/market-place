# Market Place — Backend Architecture

## 1. Propósito

Este documento describe la arquitectura técnica del backend de Market Place, las responsabilidades de sus capas y la forma en que se comunican para ejecutar las operaciones del sistema.

La arquitectura se basa en los principios de Domain-Driven Design (DDD) y Arquitectura Hexagonal.

## 2. Principios arquitectónicos

### 2.1. Separación de responsabilidades

Cada componente debe tener una responsabilidad definida.

- El dominio contiene las reglas del negocio.
- La aplicación coordina los casos de uso.
- Los puertos establecen contratos de comunicación.
- Los adaptadores conectan la aplicación con tecnologías externas.
- La infraestructura contiene configuraciones y recursos técnicos.

### 2.2. Independencia tecnológica

Las reglas del negocio no deben depender directamente de FastAPI, MySQL ni SQLAlchemy.

Esto permite cambiar una tecnología sin tener que reescribir el dominio.

### 2.3. Inversión de dependencias

La aplicación debe depender de abstracciones y contratos, no de implementaciones concretas.

Por ejemplo, `ProductService` depende del contrato `ProductRepository`, no directamente de una base de datos MySQL.

### 2.4. Responsabilidad única

Cada clase debe tener una función clara. La entidad `Product` administra las reglas propias de un producto, mientras que `ProductService` coordina los casos de uso relacionados con los productos.

## 3. Capas de la arquitectura

### 3.1. Dominio (Domain)

Es el núcleo del sistema. Contiene los conceptos y las reglas fundamentales del negocio.

Responsabilidades:

- Representar las entidades del negocio.
- Validar las reglas propias de las entidades.
- Definir los contratos que necesita el dominio para interactuar con otros componentes.

Componentes actuales:

- `entities/product.py`
- `ports/product_repository.py`
- `ports/product_use_cases.py`
- `value_objects/`

Ejemplo: la entidad `Product` impide que un producto tenga un precio menor o igual a cero.

### 3.2. Aplicación (Application)

Coordina las operaciones que el sistema permite realizar.

Responsabilidades:

- Ejecutar los casos de uso.
- Coordinar el dominio y los repositorios.
- Solicitar el almacenamiento o consulta de información.
- Aplicar reglas que correspondan al flujo de una operación.

Componente actual:

- `use_cases/product_service.py`

Ejemplo: cuando se solicita crear un producto, el servicio recibe el objeto `Product` y utiliza el repositorio para guardarlo.

### 3.3. Puertos (Ports)

Los puertos son contratos que definen las operaciones disponibles entre componentes.

#### Puerto de salida: ProductRepository

Archivo: `domain/ports/product_repository.py`

Define las operaciones de persistencia necesarias para los productos:

- `save()`: guardar un producto.
- `find_by_id()`: buscar un producto por identificador.
- `find_all()`: consultar todos los productos.

Una implementación en memoria y una implementación con MySQL pueden cumplir este mismo contrato.

#### Puerto de entrada: ProductUseCases

Archivo actual: `domain/ports/product_use_cases.py`

Define las operaciones que ofrece la aplicación:

- `create_product()`: crear un producto.
- `get_product()`: consultar un producto.
- `list_products()`: listar productos.

**Nota de diseño:** en una organización hexagonal más estricta, el puerto de entrada suele ubicarse en la capa de aplicación. En la estructura inicial del proyecto se encuentra en `domain/ports`; su ubicación podrá ajustarse posteriormente.

### 3.4. Adaptadores (Adapters)

Los adaptadores implementan la comunicación con el exterior.

#### Adaptador REST

Ubicación: `adapters/rest/`

Será responsable de recibir solicitudes HTTP, validar los datos de entrada, invocar los casos de uso y construir las respuestas HTTP.

Se implementará utilizando FastAPI.

#### Adaptador de persistencia

Ubicación: `adapters/persistence/`

Contiene implementaciones de los contratos de persistencia.

Componente actual:

- `in_memory_product_repository.py`

Esta implementación almacena productos en memoria y permite probar la lógica sin configurar una base de datos.

Más adelante se añadirá una implementación con MySQL.

### 3.5. Infraestructura (Infrastructure)

Ubicación: `infrastructure/`

Contendrá configuraciones y componentes técnicos necesarios para ejecutar el backend.

Por ejemplo:

- Configuración de conexión con MySQL.
- Configuración del motor y las sesiones de SQLAlchemy.
- Variables de entorno.
- Recursos técnicos de la aplicación.

## 4. Flujo de una solicitud

El siguiente flujo representa la comunicación prevista cuando un cliente solicita crear un producto mediante la API REST.

```text
Cliente HTTP
    |
    v
Adaptador REST (FastAPI)
    |
    v
ProductService
    |
    v
Puerto ProductRepository
    |
    v
Adaptador de persistencia
    |
    v
Base de datos
```

En la etapa actual, el repositorio en memoria reemplaza temporalmente la base de datos.

### Descripción del flujo

1. El cliente envía una solicitud HTTP.
2. El adaptador REST recibe y valida los datos.
3. El servicio de aplicación ejecuta el caso de uso.
4. El servicio solicita guardar el producto mediante `ProductRepository`.
5. El adaptador de persistencia almacena el producto.
6. El resultado regresa al servicio.
7. El adaptador REST devuelve una respuesta HTTP al cliente.

## 5. Dirección de las dependencias

Las dependencias deben apuntar hacia los componentes que contienen las reglas centrales del negocio.

La API REST puede depender de los casos de uso. El servicio puede depender de las entidades y de los contratos de persistencia. El adaptador de persistencia implementa el contrato definido para el repositorio.

El dominio no debe importar clases de FastAPI ni depender de SQLAlchemy.

## 6. Organización de carpetas

```text
backend/
├── main.py
├── src/
│   ├── domain/
│   │   ├── entities/
│   │   ├── value_objects/
│   │   └── ports/
│   ├── application/
│   │   └── use_cases/
│   ├── adapters/
│   │   ├── rest/
│   │   └── persistence/
│   └── infrastructure/
│       └── database/
└── tests/
```

La estructura se ampliará cuando se implementen nuevos módulos y funcionalidades.

## 7. Estrategia de pruebas

La arquitectura permite probar los componentes por separado.

- Pruebas unitarias: validan las reglas de entidades como `Product`.
- Pruebas de aplicación: verifican que los casos de uso coordinen correctamente las operaciones.
- Pruebas de adaptadores: comprueban la comunicación mediante HTTP y la persistencia.
- Pruebas de integración: verifican la interacción entre varios componentes.

## 8. Decisiones arquitectónicas

### DEC-001: Uso de FastAPI

Se utiliza FastAPI para construir la API REST en Python.

### DEC-002: Separación entre dominio y persistencia

Las entidades del dominio no dependen directamente de la base de datos.

### DEC-003: Uso de repositorios

La persistencia se abstrae mediante el contrato `ProductRepository`, permitiendo intercambiar implementaciones.

### DEC-004: Repositorio temporal en memoria

Se utiliza un repositorio en memoria durante el desarrollo inicial. No reemplaza la persistencia definitiva con MySQL.

## 9. Estado de implementación

| Componente | Estado |
|---|---|
| Entidad Product | Implementada |
| Contrato ProductRepository | Implementado |
| Contrato ProductUseCases | Implementado |
| ProductService | Implementado inicialmente |
| Repositorio en memoria | Implementado inicialmente |
| Adaptador REST de productos | Pendiente de integración |
| Persistencia con MySQL | Pendiente |
| Pruebas del servicio | Pendientes |

## 10. Evolución futura

La arquitectura podrá ampliarse para incluir vendedores, compradores, pedidos, autenticación, autorización y gestión de inventario, manteniendo las responsabilidades separadas y los contratos definidos entre componentes.
