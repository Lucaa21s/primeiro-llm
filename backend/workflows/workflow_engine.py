from workflows.planner import create_plan
from workflows.executor import execute_plan



def run_workflow(goal):

    plan = create_plan(goal)

    results = execute_plan(plan)

    return {
        "goal": goal,
        "plan": plan,
        "results": results,
    }
