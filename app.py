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
    params = {
        "text": user_text,
        "context": "recipe assistance",
        "apiKey": API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return jsonify({"answer": data.get("answer", "No answer returned.")})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Backend is running!"
