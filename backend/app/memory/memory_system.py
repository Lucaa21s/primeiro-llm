from sqlalchemy import text
from sentence_transformers import SentenceTransformer

from app.db.database import async_engine

_embedding_model = None


def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedding_model

async def save_memory(content: str):
    embedding = get_embedding_model().encode(content)
    embedding_list = embedding.tolist()
    embedding_string = "[" + ",".join(map(str, embedding_list)) + "]"

    async with async_engine.begin() as conn:
        await conn.execute(
            text("""
            INSERT INTO memories (content, embedding)
            VALUES (:content, :embedding)
            """),
            {
                "content": content,
                "embedding": embedding_string,
            },
        )

async def search_memory(query: str, limit: int = 3):
    embedding = get_embedding_model().encode(query)
    embedding_list = embedding.tolist()
    embedding_string = "[" + ",".join(map(str, embedding_list)) + "]"

    async with async_engine.connect() as conn:
        result = await conn.execute(
            text("""
            SELECT content
            FROM memories
            ORDER BY embedding <-> CAST(:embedding AS vector)
            LIMIT :limit
            """),
            {
                "embedding": embedding_string,
                "limit": limit,
            },
        )
        return [row[0] for row in result.fetchall()]
