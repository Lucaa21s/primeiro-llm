from pypdf import PdfReader

arquivo = "data/docs/manual.pdf"

reader = PdfReader(arquivo)

print(f"Páginas: {len(reader.pages)}\n")

texto_total = ""

for i, pagina in enumerate(reader.pages):

    texto = pagina.extract_text()

    if texto:

        print(f"Página {i + 1}\n")
        print(texto[:1000])
        print("\n" + "=" * 50 + "\n")

        texto_total += texto + "\n"

print("PDF lido com sucesso.")
