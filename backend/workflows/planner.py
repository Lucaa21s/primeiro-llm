from ollama import chat


SYSTEM_PROMPT = """
Você é um planner de workflows.

Quebra tarefas complexas em passos.
"""



def create_plan(user_goal):

    response = chat(
        model="llama3",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_goal,
            },
        ],
    )

    return response["message"]["content"]
1222