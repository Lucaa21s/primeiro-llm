from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import ollama
from ollama import chat

# Importações de Sistemas Core e Evolutivos
from self_improving.evolution_manager import evolve
from rag_system import search_documents
from memory_system import save_memory, search_memory
from agents.agent import run_agent
from multi_agents.supervisor import run_supervisor
from workflows.workflow_engine import run_workflow
from autonomous.autonomous_core import run_autonomous_system
from routes.auth_routes import router as auth_router

# Importações de Sistemas Distribuídos e AGI
from distributed import Client
from distributed.orchestrator import run_distributed_ai
from civilization.civilization_core import initialize_civilization
from civilization.evolution_cycle import evolve_civilization
from agi.agi_supervisor import supervise

app = FastAPI()

# Configuração de CORS para comunicação com o Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

# Modelos de Dados Pydantic
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]

@app.get("/")
def home():
    return {
        "status": "online"
    }

@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    user_message = req.messages[-1].content
    memory_context = search_memory(user_message)
    rag_context = search_documents(user_message)

    final_prompt = f"""
Você é uma IA moderna.

Memórias relevantes:
{memory_context}

Contexto encontrado:
{rag_context}

Pergunta:
{user_message}
"""
    save_memory(user_message)

    def generate():
        # Correção Crítica: Adicionado stream=True e extração limpa do chunk de texto
        stream_response = chat(
            model="llama3",
            messages=[
                {
                    "role": "user",
                    "content": final_prompt,
                }
            ],
            stream=True
        )

        for chunk in stream_response:
            yield chunk["message"]["content"]

    return StreamingResponse(generate(), media_type="text/plain")

@app.post("/agent")
def agent_route(req: ChatRequest):
    user_message = req.messages[-1].content
    result = run_agent(user_message)
    return result

@app.post("/workflow")
def workflow_route(req: ChatRequest):
    goal = req.messages[-1].content
    result = run_workflow(goal)
    return result

@app.post("/multi-agent")
def multi_agent_route(req: ChatRequest):
    task = req.messages[-1].content
    result = run_supervisor(task)
    return result

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    with open("uploaded_file.pdf", "wb") as f:
        f.write(await file.read())
    return {"filename": file.filename}

@app.post("/autonomous")
def autonomous_route(req: ChatRequest):
    goal = req.messages[-1].content
    result = run_autonomous_system(goal)
    return result

@app.post("/distributed")
def distributed_route(req: ChatRequest):
    prompt = req.messages[-1].content
    result = run_distributed_ai(prompt) # <--- Garanta que chama a função correta
    return result

@app.post("/evolve")
def evolve_route(req: ChatRequest):
    import os
    
    prompt = req.messages[-1].content

    # Configura a ponte de rede correta com o host externo do Docker
    ollama_host = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
    client = ollama.Client(host=ollama_host)

    # Descobre e seleciona automaticamente o melhor modelo instalado na sua GPU
    chosen_model = "llama3"
    try:
        models_list = client.list()
        available_models = [m['model'] for m in models_list.get('models', [])]
        priority_list = ["llama3.1:latest", "llama3.1", "llama3:latest", "llama3", "mistral:latest"]
        for model in priority_list:
            if model in available_models:
                chosen_model = model
                break
    except Exception:
        pass

    # Realiza a inferência acelerada por hardware na RTX 3060
    response = client.chat(
        model=chosen_model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    answer = response["message"]["content"]
    
    # Aciona o Evolution Manager da Fase 15
    evolved = evolve(prompt, answer)
    return evolved

@app.post("/initialize-civilization")
def initialize_civilization_route():
    return initialize_civilization()

@app.post("/evolve-civilization")
def evolve_civilization_route():
    return evolve_civilization("")

@app.get("/civilization")
def civilization_status():
    return initialize_civilization()

@app.post("/civilization/evolve")
def civilization_evolve(req: ChatRequest):
    prompt = req.messages[-1].content
    return evolve_civilization(prompt)

@app.post("/supervise")
def supervise_route(req: ChatRequest):
    task = req.messages[-1].content
    return supervise(task)

@app.post("/agi")
def agi_route(req: ChatRequest):
    prompt = req.messages[-1].content
    return supervise(prompt)
