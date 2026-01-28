# VRM Core Backend - Complete Setup Guide for GitHub

This guide provides step-by-step instructions for setting up and running the VRM Core Backend project.

## 📋 What's Included

This is a **production-ready Django REST API** with:

- ✅ 11 database models for VRM/TPRM system
- ✅ Multi-tenancy support (Org-based isolation)
- ✅ Role-Based Access Control (RBAC)
- ✅ Celery background tasks with scheduling
- ✅ MinIO S3-compatible file storage
- ✅ Audit logging system
- ✅ Docker Compose orchestration (7 services)
- ✅ Complete API ready for REST endpoint development

## 🚀 Quick Setup (5 Minutes)

### Step 1: Prerequisites

```
✓ Docker Desktop installed
✓ Git installed
✓ Internet connection
```

### Step 2: Clone & Start

```powershell
# Clone repository
git clone <repo-url>
cd vrm-core-backend

# Copy environment file
copy .env.example .env

# Build and start services
docker-compose build --no-cache
docker-compose up -d

# Wait 15-20 seconds for services to start
```

### Step 3: Initialize Database

```powershell
# Run migrations
docker-compose run web python manage.py migrate

# Seed demo data (creates test users & data)
docker-compose run web python manage.py seed_demo_data

# Verify all services are running
docker-compose ps
```

### Step 4: Access

- **Django Admin**: http://localhost:8000/admin
  - Login: `admin@demo.com` / `admin123`
- **MinIO Console**: http://localhost:9001
  - Login: `minioadmin` / `minioadmin`

## 🔐 Test Credentials

All automatically created via `seed_demo_data.py`:

| User Type | Email                | Password     |
| --------- | -------------------- | ------------ |
| Admin     | admin@demo.com       | admin123     |
| Reviewer  | reviewer@demo.com    | reviewer123  |
| Requester | requester@demo.com   | requester123 |
| Vendor    | contact@techcorp.com | vendor123    |

## 📊 Services Running

All 7 services are containerized:

| Service       | Port      | Purpose               |
| ------------- | --------- | --------------------- |
| Django Web    | 8000      | REST API              |
| PostgreSQL    | 5432      | Database              |
| Redis         | 6379      | Cache/Message Broker  |
| MinIO         | 9000-9001 | File Storage          |
| Celery Worker | -         | Background Tasks      |
| Celery Beat   | -         | Task Scheduler        |
| Network       | -         | Service Communication |

## 🗂️ Key Files

| File                                                      | Purpose                               |
| --------------------------------------------------------- | ------------------------------------- |
| `backend/apps/core/models.py`                             | 11 database models (600+ lines)       |
| `backend/apps/core/tasks.py`                              | 4 Celery scheduled tasks (350+ lines) |
| `backend/apps/core/management/commands/seed_demo_data.py` | Demo data seeding (303 lines)         |
| `docker-compose.yml`                                      | 7-service orchestration               |
| `.env.example`                                            | Environment configuration template    |
| `requirements.txt`                                        | Python dependencies                   |

## 📝 Database Models

1. **Org** - Organization/Tenant
2. **User** - User with RBAC role
3. **Vendor** - Third-party vendor
4. **Template** - Assessment template (versioned)
5. **Assessment** - Assessment instance
6. **Evidence** - File metadata with expiry
7. **Review** - Assessment review
8. **Finding** - Issues found
9. **Remediation** - Remediation tracking
10. **Renewal** - Renewal cycles
11. **AuditLog** - Complete audit trail

## 🔄 Background Tasks

Celery Beat scheduler runs these tasks:

| Task                     | Schedule    | Purpose                       |
| ------------------------ | ----------- | ----------------------------- |
| mark-expired-evidence    | Daily 00:00 | Mark expired evidence         |
| evidence-expiry-reminder | Daily 08:00 | Send reminders (30/15/7 days) |
| renewal-due-reminder     | Daily 09:00 | Send renewal notifications    |
| assessment-due-reminder  | Mon 10:00   | Send assessment reminders     |

All tasks create audit log entries and send email notifications.

## 📁 Demo Data Created

When you run `seed_demo_data.py`:

