# Architecture & Design

## Design Goals
- **Low Maintenance**: Small, well-defined modules with clear interfaces.
- **Strong Typing**: Pydantic and SQLModel for runtime and compile-time validation.
- **Separation of Concerns**: Distinct layers for API, domain logic, workers, and infrastructure.
- **Evolvability**: Safe DB migrations (Alembic), versioned API, and feature toggles.
- **Testability**: Designed for unit, integration, and E2E testing.
- **Observability**: Built-in logging, metrics, and health checks.
- **Deployment**: Docker-ready for easy VPS or Kubernetes deployment.

## Tech Stack

### Backend
- **Framework**: FastAPI
- **ORM**: SQLModel (SQLAlchemy) + Alembic
- **Auth**: PyJWT (OAuth2PasswordBearer)
- **Workers**: Celery + Redis
- **Server**: Uvicorn

### Infrastructure
- **Database**: MySQL 8
- **Cache**: Redis
- **Storage**: S3 (or MinIO)
- **Containerization**: Docker

## Directory Structure
```
/college-erp
├── apps
│   └── api                      # FastAPI app
│       ├── app
│       │   ├── config           # Settings & Logging
│       │   ├── core             # Security, Permissions, Events
│       │   ├── db               # Database Session & Base
│       │   ├── models           # SQLModel Models
│       │   ├── schemas          # Pydantic Schemas
│       │   ├── repositories     # Database Access Layer
│       │   ├── services         # Business Logic
│       │   ├── api              # API Routes & Dependencies
│       │   ├── workers          # Celery Tasks
│       │   └── utils            # Helpers (S3, PDF, etc.)
│       ├── scripts              # Operational Scripts
│       └── docker               # Docker Configs
├── infra                        # Infrastructure (Nginx, Terraform)
├── docs                         # Documentation
└── tools                        # Utility Scripts
```

## Best Practices
- **Models vs Schemas**: Separate persistence models (SQLModel) from API contracts (Pydantic).
- **Repositories**: Encapsulate DB queries to keep services clean.
- **Services**: Contain all business logic.
- **Workers**: Offload long-running tasks (OCR, PDF generation) to Celery.
- **Versioning**: Use `api/v1` to prevent breaking changes.
