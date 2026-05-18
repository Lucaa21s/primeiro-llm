import chromadb
from ollama import embeddings, chat

client = chromadb.PersistentClient(path="data/chroma")

try:

    collection = client.get_collection("rag_docs")

except:

    print("Coleção RAG não encontrada.")
    print("Execute primeiro:")
    print("python scripts/rag.py")
    exit()


while True:

    pergunta = input("\nPergunta: ")

    if pergunta.lower() in ["sair", "exit", "quit"]:
        break

    query = embeddings(
        model="nomic-embed-text",
        prompt=pergunta
    )

    resultado = collection.query(
        query_embeddings=[query["embedding"]],
        n_results=2
    )

    documentos = resultado.get("documents")

    if not documentos:

        print("Nenhum contexto encontrado.")
        continue

    contexto = "\n".join(documentos[0])

    prompt = f"""
Use o contexto abaixo para responder.

Contexto:
{contexto}

Pergunta:
{pergunta}
"""

    response = chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print("\nResposta:\n")
    print(response["message"]["content"])