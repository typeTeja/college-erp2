# Server wrapper that imports from the actual API location
import sys
import os

# Add the apps/api directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'apps', 'api'))

# Copy environment variables from backend .env to be accessible
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Import the FastAPI app from the actual location
from app.main import app

# Re-export for uvicorn
__all__ = ['app']
