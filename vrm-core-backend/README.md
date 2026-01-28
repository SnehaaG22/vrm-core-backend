# VRM Core Backend - Complete Third-Party Risk Management System

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.15-blue.svg)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com/)

# Vulnerability & Third-Party Risk Management System (MVP)

# Production-ready Django REST backend for VRM / TPRM with:

Multi-tenant architecture (org isolation)

JWT Authentication + RBAC

PostgreSQL

Celery + Redis (background jobs)

MinIO (S3 compatible evidence storage)

Audit logs

Dockerized infrastructure

#Tech Stack

Python 3.11

Django 4.2 + DRF

PostgreSQL 15

Redis

Celery + Celery Beat

MinIO

Docker Compose

# One-Command Local Setup

1. Clone repo
   
git clone <repo_url>

cd vrm-core-backend

2. Environment setup

Create env file:

cp .env.example .env

3. Start everything
   
docker-compose up -d

4. Run migrations
   
docker-compose run web python manage.py migrate

5. Seed demo data
   
docker-compose run web python manage.py seed_demo_data

**Backend ready.**

# Service URLs

Django API-	http://localhost:8000

Swagger-	http://localhost:8000/api/schema/swagger-ui/

MinIO Console-	http://localhost:9001

PostgreSQL-	localhost:5432

Redis-	localhost:6379

# Services in Docker Compose

web → Django API

db → PostgreSQL

redis → Redis broker

celery-worker → Background tasks

celery-beat → Scheduled jobs

minio → Evidence file storage

#Test Credentials (Seeded)

**Admin**

email: admin@demo.com

password: admin123

**Reviewer**

email: reviewer@demo.com

password: reviewer123

**Requester**

email: requester@demo.com

password: requester123

**Vendor User**

email: vendor@demo.com

password: vendor123

# Common Docker Commands

Start

docker-compose up -d

Stop

docker-compose down

Reset DB

docker-compose down -v

Rebuild

docker-compose build --no-cache

Logs

docker-compose logs -f

docker-compose logs -f web

docker-compose logs -f celery-worker

# Django Commands

docker-compose run web python manage.py migrate

docker-compose run web python manage.py makemigrations

docker-compose run web python manage.py createsuperuser

docker-compose run web python manage.py seed_demo_data

docker-compose exec web python manage.py shell

docker-compose run web pytest

# Database

Access psql

docker-compose exec db psql -U vrm_user -d vrm_db

Backup

docker-compose exec db pg_dump -U vrm_user vrm_db > backup.sql

Restore

cat backup.sql | docker-compose exec -T db psql -U vrm_user -d vrm_db

# Celery & Background Jobs

Workers

docker-compose logs -f celery-worker

Beat Scheduler

docker-compose logs -f celery-beat

Redis CLI

docker-compose exec redis redis-cli

**Implemented Jobs**

Evidence expiry reminders (30 / 15 / 7 days)

Vendor renewal reminders

Optional assessment due reminders

# MinIO (Evidence Storage)

Console:

http://localhost:9001

Credentials (from .env):

MINIO_ROOT_USER

MINIO_ROOT_PASSWORD

Default bucket:

evidence

Environment Variables (.env.example)

DJANGO_SECRET_KEY=changeme 

DJANGO_DEBUG=True

DJANGO_SETTINGS_MODULE=backend.settings.dev

POSTGRES_DB=vrm_db

POSTGRES_USER=vrm_user

POSTGRES_PASSWORD=vrm_pass

POSTGRES_HOST=db

POSTGRES_PORT=5432

REDIS_URL=redis://redis:6379/0

CELERY_BROKER_URL=redis://redis:6379/0

MINIO_ENDPOINT=minio:9000

MINIO_ACCESS_KEY=minioadmin

MINIO_SECRET_KEY=minioadmin

MINIO_BUCKET=evidence

# Seeded Demo Data

Includes:

1 Org

Admin / Reviewer / Requester users

2 Vendors + vendor users

1 Template with sections/questions

Assessments in multiple states

Evidence entries with expiry

1 remediation scenario

**MVP Status**

Docker infra ready

Celery operational

MinIO configured

Seed data available

Swagger enabled

JWT auth active

ALLOWED_HOSTS=*
CORS_ALLOW_ALL=True
