GALACTIC_MEMORY = {}



def save_memory(key, value):

    GALACTIC_MEMORY[key] = value



def recall_memory(key):

    return GALACTIC_MEMORY.get(key)
