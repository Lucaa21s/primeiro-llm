from fastapi import FastAPI, UploadFile, BackgroundTasks, HTTPException
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
from app.agents.agent import run_agent
from multi_agents.supervisor import run_supervisor
from app.workflows.workflow_engine import run_workflow
from autonomous.autonomous_core import run_autonomous_system
from app.services.chat_service import build_chat_prompt, stream_chat_response
from app.services.document_service import process_document
from app.services.observability_service import register_observability
try:
    from app.services.tasks import process_document_task
except Exception:
    process_document_task = None
from app.services.redis_service import redis_ping
from experimental.api.router import register_experimental_routes
try:
    from routes.auth_routes import router as auth_router
except Exception as auth_import_error:
    auth_router = None
    logger.warning("Auth routes disabled: %s", auth_import_error)

# Importações de Sistemas Distribuídos e AGI
try:
    from distributed.orchestrator import run_distributed_ai
except Exception as distributed_import_error:
    run_distributed_ai = None
    logger.warning("Distributed routes disabled: %s", distributed_import_error)

app = FastAPI(title="Primeiro LLM")
register_observability(app)

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

if auth_router is not None:
    app.include_router(auth_router)

# Modelos de Dados Pydantic
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]

def _extract_last_message(req: ChatRequest) -> str:
    if not req.messages:
        raise HTTPException(status_code=400, detail="messages não pode ser vazio")
    content = req.messages[-1].content.strip()
    if not content:
        raise HTTPException(status_code=400, detail="mensagem final não pode ser vazia")
    return content

register_experimental_routes(app, _extract_last_message)

@app.get("/")
async def home():
    return {
        "status": "online",
        "project": "primeiro-llm"
    }

@app.get("/health/redis")
async def redis_health():
    status = redis_ping()
    if not status:
        raise HTTPException(status_code=503, detail="Redis indisponível")
    return {"status": "ok", "service": "redis"}

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    user_message = _extract_last_message(req)
    prompt = await build_chat_prompt(user_message)
    return StreamingResponse(stream_chat_response(prompt), media_type="text/plain")

@app.post("/agent")
async def agent_route(req: ChatRequest):
    user_message = _extract_last_message(req)
    result = run_agent(user_message)
    return result

@app.post("/workflow")
async def workflow_route(req: ChatRequest):
    goal = _extract_last_message(req)
    result = run_workflow(goal)
    return result

@app.post("/multi-agent")
async def multi_agent_route(req: ChatRequest):
    task = _extract_last_message(req)
    result = run_supervisor(task)
    return result

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile, background_tasks: BackgroundTasks):
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    filepath = os.path.join(upload_dir, unique_filename)
    
    async with aiofiles.open(filepath, "wb") as f:
        while chunk := await file.read(1024 * 1024): # Lê em lotes de 1MB
            await f.write(chunk)
            
    try:
        if process_document_task is None:
            raise RuntimeError("Celery indisponível")
        process_document_task.delay(filepath)
        return {"filename": unique_filename, "status": "queued"}
    except Exception:
        background_tasks.add_task(process_document, filepath)
        return {"filename": unique_filename, "status": "processing"}

@app.post("/autonomous")
async def autonomous_route(req: ChatRequest):
    goal = _extract_last_message(req)
    result = run_autonomous_system(goal)
    return result

@app.post("/distributed")
async def distributed_route(req: ChatRequest):
    if run_distributed_ai is None:
        raise HTTPException(status_code=503, detail="Distributed module indisponível")
    prompt = _extract_last_message(req)
    result = run_distributed_ai(prompt) 
    return result

@app.post("/evolve")
async def evolve_route(req: ChatRequest):
    prompt = _extract_last_message(req)

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

logger.info("API iniciada de forma assíncrona")
