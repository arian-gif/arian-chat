from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("API_KEY")
debug_mode = os.getenv("DEBUG", "False") == "True"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

app = Flask(__name__)

chat_data = [
    {"sender": "bot", "message": "Welcome! Ask me anything, or just say hi. 🌟"}
]

@app.route("/")
def chat():
    return render_template("index.html",chat_data=chat_data)

@app.route("/chat", methods=["POST"])
def ai():
    data = request.get_json()
    user_input = data.get("message") if data else None

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    response = model.generate_content(user_input)
    reply = response.text

    chat_data.append({"sender": "user", "message": user_input})
    chat_data.append({"sender": "bot", "message": reply})

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run()