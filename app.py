from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app, origins=["https://idontianknow.github.io"])

GROQ_KEY = os.getenv("GROQ_API_KEY")

@app.route("/ask", methods=["POST"])
def ask():
    user_text = request.json.get("text", "")

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a helpful cooking assistant. Keep responses under 200 words."},
            {"role": "user", "content": user_text}
        ],
        "max_completion_tokens": 300,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise error for 4xx/5xx
        data = response.json()

        # Extract assistant reply
        answer = data["choices"][0]["message"]["content"]

        return jsonify({"answer": answer})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Groq request failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Backend is running with Groq!"
