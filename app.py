from flask import Flask, render_template, request, jsonify
from chatbot import chatbot_response
import uuid

app = Flask(__name__)

chats = {}
current_id = str(uuid.uuid4())
chats[current_id] = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global current_id
    user_message = request.json.get("message")
    bot_reply = chatbot_response(user_message)
    chats[current_id].append({"user": user_message, "bot": bot_reply})
    return jsonify({"reply": bot_reply})

@app.route("/new_chat", methods=["POST"])
def new_chat():
    global current_id
    current_id = str(uuid.uuid4())
    chats[current_id] = []
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
