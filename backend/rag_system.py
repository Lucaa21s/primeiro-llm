from sqlalchemy import text
from sentence_transformers import SentenceTransformer
from app.db.database import async_engine
import uuid

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def split_text(text: str, chunk_size: int = 500):
    chunks = []
    words = text.split()
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

async def add_document(text_content: str, filename: str):
    chunks = split_text(text_content)
    if not chunks:
        return
        
    embeddings = embedding_model.encode(chunks)
    
    async with async_engine.begin() as conn:
        for chunk, emb in zip(chunks, embeddings):
            emb_str = "[" + ",".join(map(str, emb.tolist())) + "]"
            await conn.execute(
                text("""
                INSERT INTO documents (content, document_id, embedding)
                VALUES (:content, :doc_id, :embedding)
                """),
                {
                    "content": chunk,
                    "doc_id": filename,
                    "embedding": emb_str,
                }
            )

async def search_documents(query: str, n_results: int = 4):
    embedding = embedding_model.encode(query)
    emb_str = "[" + ",".join(map(str, embedding.tolist())) + "]"

    async with async_engine.connect() as conn:
        result = await conn.execute(
            text("""
            SELECT content
            FROM documents
            ORDER BY embedding <-> CAST(:embedding AS vector)
            LIMIT :limit
            """),
            {
                "embedding": emb_str,
                "limit": n_results,
            },
        )
        rows = result.fetchall()
        if not rows:
            return ""
        return "\\n".join([row[0] for row in rows])
