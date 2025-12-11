# Onboarding Guide

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose

### Common Commands

#### Backend (`apps/api`)

**Run Development Server:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Run Tests:**
```bash
pytest -q
```

**Database Migrations:**
```bash
# Create migration
alembic revision --autogenerate -m "add X"

# Apply migrations
alembic upgrade head
```

**Celery Workers:**
```bash
# Start worker
celery -A app.workers.celery_app worker -l info

# Start scheduler (beat)
celery -A app.workers.celery_app beat -l info
```

#### Docker (Dev)
```bash
docker-compose -f docker/docker-compose.yml up --build
```
