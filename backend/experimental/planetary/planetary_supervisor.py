from experimental.planetary.global_router import route_request
from experimental.planetary.hyperscale_inference import distributed_inference
from experimental.planetary.orchestration_grid import orchestrate



def planetary_control(prompt):

    route = route_request("global", prompt)

    inference = distributed_inference(prompt)

    orchestration = orchestrate(prompt)

    return {
        "route": route,
        "inference": inference,
        "orchestration": orchestration,
    }
