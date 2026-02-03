import os
from celery import Celery
from app.config.settings import settings

# Set default Django settings module for the 'celery' program.
# Not using Django, but standard pattern to set env vars if needed.

celery_app = Celery(
    "college_erp",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.domains.academic.tasks", # Planned
        # Add other domain tasks here
    ]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_routes={
        "app.domains.communication.tasks.*": {"queue": "high_priority"},
        "*": {"queue": "default"},
    },
    task_create_missing_queues=True,
    task_default_queue="default",
)

if __name__ == "__main__":
    celery_app.start()
