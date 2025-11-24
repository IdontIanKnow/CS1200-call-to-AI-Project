from flask import Flask, request, jsonify
from flask_cors import CORS
import requests, os

app = Flask(__name__)
CORS(app, origins=["https://idontianknow.github.io"])  # Your frontend URL

# Get your Spoonacular API key from Render
API_KEY = os.getenv("SPOONACULAR_KEY")

if not API_KEY:
    raise RuntimeError("Missing SPOONACULAR_KEY environment variable!")

@app.route("/ask", methods=["POST"])
def ask():
    user_text = request.json.get("text", "").strip()
    if not user_text:
        return jsonify({"error": "No text provided"}), 400

    # Correct endpoint for generating recipe answers
    url = "https://api.spoonacular.com/recipes/quickAnswer"

    params = {
        "question": user_text,
        "includeNutrition": False,
        "apiKey": API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Spoonacular returns 'answer' in the JSON
        answer = data.get("answer", "No answer returned.")

        # Enforce 200-word limit
        words = answer.split()
        if len(words) > 200:
            answer = " ".join(words[:200])

        return jsonify({"answer": answer})

    except requests.exceptions.HTTPError as e:
        return jsonify({"error": f"HTTP error: {e}"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return "Backend is running!"
