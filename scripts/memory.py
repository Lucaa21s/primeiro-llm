import chromadb
from ollama import embeddings

client = chromadb.PersistentClient(path="data/chroma")

collection = client.get_or_create_collection(
    name="memory"
)


def salvar_memoria(texto, memoria_id):

    response = embeddings(
        model="nomic-embed-text",
        prompt=texto
    )

    vetor = response["embedding"]

    collection.add(
        ids=[str(memoria_id)],
        embeddings=[vetor],
        documents=[texto]
    )



def buscar_memorias(pergunta, limite=3):

    response = embeddings(
        model="nomic-embed-text",
        prompt=pergunta
    )

    resultado = collection.query(
        query_embeddings=[response["embedding"]],
        n_results=limite
    )

    return resultado["documents"][0]