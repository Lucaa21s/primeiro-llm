from pypdf import PdfReader

from app.core.logger import logger
from app.rag.rag_system import add_document


async def process_document(filepath: str):
    logger.info("Extraindo texto e gerando vetores: %s", filepath)
    try:
        reader = PdfReader(filepath)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\\n"

        await add_document(text, filepath)
        logger.info("PDF processado e injetado no pgvector: %s", filepath)
    except Exception as error:
        logger.error("Erro ao processar PDF %s: %s", filepath, error)
