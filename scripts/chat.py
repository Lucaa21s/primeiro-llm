from ollama import chat

response = chat(
    model='llama3',
    messages=[
        {
            'role': 'user',
            'content': 'Explique inteligência artificial de forma simples.'
        }
    ]
)

print(response['message']['content'])
