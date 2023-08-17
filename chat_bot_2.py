from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from difflib import get_close_matches

class ChatBotHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow requests from any origin
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')  # Allow POST and OPTIONS requests
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        user_message = json.loads(post_data)['message']

        bot_response = self.get_bot_response(user_message)

        self._set_response()
        response = {'bot_response': bot_response}
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def load_json(self, file_path: str) -> dict:
        with open(file_path, 'r') as file:
            data: dict = json.load(file)
        return data

    def save_json(self, file_path: str, data: dict):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)

    def find_best_match(self, user_question: str, questions: list[str]) -> str | None:
        matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
        return matches[0] if matches else None

    def get_answer_for_question(self, question: str, knowledge_base: dict) -> str | None:
        for q in knowledge_base["questions"]:
            if q["question"] == question:
                return q["answer"]

    def get_bot_response(self, user_input):
        knowledge_base = self.load_json('knowledge_base.json')
        best_match = self.find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer = self.get_answer_for_question(best_match, knowledge_base)
            return answer
        else:
            new_answer = input("Bot: I don't understand. Can you teach me? Type the answer or 'skip' to skip: ")
            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                self.save_json('knowledge_base.json', knowledge_base)
                return "Thank you for teaching me"
            else:
                return "I'm sorry I couldn't learn from you this time."

if __name__ == '__main__':
    server_address = ('localhost', 8001) 
    httpd = HTTPServer(server_address, ChatBotHandler)
    print('Starting server on port 8001...')
    httpd.serve_forever()