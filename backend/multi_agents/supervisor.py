import logging
from ollama import chat
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

def run_supervisor(task: str) -> dict:
    """
    Supervisor Inteligente: Decide a melhor especialidade para resolver
    a tarefa e despacha a execução diretamente para o orquestrador distribuído.
    """
    logger.info(f"Recebendo nova diretriz de orquestração: '{task[:50]}...'")

    try:
        # Inferência local acelerada por hardware (RTX 3060)
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

        # Captura e higieniza a saída de texto do modelo local
        raw_decision = response["message"]["content"].strip()
        logger.info(f"Decisão bruta do modelo Ollama: '{raw_decision}'")

        # Processamento seguro para extrair o nome do agente (mesmo se o LLM falhar na formatação)
        decision = "research" # Fallback padrão caso o retorno venha corrompido
        if "AGENT:" in raw_decision:
            decision = raw_decision.split("AGENT:")[-1].strip().lower()
        elif ":" in raw_decision:
            decision = raw_decision.split(":")[-1].strip().lower()

        # Aciona o motor de orquestração distribuído da Fase 15
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
