from sentence_transformers import SentenceTransformer
import chromadb

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(
    path="rag_db"
)

collection = client.get_or_create_collection(
    name="documents"
)


def split_text(text, chunk_size=500):
    chunks = []

    words = text.split()

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def add_document(text, filename):

    chunks = split_text(text)

    embeddings = embedding_model.encode(chunks)

    ids = [
        f"{filename}_{i}"
        for i in range(len(chunks))
    ]

    collection.add(
        documents=chunks,
        embeddings=embeddings.tolist(),
        ids=ids,
    )


def search_documents(query, n_results=4):

    query_embedding = embedding_model.encode(
        [query]
    )

    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=n_results,
    )

    return results["documents"][0]
