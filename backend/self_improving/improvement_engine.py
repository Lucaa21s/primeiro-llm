from self_improving.reflection_engine import reflect_response



def improve_answer(prompt, response):

    reflection = reflect_response(prompt, response)

    return {
        "original": response,
        "reflection": reflection,
    }
