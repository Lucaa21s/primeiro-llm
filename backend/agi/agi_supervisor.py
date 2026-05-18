from agi.adaptive_planner import create_plan
from agi.recursive_cognition import recursive_reflection
from agi.universal_reasoning import reason



def supervise(problem):

    reasoning = reason(problem)

    plan = create_plan(problem)

    reflection = recursive_reflection(problem)

    return {
        "reasoning": reasoning,
        "plan": plan,
        "reflection": reflection,
    }
