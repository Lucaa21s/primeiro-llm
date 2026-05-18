from ollama import embeddings

texto = "Inteligência artificial está transformando o mundo."

response = embeddings(
    model='nomic-embed-text',
    prompt=texto
)

vetor = response['embedding']

print(f"Tamanho do vetor: {len(vetor)}")
print(vetor[:10])