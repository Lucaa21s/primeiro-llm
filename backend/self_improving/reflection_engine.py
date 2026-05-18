import os
import ollama

def get_best_model(client):
    """Descobre dinamicamente o melhor modelo disponível no Ollama local."""
    # 1. Tenta pegar o modelo definido na variável de ambiente do Docker
    env_model = os.getenv("OLLAMA_MODEL")
    if env_model:
        return env_model

    try:
        # 2. Se não houver variável, lista os modelos baixados na GPU
        models_list = client.list()
        available_models = [m['model'] for m in models_list.get('models', [])]
        
        # Lista de prioridade dos melhores modelos do mercado local
        priority_list = ["llama3.1:latest", "llama3.1", "llama3:latest", "llama3", "mistral:latest", "mistral", "gemma:latest"]
        
        for model in priority_list:
            if model in available_models:
                return model
                
        # 3. Se não achar nenhum da lista, pega o primeiro que encontrar instalado
        if available_models:
            return available_models[0]
            
    except Exception:
        pass
        
    # Fallback de segurança absoluto
    return "llama3"

def reflect_response(prompt, response):
    ollama_host = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
    client = ollama.Client(host=ollama_host)
    
    # Escolha automática do melhor modelo
    chosen_model = get_best_model(client)
    
    reflection_prompt = f'''
 Analise esta resposta da IA.
 Pergunta:
{prompt}
 Resposta:
{response}
 Avalie:
 - clareza
 - precisão
 - melhoria possível
 - otimização
 '''
    result = client.chat(
        model=chosen_model, # <--- Modelo dinâmico e automatizado!
        messages=[
            {
                "role": "user",
                "content": reflection_prompt,
            }
        ],
    )
    return result["message"]["content"]
