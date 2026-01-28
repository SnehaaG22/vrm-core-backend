# VRM Core Backend - Complete Third-Party Risk Management System

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.15-blue.svg)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com/)

Complete **Vulnerability & Risk Management (VRM)** / **Third-Party Risk Management (TPRM)** backend system. Production-ready Django REST API with multi-tenancy, RBAC, Celery background jobs, file storage, audit logging, and comprehensive data models.

 🔧 Common Commands

### Docker Management

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Stop & remove volumes (reset DB)
docker-compose down -v

# Rebuild images
docker-compose build --no-cache

# View real-time logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f web
docker-compose logs -f celery-worker
```

### Django Commands

```bash
# Run migrations
docker-compose run web python manage.py migrate

# Make migrations
docker-compose run web python manage.py makemigrations

# Create superuser
docker-compose run web python manage.py createsuperuser

# Seed demo data
docker-compose run web python manage.py seed_demo_data

# Django shell
docker-compose exec web python manage.py shell

# Run tests
docker-compose run web pytest

# Execute arbitrary command
docker-compose exec web python manage.py <command>
```

### Database

```bash
# Access PostgreSQL CLI
docker-compose exec db psql -U vrm_user -d vrm_db

# Backup database
docker-compose exec db pg_dump -U vrm_user vrm_db > backup.sql

# Restore from backup
cat backup.sql | docker-compose exec -T db psql -U vrm_user -d vrm_db
```

### Celery & Redis

```bash
# View Celery worker logs
docker-compose logs -f celery-worker

# View Celery Beat scheduler logs
docker-compose logs -f celery-beat

# Access Redis CLI
docker-compose exec redis redis-cli

# View Redis keys
docker-compose exec redis redis-cli KEYS '*'
```


```
