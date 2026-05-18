import chromadb
from ollama import embeddings

client = chromadb.PersistentClient(path="data/chroma")

collection = client.get_collection("pdf_docs")

pergunta = input("Pergunta: ")

response = embeddings(
    model="nomic-embed-text",
    prompt=pergunta
)

resultado = collection.query(
    query_embeddings=[response["embedding"]],
    n_results=3
)

print("\nResultados:\n")

for item in resultado["documents"][0]:

    print(item)
    print("\n" + "=" * 50 + "\n")