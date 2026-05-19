import os

from fastapi import HTTPException
from ollama import AsyncClient

from app.core.logger import logger
from app.memory.memory_system import save_memory, search_memory
from app.rag.rag_system import search_documents


async def build_chat_prompt(user_message: str) -> str:
    try:
        memory_context = await search_memory(user_message)
        rag_context = await search_documents(user_message)
    except Exception as error:
        logger.exception("Falha ao consultar memória/RAG: %s", error)
        raise HTTPException(status_code=503, detail="Serviços de contexto indisponíveis")

    try:
        await save_memory(user_message)
    except Exception as error:
        logger.exception("Falha ao salvar memória: %s", error)

    return f"""
Você é uma IA moderna.

Memórias relevantes:
{memory_context}

Contexto encontrado:
{rag_context}

Pergunta:
{user_message}
"""


async def stream_chat_response(prompt: str):
    client = AsyncClient(host=os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434"))
    stream_response = await client.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )

    async for chunk in stream_response:
        yield chunk["message"]["content"]
