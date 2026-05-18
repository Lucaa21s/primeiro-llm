from autonomous.planner import create_plan
from autonomous.executor import execute_tasks
from autonomous.reflection import reflect



def autonomous_loop(goal):

    plan = create_plan(goal)

    tasks = [
        line
        for line in plan.splitlines()
        if line.strip()
    ]

    results = execute_tasks(tasks)

    reflection = reflect(results)

    return {
        "goal": goal,
        "plan": plan,
        "results": results,
        "reflection": reflection,
    }
