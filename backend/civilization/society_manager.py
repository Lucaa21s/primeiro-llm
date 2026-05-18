AGENTS = [
    "research_agent",
    "planning_agent",
    "economy_agent",
    "memory_agent",
]



def create_society():

    return {
        "agents": AGENTS,
        "population": len(AGENTS),
    }
