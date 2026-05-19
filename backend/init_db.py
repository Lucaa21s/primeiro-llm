import sys
import os
# Garante que imports base funcionem
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.database import sync_engine
from models import Base
from sqlalchemy import text

def init_database():
    with sync_engine.begin() as conn:
        print("Habilitando extensão pgvector...")
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        
        print("Criando tabelas relacionais...")
        Base.metadata.create_all(bind=conn)

        print("Criando tabela vetorial de Memórias...")
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS memories (
            id SERIAL PRIMARY KEY,
            content TEXT,
            embedding vector(384)
        );
        """))

        print("Criando tabela vetorial de Documentos (RAG)...")
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS documents (
            id SERIAL PRIMARY KEY,
            content TEXT,
            document_id VARCHAR,
            embedding vector(384)
        );
        """))

        print("Criando índices vetoriais (IVFFLAT)...")
        conn.execute(text("""
        CREATE INDEX IF NOT EXISTS memories_embedding_ivfflat_idx
        ON memories USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 100);
        """))
        conn.execute(text("""
        CREATE INDEX IF NOT EXISTS documents_embedding_ivfflat_idx
        ON documents USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 100);
        """))
    print("Banco de dados criado e atualizado com sucesso!")

if __name__ == "__main__":
    init_database()
