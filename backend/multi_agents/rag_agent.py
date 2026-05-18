from rag_system import search_documents

def run_rag_agent(query):
    """
    Agente RAG: Executa a busca semântica de documentos 
    utilizando a raiz do sistema RAG unificado.
    """
    docs = search_documents(query)
    return docs
