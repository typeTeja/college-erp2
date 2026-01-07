"""
Initialize PostgreSQL database with all tables using centralized model registry
"""
import sys
import os

# Add parent directory to path to allow importing app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import central model registry to ensure all tables are registered
# Load environment variables before importing settings
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

import app.models  # noqa: F401

from app.db.session import engine
from sqlmodel import SQLModel

def init_db():
    print("Initializing database...")
    print("Creating tables from centralized registry...")
    SQLModel.metadata.create_all(engine)
    print("✅ Tables created successfully.")

if __name__ == "__main__":
    init_db()
