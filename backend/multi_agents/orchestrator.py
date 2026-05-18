from multi_agents.coding_agent import run_coding_agent
from multi_agents.research_agent import run_research_agent
from multi_agents.rag_agent import run_rag_agent
from multi_agents.workflow_agent import run_workflow_agent



def orchestrate(task, agent_type):

    if agent_type == "coding":
        return run_coding_agent(task)

    if agent_type == "research":
        return run_research_agent(task)

    if agent_type == "rag":
        return run_rag_agent(task)

    if agent_type == "workflow":
        return run_workflow_agent(task)

    return "Agent não encontrado"
