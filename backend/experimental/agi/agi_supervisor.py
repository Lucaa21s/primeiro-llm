from experimental.agi.adaptive_planner import create_plan
from experimental.agi.recursive_cognition import recursive_reflection
from experimental.agi.universal_reasoning import reason



def supervise(problem):

    reasoning = reason(problem)

    plan = create_plan(problem)

    reflection = recursive_reflection(problem)

    return {
        "reasoning": reasoning,
        "plan": plan,
        "reflection": reflection,
    }
