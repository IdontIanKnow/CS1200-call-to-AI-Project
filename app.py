from flask import Flask, request, jsonify
from flask_cors import CORS
import requests, os

app = Flask(__name__)
CORS(app, origins=["https://idontianknow.github.io"])

API_KEY = os.getenv("SPOONACULAR_KEY")

@app.route("/ask", methods=["POST"])
def ask():
    user_text = request.json.get("text", "")

    url = "https://api.spoonacular.com/recipes/quickAnswer"

    params = {
        "q": user_text + " (Reply in under 200 words.)",
        "apiKey": API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        answer = data.get("answer", None)
        if not answer:
            return jsonify({"error": "No answer returned from Spoonacular"}), 500

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
