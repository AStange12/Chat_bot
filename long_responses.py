import random

#long responses
R_EATING = "I don't eat, stoopid"
R_ROBOT = "Yessir, I do be made of lines of code"

#returns random resp
def unknown():
    responses = ['Could you re-phrase that?', '...', 'Sounds about right', 'I don\'t really care', 'Whatever', 'huh']
    return responses[random.randrange(len(responses))]
