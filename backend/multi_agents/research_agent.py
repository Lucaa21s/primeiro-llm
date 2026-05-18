from ollama import chat


SYSTEM_PROMPT = """
Você é um agente de pesquisa.

Especialidades:
- análise
- pesquisa
- resumo
- documentação
"""



def run_research_agent(task):

    response = chat(
        model="llama3",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": task,
            },
        ],
    )

    return response["message"]["content"]
