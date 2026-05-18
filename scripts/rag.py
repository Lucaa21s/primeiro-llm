import os
import chromadb
from ollama import embeddings
from pypdf import PdfReader

client = chromadb.PersistentClient(path="data/chroma")

collection = client.get_or_create_collection(
    name="rag_docs"
)

PASTA_DOCS = "data/docs"


def ler_txt(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()



def ler_pdf(caminho):

    reader = PdfReader(caminho)

    texto = ""

    for pagina in reader.pages:

        conteudo = pagina.extract_text()

        if conteudo:
            texto += conteudo + "\n"

    return texto


arquivos = os.listdir(PASTA_DOCS)

for i, arquivo in enumerate(arquivos):

    caminho = os.path.join(PASTA_DOCS, arquivo)

    texto = ""

    if arquivo.endswith(".txt"):
        texto = ler_txt(caminho)

    elif arquivo.endswith(".pdf"):
        texto = ler_pdf(caminho)

    else:
        continue

    texto = texto.strip()

    if not texto:

        print(f"Ignorado vazio: {arquivo}")
        continue

    try:

        response = embeddings(
            model="nomic-embed-text",
            prompt=texto
        )

        vetor = response.get("embedding")

        if not vetor:

            print(f"Embedding vazio: {arquivo}")
            continue

        collection.add(
            ids=[str(i)],
            embeddings=[vetor],
            documents=[texto]
        )

        print(f"Indexado: {arquivo}")

    except Exception as e:

        print(f"Erro em {arquivo}: {e}")