- 1 Organization
- 5 Users (3 internal + 2 vendors)
- 2 Vendors
- 1 Assessment Template (v1)
- 4 Assessments (various statuses)
- 2 Evidence Files (with expiry dates)
- 1 Finding (High severity)
- 1 Remediation
- 1 Renewal cycle
- Multiple Audit Logs

All isolated to "Demo Organization" for safe testing.

## 🛠️ Common Commands

### Manage Services

```powershell
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f web

# Reset (delete all data)
docker-compose down -v
```

### Django Management

```powershell
# Run migrations
docker-compose run web python manage.py migrate

# Create superuser
docker-compose run web python manage.py createsuperuser

# Seed data
docker-compose run web python manage.py seed_demo_data

# Django shell
docker-compose exec web python manage.py shell
```

### Check Status

```powershell
# All containers running?
docker-compose ps

# Database tables created?
docker-compose exec db psql -U vrm_user -d vrm_db -c "\dt"

# Redis connection?
docker-compose exec redis redis-cli PING
```

## 📚 Next Steps for Team

### Renuka - Build REST APIs

- Create ViewSets for each model
- Add serializers and filters
- Implement authentication endpoints

### Pranjali - Workflow Validation

- Assessment status transitions
- Business rule enforcement
- Validation logic

### Tanishka - Scoring Service

- Risk calculation algorithms
- Evidence analysis
- Scoring API

### Anuja - API Documentation

- Swagger/OpenAPI specs
- Endpoint documentation
- Example requests

### Shiwani - React Frontend

- Authentication UI
- Dashboard
- Assessment forms
- Evidence upload

## ⚠️ Troubleshooting

### Services Not Starting

```powershell
# Rebuild everything
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Database Connection Error

```powershell
# Check PostgreSQL logs
docker-compose logs db

# Restart database
docker-compose restart db
docker-compose run web python manage.py migrate
```

### Port Already in Use

```powershell
# Kill process using port 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or change port in docker-compose.yml
```

### Admin Login Not Working

```powershell
# Verify user exists
docker-compose exec web python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.filter(username='admin@demo.com').exists()

# If False, reseed
>>> exit()
$ docker-compose run web python manage.py seed_demo_data
```

## 📞 Support

- **Project Status**: ✅ MVP Infrastructure Complete
- **API Development**: In Progress (Renuka)
- **Documentation**: In Progress (Anuja)

For issues, check:

1. Docker logs: `docker-compose logs`
2. Django shell for data verification
3. Database connection: `docker-compose exec db psql -U vrm_user -d vrm_db`

## 📄 Important Files to Review

1. **README.md** - Full project documentation
2. **docker-compose.yml** - Service configuration
3. **backend/apps/core/models.py** - Data models
4. **backend/apps/core/tasks.py** - Background tasks
5. **backend/apps/core/management/commands/seed_demo_data.py** - Data seeding

## ✨ Features Implemented

✅ Multi-tenant Django application  
✅ RBAC (4 roles: Admin, Reviewer, Requester, Vendor)  
✅ Assessment workflow with status tracking  
✅ Evidence management with expiry  
✅ Celery background jobs with scheduling  
✅ Email notifications  
✅ Audit logging (11 action types)  
✅ Template versioning  
✅ Remediation tracking  
✅ Renewal cycle management  
✅ MinIO S3 file storage  
✅ PostgreSQL database  
✅ Redis caching  
✅ Docker Compose orchestration  
✅ Complete demo data

## 🎯 What's Ready

- ✅ Database schema and models
- ✅ Authentication system (JWT ready)
- ✅ Background job infrastructure
- ✅ File storage system
- ✅ Audit logging system
- ✅ Demo data and test credentials
- ✅ Docker containerization
- ⏳ REST API endpoints (in development)
- ⏳ Frontend (planned)

## 📅 Timeline

- **Phase 1 (Complete)**: Infrastructure & Models ✅
- **Phase 2 (In Progress)**: REST API Endpoints
- **Phase 3 (Pending)**: Frontend Development
- **Phase 4 (Pending)**: Deployment

---

**Project Ready for Team Development!** 🚀

For detailed documentation, see README.md
