from pypdf import PdfReader
from ollama import embeddings
import chromadb

client = chromadb.PersistentClient(path="data/chroma")

collection = client.get_or_create_collection(
    name="pdf_docs"
)

arquivo = "data/docs/manual.pdf"

reader = PdfReader(arquivo)

texto_total = ""

for pagina in reader.pages:

    texto = pagina.extract_text()

    if texto:
        texto_total += texto + "\n"


TAMANHO_CHUNK = 500

chunks = []

for i in range(0, len(texto_total), TAMANHO_CHUNK):

    chunk = texto_total[i:i + TAMANHO_CHUNK]

    if chunk.strip():
        chunks.append(chunk)


for i, chunk in enumerate(chunks):

    response = embeddings(
        model="nomic-embed-text",
        prompt=chunk
    )

    vetor = response.get("embedding")

    if not vetor:
        continue

    collection.add(
        ids=[str(i)],
        embeddings=[vetor],
        documents=[chunk]
    )

    print(f"Chunk indexado: {i}")

print("\nPDF indexado com sucesso.")