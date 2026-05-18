from ollama import chat


SYSTEM_PROMPT = """
Você é um planner autônomo.

Quebre objetivos em etapas.
"""



def create_plan(goal):

    response = chat(
        model="llama3",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": goal,
            },
        ],
    )

    return response["message"]["content"]
