import sys
import re
import long_responses as long

def get_bot_response(self, user_input):

    def msg_prob(msg, known_words, single_resp=False, req_words=[], only_one=False):
        msg_certainty = 0
        has_req_words = True

        # Counts the amount of known words in the msg
        for word in msg:
            if word in known_words:
                msg_certainty += 1

        # Calcs the % of known words in msg
        percentage = float(msg_certainty) / float(len(known_words))

        # makes sure msg has req words
        for word in req_words:
            if only_one:
                if word in msg:
                    break
            else:
                if word not in msg:
                    has_req_words = False
                    break

        # return statement  NOTE: make it so if it has one of a required word it will still return
        if has_req_words or single_resp:
            return int(percentage*100)
        else:
            return 0

    def check_all_msgs(msg):
        highest_prob_list = {}

        def response(bot_resp, list_of_words, single_resp=False, req_words=[], only_one=False):
            nonlocal highest_prob_list
            highest_prob_list[bot_resp] = msg_prob(msg, list_of_words, single_resp, req_words, only_one)

        # Responses ------------------------------------------------------------------------
        response('Whats good!', ['hello', 'hi', 'sup', 'hey', 'heyo'], single_resp=True)
        response('robo tings', ['whats', 'up', 'what', 'are', 'you', 'doing'], req_words=['whats', 'doing'], only_one=True)
        response('Good morn to you sir', ['good', 'morning'], req_words=['morning'])
        response('good night, sleep tight', ['good', 'night', 'evening'], req_words=['night', 'evening'], only_one=True)
        response(long.R_ROBOT, ['are', 'you', 'robot'], req_words=['you', 'robot'])
        response('what', ['what', 'huh'], single_resp=True)
        response('yuh huh', ['no', 'nah', 'nope'], single_resp=True)
        response('nuh uh', ['yes', 'yep', 'yah'], single_resp=True)
        response('I\'m chillin', ['how', 'are', 'you', 'doing'], req_words=['how'])
        response('Thanks bruda', ['i', 'like', 'love', 'you'], req_words=['you'])
        response(long.R_EATING, ['what', 'you', 'eat'], req_words=['you', 'eat'])

        best_match = max(highest_prob_list, key=highest_prob_list.get)
        # print(highest_prob_list)

        return long.unknown() if highest_prob_list[best_match] < 1 else best_match

    split_msg = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = self.check_all_msgs(split_msg)
    return response

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: chat_bot_1.py <user_input>")
        sys.exit(1)

    user_input = sys.argv[1]
    bot_response = get_bot_response(user_input)
    print(bot_response)