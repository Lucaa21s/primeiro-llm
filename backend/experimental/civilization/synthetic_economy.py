TOKENS = {}



def reward_agent(agent, value):

    TOKENS[agent] = TOKENS.get(agent, 0) + value

    return TOKENS
