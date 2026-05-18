# Expõe o orquestrador nativo da sua pasta local para o main.py
from .orchestrator import run_distributed_ai as orchestrator

class Client:
    """
    Client de Simulação Enterprise para o Cluster de IA Distribuído.
    """
    def __init__(self):
        self.status = "connected"
