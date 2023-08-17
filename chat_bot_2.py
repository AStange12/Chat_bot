from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from difflib import get_close_matches

class ChatBot2Handler(BaseHTTPRequestHandler):
    # ... your existing load_json, save_json, find_best_match, get_answer_for_question functions ...
    def load_json(file_path: str) -> dict:
        with open(file_path, 'r') as file:
            data: dict = json.load(file)
        return data

    def save_json(file_path: str, data: dict):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)

    def find_best_match(user_question: str, questions: list[str]) -> str | None:
        matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
        return matches[0] if matches else None

    def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
        for q in knowledge_base["questions"]:
            if q["question"] == question:
                return q["answer"]
            
    def chat_bot(self):
        knowledge_base = self.load_json('knowledge_base.json')

        while True:
            user_input = input('You: ')

            if user_input.lower() == 'quit':
                break

            best_match = self.find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

            if best_match:
                answer = self.get_answer_for_question(best_match, knowledge_base)
                print('bot:', answer)
            else:
                print("Bot: I don't understand. Can you teach me?")
                new_answer = input('Type the answer or "skip" to skip: ')

                if new_answer.lower() != 'skip':
                    knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                    self.save_json('knowledge_base.json', knowledge_base)
                    print('Bot: Thank you for teaching me')

if __name__ == '__main__':
    server_address = ('', 8001)
    httpd = HTTPServer(server_address, ChatBot2Handler)
    print('Starting server for Chat Bot 2 on port 8001...')
    httpd.serve_forever()
