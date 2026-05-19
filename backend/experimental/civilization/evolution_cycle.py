from experimental.civilization.recursive_reasoning import recursive_think



def evolve_civilization(problem):

    thoughts = recursive_think(problem)

    return {
        "evolution": thoughts,
        "status": "evolving",
    }
