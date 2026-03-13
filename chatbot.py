from flask import Flask, request, jsonify, send_from_directory
import json
import os
import uuid
from openai import OpenAI

app = Flask(__name__)


client = OpenAI(api_key="API_KEY")

HISTORY_FILE = "history/history.json"

# Create history folder if it doesn't exist
os.makedirs("history", exist_ok=True)

# Create history file if missing
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)


# Load chat history
def load_history():
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)


# Save chat history
def save_history(data):
    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


# Serve homepage
@app.route("/")
def home():
    return send_from_directory(".", "index.html")


# Send message to AI
@app.route("/send_message", methods=["POST"])
def send_message():

    data = request.json
    user_message = data.get("message", "")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        bot_reply = response.choices[0].message.content

    except Exception as e:
        import traceback
        traceback.print_exc()
        bot_reply = "⚠️ AI temporarily unavailable."

    history = load_history()

    new_chat = {
        "id": str(uuid.uuid4()),
        "user": user_message,
        "bot": bot_reply,
        "pinned": False,
        "archived": False
    }

    history.append(new_chat)

    save_history(history)

    return jsonify({"reply": bot_reply})


# Get all chat history
@app.route("/get_history")
def get_history():
    return jsonify(load_history())


# Delete chat
@app.route("/delete_chat", methods=["POST"])
def delete_chat():

    chat_id = request.json["id"]

    history = load_history()

    history = [c for c in history if c["id"] != chat_id]

    save_history(history)

    return jsonify({"status": "deleted"})


# Rename chat
@app.route("/rename_chat", methods=["POST"])
def rename_chat():

    chat_id = request.json["id"]
    new_name = request.json["name"]

    history = load_history()

    for chat in history:
        if chat["id"] == chat_id:
            chat["user"] = new_name

    save_history(history)

    return jsonify({"status": "renamed"})


# Pin chat
@app.route("/pin_chat", methods=["POST"])
def pin_chat():

    chat_id = request.json["id"]

    history = load_history()

    for chat in history:
        if chat["id"] == chat_id:
            chat["pinned"] = not chat["pinned"]

    save_history(history)

    return jsonify({"status": "pinned"})


# Archive chat
@app.route("/archive_chat", methods=["POST"])
def archive_chat():

    chat_id = request.json["id"]

    history = load_history()

    for chat in history:
        if chat["id"] == chat_id:
            chat["archived"] = True

    save_history(history)

    return jsonify({"status": "archived"})


# Generate share link
@app.route("/share_chat", methods=["POST"])
def share_chat():

    chat_id = request.json["id"]

    link = f"http://127.0.0.1:5000/shared/{chat_id}"

    return jsonify({"link": link})


# View shared chat
@app.route("/shared/<chat_id>")
def shared(chat_id):

    history = load_history()

    for chat in history:
        if chat["id"] == chat_id:
            return jsonify(chat)

    return jsonify({"error": "Chat not found"})


# Run server
if __name__ == "__main__":
    app.run(debug=True)