from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

# DeepSeek API details
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
#Enter your API Key Here
DEEPSEEK_API_KEY = "API key here"

# LangChain integration (simplified for this example)
class Chatbot:
    def __init__(self):
        self.conversation_history = []

    def generate_response(self, user_input):
    # Add user input to conversation history
     self.conversation_history.append({"role": "user", "content": user_input})

    # Prepare the payload for DeepSeek API
     payload = {
        "model": "deepseek-chat",
        "messages": self.conversation_history,
        "max_tokens": 150
     }

     headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
     }

    # Call DeepSeek API
     response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)
    
    # Print the full API response and status code for debugging
     print("DeepSeek API Status Code:", response.status_code)
     print("DeepSeek API Response:", response.json())

    # Check if the request was successful
     if response.status_code != 200:
        return "Error: Unable to get a response from the API."

     response_data = response.json()

    # Check if the response contains the expected structure
     if "choices" not in response_data:
        return "Error: Invalid response format from the API."

    # Extract the chatbot's reply
     chatbot_reply = response_data["choices"][0]["message"]["content"]

    # Add chatbot's reply to conversation history
     self.conversation_history.append({"role": "assistant", "content": chatbot_reply})

     return chatbot_reply

# Initialize the chatbot
chatbot = Chatbot()

# Serve the front-end (index.html)
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

# Flask route to handle chat requests
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Generate response using the chatbot
    response = chatbot.generate_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
