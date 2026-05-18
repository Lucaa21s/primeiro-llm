import chromadb
from ollama import embeddings

client = chromadb.PersistentClient(
    path="data/chroma"
)

collection = client.get_collection(
    name="documentos"
)

while True:

    pergunta = input("\nBusca: ")

    if pergunta.lower() in ["sair", "exit", "quit"]:
        break

    response = embeddings(
        model="nomic-embed-text",
        prompt=pergunta
    )

    vetor = response.get("embedding")

    if not vetor:
        print("Erro no embedding.")
        continue

    resultado = collection.query(
        query_embeddings=[vetor],
        n_results=3
    )

    documentos = resultado.get("documents")

    if not documentos:
        print("Nenhum resultado.")
        continue

    print("\nResultados:\n")

    for item in documentos[0]:

        print(item)
        print("\n" + "=" * 50)