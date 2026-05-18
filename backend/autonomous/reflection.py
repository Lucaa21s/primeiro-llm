from ollama import chat


SYSTEM_PROMPT = """
Analise resultados.

Detecte:
- erros
- melhorias
- otimizações
"""



def reflect(results):

    response = chat(
        model="llama3",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": str(results),
            },
        ],
    )

    return response["message"]["content"]
