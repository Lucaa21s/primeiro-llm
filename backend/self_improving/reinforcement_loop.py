from self_improving.scoring_engine import score_response



def reinforcement_cycle(response):

    score = score_response(response)

    return {
        "score": score,
        "status": "improved",
    }
