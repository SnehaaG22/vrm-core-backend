# VRM Core Backend - Complete Third-Party Risk Management System

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.15-blue.svg)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com/)

**Vulnerability & Third-Party Risk Management System (MVP)**

**Production-ready Django REST backend for VRM / TPRM with:**

Multi-tenant architecture (org isolation)

JWT Authentication + RBAC

PostgreSQL

Celery + Redis (background jobs)

MinIO (S3 compatible evidence storage)

Audit logs

Dockerized infrastructure

# Tech Stack

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

3. Build Docker Images (First Time Only)

docker-compose build --no-cache

4. Start All Services
   
docker-compose up -d

5.then check service

docker-compose ps

6. Run Database Migrations
   
docker-compose run web python manage.py migrate

7. Seed demo data

docker-compose run web python manage.py seed_demo_data
   
**Backend ready.**

# Service URLs

Django Admin: 	http://localhost:8000/admin

Login: admin@demo.com / admin123

MinIO File Storage:  http://localhost:9001 

Login: minioadmin / minioadmin 

# Services in Docker Compose

web → Django 

db → PostgreSQL

redis → Redis broker

celery-worker → Background tasks

celery-beat → Scheduled jobs

minio → Evidence file storage

# Common Docker Commands

Check Status

docker-compose ps

View Logs

docker-compose logs -f web

Start

docker-compose up -d

Stop

docker-compose down

Reset DB

docker-compose down -v

Restart Services

docker-compose restart

Access Django Shell

docker-compose exec web python manage.py shell

Run Custom Commands

docker-compose exec web python manage.py <command>

View Database Logs

docker-compose logs db

View Celery Task Logs

docker-compose logs celery-worker

# Django Commands

docker-compose run web python manage.py migrate

docker-compose run web python manage.py makemigrations

docker-compose run web python manage.py createsuperuser

docker-compose run web python manage.py seed_demo_data

docker-compose exec web python manage.py shell

docker-compose run web pytest

# Test API Endpoints

Get JWT Token (All Users)

# Admin
curl.exe -X POST http://localhost:8000/api/token/ -H "Content-Type: application/json" -d '{"username":"admin@demo.com","password":"admin123"}'

# Reviewer
curl.exe -X POST http://localhost:8000/api/token/ -H "Content-Type: application/json" -d '{"username":"reviewer@demo.com","password":"reviewer123"}'

# Requester
curl.exe -X POST http://localhost:8000/api/token/ -H "Content-Type: application/json" -d '{"username":"requester@demo.com","password":"requester123"}'

# Vendor
curl.exe -X POST http://localhost:8000/api/token/ -H "Content-Type: application/json" -d '{"username":"vendor_1@techcorpsolutions","password":"vendor123"}'


# All Test User Credentials:

Role-> Admin 	  Username->admin@demo.com 	Email->admin@demo.com	Password->admin123

Role-> Reviewer	  Username->reviewer@demo.com  Email->reviewer@demo.com	 Password->reviewer123

Role-> Requester	  Username->requester@demo.com	 Email->requester@demo.com	 Password->requester123

Role-> Vendor 1  Username->vendor_1@techcorpsolutions	 Email->contact@techcorp.com	 Password->vendor123

Role-> Vendor 2  Username->vendor_2@cloudservicesinc	 Email->contact@cloudservices.com	 Password->vendor123


# Environment Variables (.env.example)

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

# MVP Status

Docker infra ready

Celery operational

MinIO configured

Seed data available

Swagger enabled

JWT auth active

ALLOWED_HOSTS=*
CORS_ALLOW_ALL=True
