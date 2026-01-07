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

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(roles_router, prefix=f"{settings.API_V1_STR}/roles", tags=["rbac"])

@app.get("/")
def root():
    return {"message": "Welcome to College ERP API", "docs": "/docs"}
