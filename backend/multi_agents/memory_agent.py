from memory.memory_system import save_memory



def run_memory_agent(user_id, text):

    save_memory(user_id, text)

    return {
        "status": "saved"
    }
