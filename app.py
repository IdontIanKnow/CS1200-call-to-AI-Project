from flask import Flask, request, jsonify
from flask_cors import CORS
import requests, os

app = Flask(__name__)
CORS(app, origins=["https://idontianknow.github.io"])

API_KEY = os.getenv("SPOONACULAR_KEY")

@app.route("/ask", methods=["POST"])
def ask():
    user_text = request.json.get("text", "")

    url = "https://api.spoonacular.com/food/converse"

    # Use GET parameters — Spoonacular requires GET, not POST
    params = {
        "text": user_text + " (Reply in under 200 words.)",
        "context": "recipe assistance",
        "apiKey": API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        answer = data.get("answer", "No answer returned.")

        # enforce 200-word limit
        words = answer.split()
        if len(words) > 200:
            answer = " ".join(words[:200])

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return "Backend is running!"
