from interplanetary.cosmic_router import route_cosmic
from interplanetary.deep_space_reasoning import reason_space
from interplanetary.cosmic_orchestrator import orchestrate_cosmic



def supervise_cosmic(prompt):

    route = route_cosmic("mars", prompt)

    reasoning = reason_space(prompt)

    orchestration = orchestrate_cosmic(prompt)

    return {
        "route": route,
        "reasoning": reasoning,
        "orchestration": orchestration,
    }
