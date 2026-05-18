from planetary.global_router import route_request
from planetary.hyperscale_inference import distributed_inference
from planetary.orchestration_grid import orchestrate



def planetary_control(prompt):

    route = route_request("global", prompt)

    inference = distributed_inference(prompt)

    orchestration = orchestrate(prompt)

    return {
        "route": route,
        "inference": inference,
        "orchestration": orchestration,
    }
