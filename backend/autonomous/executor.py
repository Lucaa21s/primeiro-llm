from multi_agents.supervisor import run_supervisor



def execute_tasks(tasks):

    results = []

    for task in tasks:

        result = run_supervisor(task)

        results.append({
            "task": task,
            "result": result,
        })

    return results
