from ollama import chat

from app.agents.tools_router import execute_tool


SYSTEM_PROMPT = """
Você é um agente IA.

Você pode:

- listar arquivos
- ler pdf
- executar python

Quando precisar usar ferramenta:

RESPONDA EXATAMENTE:

TOOL: nome_tool
ARGS: {json}
"""



def run_agent(user_message):

    response = chat(
        model="llama3",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_message,
            },
        ],
    )

    content = response["message"]["content"]

    if "TOOL:" in content:

        lines = content.splitlines()

        tool_name = (
            lines[0]
            .replace("TOOL:", "")
            .strip()
        )

        args_line = (
            lines[1]
            .replace("ARGS:", "")
            .strip()
        )

        import json

        args = json.loads(args_line)

        result = execute_tool(
            tool_name,
            args,
        )

        return {
            "tool": tool_name,
            "result": result,
        }

    return {
        "response": content
    }
