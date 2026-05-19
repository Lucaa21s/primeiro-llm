from app.agents.agent import run_agent



def execute_plan(plan_text):

    lines = plan_text.splitlines()

    results = []

    for line in lines:

        if line.strip() == "":
            continue

        result = run_agent(line)

        results.append({
            "step": line,
            "result": result,
        })

    return results
