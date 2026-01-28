# VRM Core Backend - Complete Third-Party Risk Management System

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.15-blue.svg)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com/)

Complete **Vulnerability & Risk Management (VRM)** / **Third-Party Risk Management (TPRM)** backend system. Production-ready Django REST API with multi-tenancy, RBAC, Celery background jobs, file storage, audit logging, and comprehensive data models.

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Running the Project](#-running-the-project)
- [API Documentation](#-api-documentation)
- [Database Models](#-database-models)
- [Test Credentials](#-test-credentials)
- [Celery Tasks](#-celery-tasks)
- [File Storage (MinIO)](#-file-storage-minio)
- [Troubleshooting](#-troubleshooting)
- [Team Members & Responsibilities](#-team-members--responsibilities)
- [Project Structure](#-project-structure)

## ✨ Features

- ✅ **Multi-Tenant Architecture** - Org-based isolation with complete data segregation
- ✅ **Role-Based Access Control (RBAC)** - 4 roles: Admin, Reviewer, Requester, Vendor
- ✅ **Assessment Workflow** - Multi-status workflow (assigned → in_progress → submitted → under_review → approved/rejected → remediation)
- ✅ **Template Versioning** - Assessment templates with version locking at assignment
- ✅ **Evidence Management** - File upload/storage with expiry tracking and MinIO S3-compatible storage
- ✅ **Audit Logging** - Complete audit trail of all operations with JSON change tracking
- ✅ **Celery Background Jobs** - 4 scheduled tasks (evidence expiry reminders, renewal reminders, assessment reminders, expiry marking)
- ✅ **Vendor Management** - Third-party vendor tracking and responses
- ✅ **Remediation Tracking** - Complete remediation workflow with findings and status tracking
- ✅ **Renewal Cycles** - Annual renewal management with due date tracking
- ✅ **Email Notifications** - Automated email alerts for key events
- ✅ **JWT Authentication** - Secure token-based API authentication
- ✅ **PostgreSQL Backend** - Production-grade database with full-text search support
- ✅ **Redis Caching** - Fast caching and Celery message broker
- ✅ **Docker Compose** - Complete containerized stack (7 services)

## 🏗️ Architecture

````
vrm-core-backend/
├── docker-compose.yml          # 7-service stack: Django, PostgreSQL, Redis, MinIO, Celery
├── manage.py                    # Django management
## 📦 Installation & Setup

### 1. Prerequisites

- Docker & Docker Compose ([Download](https://www.docker.com/products/docker-desktop))
- Git
- Windows/Mac/Linux

### 2. Clone & Setup

```bash
# Clone repository
git clone <repo-url>
cd vrm-core-backend

# Copy environment template
cp .env.example .env

# Edit .env with your settings (optional for development)
# Default values work for local development
````

### 3. Build & Start

```bash
# Build Docker images
docker-compose build --no-cache

# Start all services (7 containers)
docker-compose up -d

# Wait for services to start
# Check status with:
docker-compose ps
```

### 4. Initialize Database

```bash
# Run migrations
docker-compose run web python manage.py migrate

# Seed demo data (optional but recommended)
docker-compose run web python manage.py seed_demo_data
```

### 5. Verify Setup

```bash
# Check all containers are running
docker-compose ps

# View logs
docker-compose logs web
```

✅ **Setup Complete!** Proceed to [Access Services](#access-services)

## 🌐 Access Services

| Service       | URL                         | Username       | Password     |
| ------------- | --------------------------- | -------------- | ------------ |
| Django Admin  | http://localhost:8000/admin | admin@demo.com | admin123     |
| Django API    | http://localhost:8000/api/  | (JWT required) | -            |
| MinIO Console | http://localhost:9001       | minioadmin     | minioadmin   |
| PostgreSQL    | localhost:5432              | vrm_user       | vrm_password |
| Redis         | localhost:6379              | (no auth)      | -            |

## 🔐 Test User Accounts

All credentials are created automatically when you run:

```bash
docker-compose run web python manage.py seed_demo_data
```

### Account Details

| Role      | Email                     | Password     | Use Case                         |
| --------- | ------------------------- | ------------ | -------------------------------- |
| **Admin** | admin@demo.com            | admin123     | Full system access, Django admin |
| Reviewer  | reviewer@demo.com         | reviewer123  | Review & approve assessments     |
| Requester | requester@demo.com        | requester123 | Create & submit assessments      |
| Vendor 1  | contact@techcorp.com      | vendor123    | Respond to vendor assessments    |
| Vendor 2  | contact@cloudservices.com | vendor123    | Respond to vendor assessments    |

## 🗄️ Database Models

### 11 Core Models Implemented

| Model           | Purpose              | Fields                                                                       |
| --------------- | -------------------- | ---------------------------------------------------------------------------- |
| **Org**         | Organization/Tenant  | name, created_at, updated_at                                                 |
| **User**        | User with RBAC role  | django_user, org, role, created_at, updated_at                               |
| **Vendor**      | Third-party vendor   | name, org, status, contact_email, created_at, updated_at                     |
| **Template**    | Assessment template  | name, org, version, description, created_at, updated_at                      |
| **Assessment**  | Assessment instance  | template, org, vendor, status, due_date, assigned_to, created_at, updated_at |
| **Evidence**    | File metadata        | assessment, file_path, file_name, file_size, expiry_date, created_at         |
| **Review**      | Assessment review    | assessment, reviewer, status, comments, created_at, updated_at               |
| **Finding**     | Issue/finding        | assessment, severity, description, created_at                                |
| **Remediation** | Remediation tracking | finding, status, due_date, created_at, updated_at                            |
| **Renewal**     | Renewal cycle        | vendor, org, due_date, status, created_at, updated_at                        |
| **AuditLog**    | Audit trail          | actor, org, action, entity, ip_address, user_agent, changes, created_at      |

## 🔄 Celery Background Tasks

### Scheduled Tasks (via Celery Beat)

| Task                       | Schedule    | Action                                            |
| -------------------------- | ----------- | ------------------------------------------------- |
| `mark-expired-evidence`    | Daily 00:00 | Mark evidence as expired in database              |
| `evidence-expiry-reminder` | Daily 08:00 | Send email reminders (30/15/7 days before expiry) |
| `renewal-due-reminder`     | Daily 09:00 | Send renewal due/overdue notifications            |
| `assessment-due-reminder`  | Mon 10:00   | Send 7-day lookahead assessment reminders         |

### Running Tasks Manually

```bash
# Test task directly
docker-compose exec web python manage.py shell

# Inside shell:
from backend.apps.core.tasks import evidence_expiry_reminder
result = evidence_expiry_reminder()
print(result)
```

## 📁 File Storage (MinIO)

MinIO provides S3-compatible object storage for evidence files.

### Access MinIO Dashboard

```
URL: http://localhost:9001
Username: minioadmin
Password: minioadmin
```

### File Structure

```
evidence-uploads/
  └── evidence/
      └── reports/
          └── {assessment_id}/
              └── {file_name}.pdf
```

## 📊 Demo Data

The `seed_demo_data.py` command creates:

- ✅ 1 Organization (Demo Organization)
- ✅ 5 Users (3 internal + 2 vendors)
- ✅ 2 Vendors
- ✅ 1 Assessment Template (v1)
- ✅ 4 Assessments in various statuses
- ✅ 2 Evidence Files with expiry tracking
- ✅ 1 Finding (High severity)
- ✅ 1 Remediation workflow
- ✅ 1 Renewal cycle
- ✅ Multiple Audit Log entries

All demo data is isolated to "Demo Organization" for testing.

## 🔧 Common Commands

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

## ⚙️ Environment Variables

All environment variables are in `.env.example`. Key settings:

```bash
# Django
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
POSTGRES_HOST=db
POSTGRES_DB=vrm_db
POSTGRES_USER=vrm_user
POSTGRES_PASSWORD=secure_password

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# MinIO
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
MINIO_ENDPOINT=minio:9000

# Email (configure for production)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 🐛 Troubleshooting

### Services Not Starting

```bash
# Check logs
docker-compose logs

# Rebuild everything
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Database Connection Error

```bash
# Ensure PostgreSQL is running
docker-compose logs db

# Check database credentials in .env
# Restart database
docker-compose restart db
docker-compose run web python manage.py migrate
```

### Celery Tasks Not Running

```bash
# Check Celery Beat scheduler
docker-compose logs celery-beat

# Restart Celery services
docker-compose restart celery-worker celery-beat
```

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process or change port in docker-compose.yml
```

### Django Admin Login Not Working

```bash
# Verify users exist in database
docker-compose exec web python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.all().values('username', 'email', 'is_staff')

# If admin not marked as staff, fix it:
>>> user = User.objects.get(username='admin@demo.com')
>>> user.is_staff = True
>>> user.is_superuser = True
>>> user.save()
```

## 📚 Project Structure Explained

```
vrm-core-backend/
├── docker-compose.yml          # 7-service orchestration
├── Dockerfile                  # Python 3.11 + Django image
├── manage.py                   # Django entry point
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
├── README.md                   # This file
├── backend/
│   ├── apps/
│   │   ├── core/              # ⭐ Main models & tasks
│   │   │   ├── models.py       # 11 database models
│   │   │   ├── tasks.py        # 4 Celery tasks + email
│   │   │   ├── celery_schedule.py  # Beat configuration
│   │   │   ├── seed.py         # Simple seed script
│   │   │   ├── management/commands/
│   │   │   │   └── seed_demo_data.py  # Full seed command
│   │   │   └── migrations/     # DB migrations
│   │   ├── accounts/           # 🔐 Auth & JWT (TBD)
│   │   ├── orgs/               # 🏢 Org management (TBD)
│   │   ├── users/              # 👥 User management (TBD)
│   │   ├── vendors/            # 🏪 Vendor module (TBD)
│   │   ├── templates/          # 📋 Templates (TBD)
│   │   ├── assessments/        # ✓ Assessments (TBD)
│   │   ├── responses/          # 💬 Responses (TBD)
│   │   ├── evidence/           # 📁 Evidence storage (TBD)
│   │   ├── reviews/            # ✍️ Reviews (TBD)
│   │   ├── remediations/       # 🔧 Remediation (TBD)
│   │   ├── renewals/           # 🔄 Renewals (TBD)
│   │   ├── dashboard/          # 📊 Analytics (TBD)
│   │   ├── audit/              # 📝 Audit logs (TBD)
│   │   └── roles_permissions/  # 🔑 RBAC (TBD)
│   └── backend/
│       ├── settings/
│       │   ├── base.py         # Base configuration
│       │   ├── dev.py          # Development overrides
│       │   └── prod.py         # Production overrides
│       ├── celery.py           # Celery initialization
│       ├── urls.py             # URL routing
│       ├── wsgi.py             # WSGI server entry
│       └── asgi.py             # ASGI server entry
```

## 👥 Team Members & Responsibilities

| Member            | Role                   | Tasks                                                       | Status         |
| ----------------- | ---------------------- | ----------------------------------------------------------- | -------------- |
| **Sneha Gaikwad** | Backend Infrastructure | Docker Compose ✅, Models ✅, Seed Data ✅, Celery Tasks ✅ | ✅ **DONE**    |
| **Renuka**        | API Development        | REST APIs, Serializers, ViewSets                            | ⏳ In Progress |
| **Pranjali**      | Workflow Validation    | Status transitions, Business logic                          | ⏳ Pending     |
| **Tanishka**      | Scoring Service        | Risk scoring engine                                         | ⏳ Pending     |
| **Anuja**         | API Documentation      | OpenAPI/Swagger specs                                       | ⏳ Pending     |
| **Shiwani**       | React Frontend         | Dashboard, Forms, Notifications                             | ⏳ Pending     |

## 📝 Completed Deliverables

### ✅ Sneha's Tasks (Infrastructure)

- [x] Docker Compose with 7 services (Django, PostgreSQL, Redis, MinIO, Celery x2)
- [x] 11 comprehensive database models with relationships
- [x] 4 Celery scheduled background tasks with email integration
- [x] Demo data seeding (users, vendors, assessments, evidence, etc.)
- [x] Audit logging system with 11 action types
- [x] Complete README documentation
- [x] Environment configuration template (.env.example)
- [x] Health checks for all Docker services

## 🚀 Next Steps for Your Team

1. **Renuka**: Build REST APIs on top of these models
   - Authentication endpoints (/api/auth/)
   - CRUD endpoints for each model
   - Filtering, pagination, serialization
2. **Pranjali**: Implement workflow validations
   - Assessment status transitions
   - Remediation approval flow
   - Renewal cycle rules

3. **Tanishka**: Develop scoring service
   - Risk calculation algorithms
   - Evidence analysis
   - Scoring API endpoints

4. **Anuja**: Document API
   - Swagger/OpenAPI specs
   - Endpoint descriptions
   - Example requests/responses

5. **Shiwani**: Build React frontend
   - Authentication UI
   - Assessment dashboard
   - Evidence upload
   - Remediation tracking

## 📞 Support & Documentation

- **Django**: https://docs.djangoproject.com/
- **DRF**: https://www.django-rest-framework.org/
- **Celery**: https://docs.celeryproject.org/
- **PostgreSQL**: https://www.postgresql.org/docs/
- **Docker**: https://docs.docker.com/

## 📄 License

This project is proprietary. All rights reserved to MIT Aurangabad.

## ✨ Contributors

- Sneha Gaikwad - Backend Infrastructure (MVP)
- Renuka - API Development (In Progress)
- Team - Collaborative VRM System

---

**Last Updated**: January 28, 2026
**Status**: ✅ MVP Infrastructure Complete - Ready for API Development

# Redis & Celery

REDIS_URL=redis://redis:6379/0

# MinIO

MINIO_ENDPOINT=minio:9000
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=strong-password
MINIO_BUCKET_NAME=evidence-uploads

# Email

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# CORS

CORS_ALLOWED_ORIGINS=https://yourdomain.com

# Logging

LOG_LEVEL=INFO

```

## 📋 Workflow States (Enforced)

### Assessment Workflow

```

assigned → in_progress → submitted → under_review → approved/rejected
↓
remediation → approved

```

### Remediation Workflow

```

requested → in_progress → submitted → verified → closed

```

### Renewal Workflow

```

pending → triggered → in_progress → completed

```

## 🚨 Important Notes

1. **Tenant Isolation**: Every query is automatically org-scoped. Super admin can view cross-org only with flag.
2. **Audit Trail**: All critical actions create audit log entries.
3. **Workflow Enforcement**: Invalid state transitions return 409 Conflict.
4. **Email Notifications**: Requires `EMAIL_BACKEND` configuration.
5. **MinIO Setup**: Bucket must be created; script auto-creates on first use.

## 🤝 Development Collaboration

- **Renuka**: API implementation (endpoints, serializers, views)
- **Pranjali**: Workflow validation & QA
- **Anuja**: OpenAPI contract alignment
- **Tanishka**: Scoring engine integration
- **Sneha**: Docker, database, Celery tasks (this README)
- **Shiwani**: React frontend UI

## 📞 Support

For issues or questions:

1. Check the logs: `docker-compose logs -f`
2. Run health checks: `docker-compose ps`
3. Test individual services
4. Consult the team

## 📝 License

Proprietary - VRM MVP Project

---

**Last Updated**: 2026-01-28
**Status**: MVP Phase - Development
**Version**: 1.0.0
raise ImportError(
"Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH?"
) from exc

    execute_from_command_line(sys.argv)

if **name** == "**main**":
main()
```
