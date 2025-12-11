from sqlmodel import create_engine, Session, SQLModel
from app.config.settings import settings

# Import all models to ensure they're registered
# This must be at module level, not inside a function
from app.models import *  # noqa

# Create database engine
engine = create_engine(
    str(settings.DATABASE_URL),
    echo=False,
    pool_pre_ping=True,  # Verify connections before using
)

def init_db():
    """Initialize database tables"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency for getting DB session"""
    with Session(engine) as session:
        yield session
