

def recursive_reflection(problem, cycles=5):

    thoughts = []

    for i in range(cycles):

        thoughts.append(
            f"cycle_{i}: {problem}"
        )

    return thoughts
