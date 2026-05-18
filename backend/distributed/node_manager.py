NODES = [
    {
        "name": "node-1",
        "host": "http://localhost:11434",
        "gpu": "RTX 3060",
        "status": "online",
    }
]



def get_available_nodes():

    return [
        node
        for node in NODES
        if node["status"] == "online"
    ]
