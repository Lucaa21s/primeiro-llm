from ollama import chat
from memory import salvar_memoria, buscar_memorias

contador = 0

print("Memória IA iniciada.")
print("Digite 'sair' para encerrar.\n")

while True:

    pergunta = input("Você: ")

    if pergunta.lower() in ["sair", "exit", "quit"]:
        break

    memorias = buscar_memorias(pergunta)

    contexto = "\n".join(memorias)

    prompt = f"""
Use as memórias abaixo para responder.

Memórias:
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

    resposta = response["message"]["content"]

    print("\nIA:")
    print(resposta)
    print()

    salvar_memoria(
        f"Usuário: {pergunta}\nIA: {resposta}",
        contador
    )

    contador += 1