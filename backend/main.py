from fastapi import FastAPI, File, UploadFile, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import ollama
from ollama import AsyncClient
import uuid
import aiofiles
import os

from app.core.logger import logger

# Importações de Sistemas Core e Evolutivos
from self_improving.evolution_manager import evolve
from rag_system import search_documents, add_document
from memory_system import save_memory, search_memory
from pypdf import PdfReader
import asyncio
from app.agents.agent import run_agent
from multi_agents.supervisor import run_supervisor
from app.workflows.workflow_engine import run_workflow
from autonomous.autonomous_core import run_autonomous_system
from routes.auth_routes import router as auth_router

# Importações de Sistemas Distribuídos e AGI
from distributed import Client
from distributed.orchestrator import run_distributed_ai
from civilization.civilization_core import initialize_civilization
from civilization.evolution_cycle import evolve_civilization
from agi.agi_supervisor import supervise

app = FastAPI(title="Primeiro LLM")

# Configuração de CORS para comunicação com o Frontend
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
env_origins = os.getenv("CORS_ORIGINS")
if env_origins:
    origins.extend([origin.strip() for origin in env_origins.split(",") if origin.strip()])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
async def home():
    return {
        "status": "online",
        "project": "primeiro-llm"
    }

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    user_message = req.messages[-1].content
    
    # Busca assíncrona vetorial via pgvector
    memory_context = await search_memory(user_message)
    rag_context = await search_documents(user_message)

    final_prompt = f"""
Você é uma IA moderna.

Memórias relevantes:
{memory_context}

Contexto encontrado:
{rag_context}

Pergunta:
{user_message}
"""
    await save_memory(user_message)

    async def generate():
        client = AsyncClient(host=os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434"))
        stream_response = await client.chat(
            model="llama3",
            messages=[
                {
                    "role": "user",
                    "content": final_prompt,
                }
            ],
            stream=True
        )

        async for chunk in stream_response:
            yield chunk["message"]["content"]

    return StreamingResponse(generate(), media_type="text/plain")

@app.post("/agent")
async def agent_route(req: ChatRequest):
    user_message = req.messages[-1].content
    result = run_agent(user_message)
    return result

@app.post("/workflow")
async def workflow_route(req: ChatRequest):
    goal = req.messages[-1].content
    result = run_workflow(goal)
    return result

@app.post("/multi-agent")
async def multi_agent_route(req: ChatRequest):
    task = req.messages[-1].content
    result = run_supervisor(task)
    return result

async def process_document(filepath: str):
    logger.info(f"Extraindo texto e gerando vetores: {filepath}")
    try:
        reader = PdfReader(filepath)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\\n"
        
        await add_document(text, filepath)
        logger.info(f"PDF processado e injetado no pgvector: {filepath}")
    except Exception as e:
        logger.error(f"Erro ao processar PDF {filepath}: {e}")

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile, background_tasks: BackgroundTasks):
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    filepath = os.path.join(upload_dir, unique_filename)
    
    async with aiofiles.open(filepath, "wb") as f:
        while chunk := await file.read(1024 * 1024): # Lê em lotes de 1MB
            await f.write(chunk)
            
    background_tasks.add_task(process_document, filepath)
    return {"filename": unique_filename, "status": "processing"}

@app.post("/autonomous")
async def autonomous_route(req: ChatRequest):
    goal = req.messages[-1].content
    result = run_autonomous_system(goal)
    return result

@app.post("/distributed")
async def distributed_route(req: ChatRequest):
    prompt = req.messages[-1].content
    result = run_distributed_ai(prompt) 
    return result

@app.post("/evolve")
async def evolve_route(req: ChatRequest):
    prompt = req.messages[-1].content

    # Configura a ponte de rede correta com o host externo do Docker
    ollama_host = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
    client = AsyncClient(host=ollama_host)
    sync_client = ollama.Client(host=ollama_host)

    # Descobre e seleciona automaticamente o melhor modelo instalado
    chosen_model = "llama3"
    try:
        models_list = sync_client.list()
        available_models = [m['model'] for m in models_list.get('models', [])]
        priority_list = ["llama3.1:latest", "llama3.1", "llama3:latest", "llama3", "mistral:latest"]
        for model in priority_list:
            if model in available_models:
                chosen_model = model
                break
    except Exception:
        pass

    # Realiza a inferência acelerada por hardware de forma assíncrona
    response = await client.chat(
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
async def initialize_civilization_route():
    return initialize_civilization()

@app.post("/evolve-civilization")
async def evolve_civilization_route():
    return evolve_civilization("")

@app.get("/civilization")
async def civilization_status():
    return initialize_civilization()

@app.post("/civilization/evolve")
async def civilization_evolve(req: ChatRequest):
    prompt = req.messages[-1].content
    return evolve_civilization(prompt)

@app.post("/supervise")
async def supervise_route(req: ChatRequest):
    task = req.messages[-1].content
    return supervise(task)

@app.post("/agi")
async def agi_route(req: ChatRequest):
    prompt = req.messages[-1].content
    return supervise(prompt)

logger.info("API iniciada de forma assíncrona")
