import chromadb
from ollama import embeddings

client = chromadb.PersistentClient(
    path="data/chroma"
)

collection = client.get_or_create_collection(
    name="documentos"
)

textos = [
    "Python é uma linguagem moderna.",
    "CUDA acelera inteligência artificial.",
    "Ollama executa modelos localmente.",
    "RAG combina busca vetorial com LLMs.",
]

for i, texto in enumerate(textos):

    response = embeddings(
        model="nomic-embed-text",
        prompt=texto
    )

    vetor = response.get("embedding")

    if not vetor:
        continue

    collection.add(
        ids=[str(i)],
        embeddings=[vetor],
        documents=[texto]
    )

    print(f"Documento indexado: {i}")

print("\nBanco vetorial criado.")