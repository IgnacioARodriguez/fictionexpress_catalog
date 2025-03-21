# Fiction Express - Prueba Técnica Backend (Django + DRF)

## Descripción del Proyecto
API RESTful construida con Django Rest Framework para la gestión de un catálogo de libros, con control de acceso basado en roles (RBAC), autenticación JWT, y despliegue automatizado en AWS EC2 usando Docker y GitHub Actions.

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

