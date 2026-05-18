from ollama import chat


SYSTEM_PROMPT = """
Você é um especialista em programação.

Especialidades:
- Python
- FastAPI
- Next.js
- IA
- automação
"""



def run_coding_agent(task):

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
