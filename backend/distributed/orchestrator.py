from distributed.inference_router import distributed_inference



def run_distributed_ai(prompt):

    result = distributed_inference(prompt)

    return result
