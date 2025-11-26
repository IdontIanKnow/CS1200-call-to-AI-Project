from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app, origins=["https://idontianknow.github.io"])

GROQ_KEY = os.getenv("GROQ_API_KEY")

BASE_URL = "https://api.groq.com/openai/v1"


# ------------------------------------------------------
# 🚀 Diagnostic endpoint — shows exactly which models YOU have
# ------------------------------------------------------
@app.route("/models")
def list_models():
    headers = {"Authorization": f"Bearer {GROQ_KEY}"}
    r = requests.get(f"{BASE_URL}/models", headers=headers)
    return r.json()


# ------------------------------------------------------
# 🚀 Chat endpoint
# ------------------------------------------------------
@app.route("/ask", methods=["POST"])
def ask():
    user_text = request.json.get("text", "")

    # 1. get list of available models
    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json"
    }

    models_res = requests.get(f"{BASE_URL}/models", headers=headers)

    if models_res.status_code != 200:
        return jsonify({"error": "Failed to fetch models", "details": models_res.text}), 500

    models = models_res.json().get("data", [])
    if not models:
        return jsonify({"error": "No models available on your Groq account"}), 500

    # pick the first available (safe)
    selected_model = models[0]["id"]

    # 2. call Groq with the working model
    payload = {
        "model": selected_model,
        "messages": [
            {"role": "system", "content": "You are a helpful cooking assistant. Keep responses under 200 words."},
            {"role": "user", "content": user_text}
        ],
        "max_tokens": 300
    }

    try:
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            headers=headers,
            json=payload
        )

        if response.status_code != 200:
            return jsonify({
                "error": "Groq request failed",
                "details": response.text
            }), 500

        data = response.json()
        answer = data["choices"][0]["message"]["content"]

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return "Backend is running with Groq!"
