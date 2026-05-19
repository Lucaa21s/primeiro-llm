

def recursive_think(problem, depth=3):

    thoughts = []

    for i in range(depth):

        thoughts.append(
            f"reflection_level_{i}: {problem}"
        )

    return thoughts
