# Telemetry Fleet API

API REST asíncrona de alto rendimiento diseñada para la ingesta de telemetría vehicular, gestión de flotas y análisis de métricas operativas en tiempo real.

Construida con **FastAPI**, **SQLAlchemy 2.0**, **Pydantic v2** y autenticación segura basada en **OAuth2 + JWT**.

---

## Características Técnicas

* **Arquitectura Modular en Capas:** Separación estricta de responsabilidades (`routers`, `services`, `models`, `schemas`, `core`).
* **Seguridad & RBAC:** Control de acceso basado en roles (`admin` vs. `operator`) con hashing de contraseñas vía `bcrypt` y tokens `JWT`.
* **Modelado & Persistencia:** ORM con SQLAlchemy 2.0, relaciones 1:N optimizadas, eliminación en cascada e índices compuestos para consultas cronológicas de alta frecuencia.
* **Procesamiento Analítico:** Endpoints de agregación SQL (`AVG`, `MAX`, `COUNT`) para métricas de velocidad, temperatura y combustible.
* **Testing Automatizado:** Suite de pruebas E2E con `Pytest` y `TestClient` sobre bases de datos SQLite en memoria aisladas.
* **Documentación Interactiva:** OpenAPI (Swagger UI y ReDoc) autogenerada.

---

## Tecnologías Utilizadas

* **Lenguaje:** Python 3.10+
* **Framework:** FastAPI
* **Servidor ASGI:** Uvicorn
* **Validación & Serialización:** Pydantic v2
* **ORM:** SQLAlchemy 2.0
* **Seguridad:** Python-Jose (JWT), Bcrypt
* **Testing:** Pytest, HTTPX

---

## Estructura del Proyecto

```text
telemetry-fleet-api/
├── app/
│   ├── api/             # Endpoints y dependencias de autenticación (RBAC)
│   ├── core/            # Configuración de entorno y seguridad criptográfica
│   ├── db/              # Conexión al motor y sesión declarativa
│   ├── models/          # Entidades SQLAlchemy (User, Vehicle, TelemetryRecord)
│   ├── schemas/         # DTOs y validación con Pydantic
│   ├── services/        # Capa de lógica de negocio y queries analíticas
│   └── main.py          # Punto de entrada de la aplicación
├── tests/               # Fixtures y tests unitarios / integración
├── requirements.txt
└── README.md