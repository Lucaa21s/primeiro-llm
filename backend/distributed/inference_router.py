import requests

from distributed.load_balancer import select_node



def distributed_inference(prompt):

    node = select_node()

    response = requests.post(
        f"{node['host']}/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False,
        },
    )

    return response.json()
