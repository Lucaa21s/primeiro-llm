from fastapi import FastAPI
from ollama import chat

app = FastAPI()

@app.get("/")
def home():
    return {"status": "IA Online"}

@app.get("/chat")
def conversar(pergunta: str):

    response = chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": pergunta
            }
        ]
    )

    return {
        "resposta": response["message"]["content"]
    }
