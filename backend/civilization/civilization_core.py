from civilization.society_manager import create_society



def initialize_civilization():

    society = create_society()

    return {
        "civilization": "online",
        "society": society,
    }
 