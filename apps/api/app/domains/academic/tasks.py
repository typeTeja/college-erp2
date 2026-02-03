from app.core.celery_app import celery_app
import logging

logger = logging.getLogger(__name__)

@celery_app.task
def test_academic_task(word: str):
    logger.info(f"Test task received: {word}")
    return f"Processed {word}"
