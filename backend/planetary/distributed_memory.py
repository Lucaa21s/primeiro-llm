GLOBAL_MEMORY = {}



def save_global(key, value):

    GLOBAL_MEMORY[key] = value



def load_global(key):

    return GLOBAL_MEMORY.get(key)
