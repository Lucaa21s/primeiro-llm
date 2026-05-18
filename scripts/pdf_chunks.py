from pypdf import PdfReader

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
    chunks.append(chunk)


print(f"Chunks criados: {len(chunks)}\n")

for i, chunk in enumerate(chunks[:3]):

    print(f"Chunk {i + 1}\n")
    print(chunk)
    print("\n" + "=" * 50 + "\n")