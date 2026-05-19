import asyncio

from app.core.logger import logger
from app.services.celery_app import celery_app
from app.services.document_service import process_document


@celery_app.task(name="document.process")
def process_document_task(filepath: str):
    logger.info("[Celery] Processando documento em worker: %s", filepath)
    asyncio.run(process_document(filepath))
    return {"status": "processed", "filepath": filepath}
