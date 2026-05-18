from self_improving.auto_optimizer import optimize_prompt
from self_improving.improvement_engine import improve_answer
from self_improving.reinforcement_loop import reinforcement_cycle



def evolve(prompt, response):

    optimized_prompt = optimize_prompt(prompt)

    improved = improve_answer(prompt, response)

    reinforcement = reinforcement_cycle(response)

    return {
        "optimized_prompt": optimized_prompt,
        "improved": improved,
        "reinforcement": reinforcement,
    }
