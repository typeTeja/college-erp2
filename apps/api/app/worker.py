from app.core.celery_app import celery_app

# This file is the entry point for the Celery worker
# Run: celery -A app.worker.celery_app worker --loglevel=info
