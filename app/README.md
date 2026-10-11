# Biblioteca Inteligente - API Backend
## Alineación con la Teoría General de Sistemas (TGS)

Este proyecto fue diseñado conceptualmente como un sistema abierto y dinámico:

Modularidad e Interdependencia: Los componentes (Usuarios, Libros, Préstamos) operan como subsistemas interconectados que forman un todo coherente.

Gestión de Fronteras (Boundaries): Las fronteras del sistema están claramente delimitadas y aisladas mediante contenedores Docker, controlando qué entra y qué sale.

Homeostasis y Resiliencia: La lógica de conexión maneja reintentos y verificaciones de salud para mantener el equilibrio operativo ante fallos en la base de datos.

Negentropía: Se mantiene la integridad transaccional estricta para evitar el desorden o la degradación de los datos a lo largo del tiempo.

## Guía de Instalación y Ejecución con Docker
1. Clonar el repositorio
Puedes clonar el proyecto desde su repositorio oficial en GitHub ejecutando el siguiente comando en tu terminal:

- git clone [https://github.com/LeonardoKepp/smart_library_api.git](https://github.com/LeonardoKepp/smart_library_api.git)
cd smart_library_api

2. Configurar las variables de entorno
Duplica el archivo de ejemplo y asínale el nombre .env:

- cp .env.example .env

3. Levantar el sistema completo
Ejecuta el siguiente comando para construir y encender los contenedores de la base de datos y la API de manera simultánea:

- docker compose up --build

4. Probar la API
Una vez que los servicios estén activos, abre tu navegador web e ingresa a la documentación interactiva generada automáticamente:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

Para detener el sistema en cualquier momento, presiona Ctrl + C en tu terminal o ejecuta:

- docker compose down.

## Tecnologías y Stack Utilizado

* **Lenguaje:** Python 3.12
* **Framework Web:** FastAPI (con validación de datos mediante Pydantic)
* **Base de Datos:** PostgreSQL
* **ORM:** SQLAlchemy (modo asíncrono)
* **Contenedorización:** Docker & Docker Compose
* **Control de Versiones:** Git & GitHub

---

<details>
<summary><b> Ver Estructura del Proyecto</b></summary>

```text
smart_library_api/
│
├── app/
│   ├── database/     # Configuración y conexión asíncrona a PostgreSQL
│   ├── models/       # Modelos SQLAlchemy (Libros, Usuarios, Préstamos)
│   ├── routers/      # Endpoints REST CRUD para cada módulo
│   ├── schemas/      # Esquemas Pydantic de entrada y salida de datos
│   └── main.py       # Archivo principal de inicio de FastAPI
│
├── .env.example      # Plantilla de variables de entorno
├── .gitignore        # Archivos y carpetas excluidas del control de versiones
├── Dockerfile        # Configuración de la imagen del contenedor de la API
└── docker-compose.yml # Orquestador de servicios (API + PostgreSQL)

