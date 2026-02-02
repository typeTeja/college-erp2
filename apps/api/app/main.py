from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.api.v1.router import api_router
from app.api.v1.roles import router as roles_router
from app.core.rbac import seed_permissions
from app.db.session import engine, init_db
from sqlmodel import Session

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

@app.on_event("startup")
def on_startup():
    # Initialize database tables first
    init_db()
    with Session(engine) as session:
        seed_permissions(session)

# CRITICAL: Add ProxyHeadersMiddleware FIRST (before CORS)
# This ensures FastAPI correctly detects HTTPS behind reverse proxy (Nginx)
if settings.ENVIRONMENT == "production":
    from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
    app.add_middleware(
        ProxyHeadersMiddleware,
        trusted_hosts=["*"]  # Or specify your load balancer IPs
    )

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include domain routers
app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(system_router, prefix=f"{settings.API_V1_STR}/system", tags=["system"])
app.include_router(hr_router, prefix=f"{settings.API_V1_STR}/hr", tags=["hr"])
app.include_router(academic_router, prefix=f"{settings.API_V1_STR}/academic", tags=["academic"])
app.include_router(student_router, prefix=f"{settings.API_V1_STR}/students", tags=["students"])
app.include_router(admission_router, prefix=f"{settings.API_V1_STR}/admissions", tags=["admissions"])
app.include_router(finance_router, prefix=f"{settings.API_V1_STR}/finance", tags=["finance"])
app.include_router(communication_router, prefix=f"{settings.API_V1_STR}/communication", tags=["communication"])
app.include_router(campus_router, prefix=f"{settings.API_V1_STR}/campus", tags=["campus"])

@app.get("/")
async def root():
    return {
        "message": "College ERP API",
        "version": "2.0",
        "docs": "/docs",
        "domains": [
            "auth", "system", "hr", "academic",
            "students", "admissions", "finance",
            "communication", "campus"
        ]
    }

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT
    }
