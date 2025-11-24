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

    # DEBUG: log full response
    print("Spoonacular raw response:", data)

    answer = data.get("answer", None)
    if not answer:
        answer = "No answer field in response."

    words = answer.split() if answer else []
    if len(words) > 200:
        answer = " ".join(words[:200])

    return jsonify({"answer": answer, "raw": data})

except Exception as e:
    return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return "Backend is running!"
