CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS memories (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(384)
);

CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    document_id VARCHAR,
    embedding vector(384)
);

-- Indexes for ANN search (effective with larger datasets)
CREATE INDEX IF NOT EXISTS memories_embedding_ivfflat_idx
    ON memories USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

CREATE INDEX IF NOT EXISTS documents_embedding_ivfflat_idx
    ON documents USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);
