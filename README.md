# Fiction Express - Prueba Técnica Backend (Django + DRF)

## Descripción del Proyecto
API RESTful construida con Django Rest Framework para la gestión de un catálogo de libros, con control de acceso basado en roles (RBAC), autenticación JWT, y despliegue automatizado en AWS EC2 usando Docker y GitHub Actions.

#### Nota sobre el idioma de la documentación

La documentación generada con Swagger/OpenAPI, así como los docstrings en el código fuente y los nombres de variables/clases, están redactados en inglés por una cuestión de buenas prácticas técnicas y estandarización internacional en proyectos de desarrollo.

---

## Tecnologías utilizadas
- Python 3.10
- Django 4+
- Django REST Framework
- MySQL / SQLite (según entorno)
- Docker + Docker Compose
- Nginx (como proxy reverso)
- Gunicorn (como WSGI server)
- GitHub Actions (CI/CD)
- AWS EC2 (Ubuntu 22.04)

---

## Características Implementadas

### Usuarios
- CRUD completo
- Campos: nombre de usuario, email, contraseña, rol (lector/editor)
- Autenticación JWT (usando `simplejwt`)

### Libros
- CRUD completo con RBAC:
  - Editores pueden crear/editar/eliminar
  - Lectores solo pueden leer
- Campos: id, título, autor, contenido (páginas), fechas de creación y actualización

### Seguridad y control de acceso
- JWT con refresh tokens y blacklist
- Decoradores para verificar permisos según rol

### Documentación
- Swagger (`/api/schema/swagger-ui/`)
- Redoc (`/api/schema/redoc/`)

### Tests automatizados
- Se ejecutan en cada push/tag con GitHub Actions
- Basados en `unittest` y Django `TestCase`
- Uso de base de datos SQLite en entorno de CI

---

## Despliegue en AWS

### Infraestructura:
- EC2 Ubuntu 22.04 con Docker y Docker Compose
- Nginx como proxy reverso (puerto 80)
- Gunicorn sirviendo la app Django (puerto 8000 interno)

### Acceso a la app:

- http://http://51.21.132.18/

---

## Automatización (CI/CD)

### Desencadenado por:
- `push` a `main`
- `push` de tags (`v1.0.0`, `v1.1.0`, etc.)

### Acciones realizadas:
1. Clona el repo
2. Instala dependencias
3. Ejecuta tests con `python manage.py test`
4. Si todo pasa, se conecta vía SSH a EC2:
   - Hace `git pull`
   - Reinicia contenedores con Docker Compose

### Secrets usados:
- `EC2_SSH_PRIVATE_KEY`: clave privada para acceder a EC2

---

## Instrucciones para desarrollo local

### Requisitos previos
- Tener Docker y Docker Compose instalados

### Pasos para correr la aplicación localmente:

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu_usuario/fictionexpress_catalog.git
cd fictionexpress_catalog

# 2. Crear archivo de entorno
cp .env.example .env  # o crear uno manual con tus variables

# 3. Construir y levantar los contenedores
docker-compose up -d --build

# 4. Ejecutar migraciones
docker-compose exec app python manage.py migrate

# 5. Crear superusuario (opcional)
docker-compose exec app python manage.py createsuperuser

# 6. Acceder a la aplicación
http://localhost:8000/

# 7. Correr tests
docker-compose exec app pytest -v
```

## Changelog

### v1.0.0 

- CRUD de usuarios y libros
- RBAC por roles (editor/lector)
- JWT Auth + blacklist
- Swagger + Redoc habilitados
- Despliegue en AWS EC2
- CI/CD con tests y despliegue automatizado


## Escalabilidad

Para escalar la aplicación de FictionExpress ante un crecimiento masivo de usuarios y eventos de lectura, propongo los siguientes cambios arquitectónicos:

#### 1. Arquitectura basada en eventos

Para evitar que el backend Django se sobrecargue con el almacenamiento de eventos, se implementaría una arquitectura asíncrona:

- **Frontend / App móvil**: envía eventos al backend (ej. lectura de una página).
- **API Django (REST)**: encola los eventos en RabbitMQ/Kafka en lugar de procesarlos directamente.
- **Worker Celery**: consume los eventos y guarda las métricas de lectura.
- **MongoDB o TimescaleDB**: almacena los eventos para análisis posterior (engagement, abandono, duración).
- **Dashboards / BI Tools**: visualizan los datos de lectura en tiempo real.


### Formato de evento (ejemplo MongoDB)
```json
{
  "user_id": 42,
  "book_id": 12,
  "page_id": 3,
  "started_at": "2025-03-21T10:30:00Z",
  "duration_seconds": 55,
  "device": "mobile"
}
```

#### 2. Caché de lecturas

Para mejorar la velocidad de respuesta de la API, se podría implementar una capa de caché con Redis: 

- Implementar Redis como capa de caché.
- Almacenar temporalmente las páginas de los libros más leídas.
- Configurar un TTL (time-to-live) para descartar páginas inactivas.
- Usar una política de reemplazo LRU (Least Recently Used) para mantener las más consultadas.

Especialmente útil en libros con alta demanda o primeros capítulos muy visitados

#### 3. Escalado horizontal

Si la aplicación crece y el servidor EC2 no es suficiente, se podría escalar horizontalmente:

- Añadir un Load Balancer (ELB) para distribuir peticiones entre instancias.
- Levantar múltiples instancias EC2 corriendo los contenedores vía Docker Compose.
- Usar un orquestador de contenedores (como ECS o Kubernetes) para gestión automática y escalado.
- Migrar la base de datos a un servicio gestionado como RDS o Aurora para mejorar escalabilidad y disponibilidad.

Esto permitiría que la aplicación escale según demanda sin perder rendimiento ni afectar la experiencia de los lectores.

---

### Experiencia previa con procesamiento de datos a gran escala

Aunque no he trabajado directamente con sistemas que manejen millones de usuarios simultáneos, sí he participado en aplicaciones que procesan grandes volúmenes de datos de lectura en entornos productivos.

#### Contexto en Cepsa

Durante mi experiencia en **Cepsa**, formé parte de proyectos orientados al procesamiento de datos históricos y en tiempo real, relacionados con consumo energético, operaciones y sensores distribuidos.

Trabajé con arquitecturas basadas en **microservicios**, donde distintos servicios intercambiaban información a través de **Apache Kafka**. El sistema requería procesar y transformar continuamente flujos de datos usando **Python (Pandas / PySpark)** y almacenarlos en bases de datos **SQL**. Se priorizaba el rendimiento y la integridad, especialmente en pipelines de lectura que alimentaban dashboards analíticos y reportes de negocio.

#### Tecnologías utilizadas

- **Apache Kafka** como bus de eventos para coordinar microservicios.
- **PostgreSQL y SQL Server** para almacenamiento estructurado.
- **Python** para procesos ETL, transformación y validación de datos.
- **Docker y CI/CD** para orquestación, despliegue y mantenimiento de los servicios.

#### Conclusión

Esta experiencia me preparó para diseñar soluciones escalables y desacopladas, comprender el impacto del volumen de datos en el rendimiento, y trabajar en entornos donde la estabilidad, trazabilidad y precisión son fundamentales.





