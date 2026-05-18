import os
import logging
import ollama
from multi_agents.orchestrator import orchestrate

# Configuração de logs para monitoramento na Fase 14/15
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AI_Supervisor")

SYSTEM_PROMPT = """
Você é um supervisor de agentes altamente qualificado.

Analise a tarefa do usuário e escolha qual agente especializado deve tratá-la:
- coding (Para desenvolvimento, correção e análise de código/scripts)
- research (Para buscas aprofundadas, explicações conceituais e sínteses)
- rag (Para consultas que exijam busca de documentos ou dados externos)
- workflow (Para processos sequenciais, automações e pipelines de tarefas)

Responda estritamente no formato abaixo, sem saudações ou justificativas:
AGENT: nome
"""

def get_best_model(client: ollama.Client) -> str:
    """Descobre dinamicamente o melhor modelo disponível ou lê do ambiente."""
    env_model = os.getenv("OLLAMA_MODEL")
    if env_model:
        return env_model
    try:
        models_list = client.list()
        available_models = [m['model'] for m in models_list.get('models', [])]
        priority_list = ["llama3.1:latest", "llama3.1", "llama3:latest", "llama3", "mistral:latest", "mistral"]
        for model in priority_list:
            if model in available_models:
                return model
        if available_models:
            return available_models[0]
    except Exception as e:
        logger.warning(f"Falha ao listar modelos do Ollama: {str(e)}")
    return "llama3"

def run_supervisor(task: str) -> dict:
    """
    Supervisor Inteligente: Decide a melhor especialidade para resolver
    a tarefa e despacha a execução utilizando modelo dinâmico e rede corrigida.
    """
    logger.info(f"Recebendo nova diretriz de orquestração: '{task[:50]}...'")

    try:
        # Configura o endpoint de rede do contêiner e instancia o cliente
        ollama_host = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
        client = ollama.Client(host=ollama_host)
        
        # Seleção automatizada do modelo na GPU (RTX 3060)
        chosen_model = get_best_model(client)
        logger.info(f"Supervisor utilizando o modelo dinâmico: '{chosen_model}'")

        response = client.chat(
            model=chosen_model,
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

        # Captura e higieniza a saída de texto do modelo local
        raw_decision = response["message"]["content"].strip()
        logger.info(f"Decisão bruta do modelo Ollama: '{raw_decision}'")

        # Processamento seguro para extrair o nome do agente
        decision = "research"
        if "AGENT:" in raw_decision:
            decision = raw_decision.split("AGENT:")[-1].strip().lower()
        elif ":" in raw_decision:
            decision = raw_decision.split(":")[-1].strip().lower()

        # Aciona o motor de orquestração distribuído
        logger.info(f"Despachando fluxo operacional para o agente: '{decision}'")
        execution_result = orchestrate(decision, task)

        return {
            "status": "success",
            "selected_agent": decision,
            "task_forwarded": task,
            "result": execution_result
        }

    except Exception as e:
        logger.error(f"Falha crítica no loop do supervisor: {str(e)}")
        return {
            "status": "error",
            "message": f"Erro interno na camada do Supervisor AI: {str(e)}",
            "fallback_agent": "research"
        }
