from sqlalchemy import create_engine
from sqlalchemy import text

from sentence_transformers import SentenceTransformer

DATABASE_URL = (
    "postgresql://ia_user:1609246@localhost/ia_memory"
)

engine = create_engine(DATABASE_URL)

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def init_db():

    with engine.connect() as conn:

        conn.execute(text("""
        CREATE EXTENSION IF NOT EXISTS vector;
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS memories (
            id SERIAL PRIMARY KEY,
            content TEXT,
            embedding vector(384)
        );
        """))

        conn.commit()



def save_memory(content):

    embedding = embedding_model.encode(content)

    embedding_list = embedding.tolist()

    embedding_string = (
        "[" + ",".join(map(str, embedding_list)) + "]"
    )

    with engine.connect() as conn:

        conn.execute(
            text("""
            INSERT INTO memories
            (content, embedding)
            VALUES
            (:content, :embedding)
            """),
            {
                "content": content,
                "embedding": embedding_string,
            },
        )

        conn.commit()



def search_memory(query, limit=3):

    embedding = embedding_model.encode(query)

    embedding_list = embedding.tolist()

    embedding_string = (
        "[" + ",".join(map(str, embedding_list)) + "]"
    )

    with engine.connect() as conn:

        result = conn.execute(
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


# init_db() será chamado quando necessário
# init_db()