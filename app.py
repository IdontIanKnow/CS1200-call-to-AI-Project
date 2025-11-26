from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app, origins=["https://idontianknow.github.io"])  # Your front-end URL

# Load Groq API key from environment variable
GROQ_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_KEY:
    raise RuntimeError("Missing GROQ_API_KEY environment variable")

@app.route("/ask", methods=["POST"])
def ask():
    user_text = request.json.get("text", "")

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json"
    }

    # Use a free, supported chat model
    payload = {
        "model": "llama3.1-8b-instant",  # Works for all free accounts
        "messages": [
            {"role": "system", "content": "You are a helpful cooking assistant. Keep responses under 200 words."},
            {"role": "user", "content": user_text}
        ],
        "max_tokens": 300
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        # Extract the AI's reply
        answer = data["choices"][0]["message"]["content"]

        # Enforce 200-word limit just in case
        words = answer.split()
        if len(words) > 200:
            answer = " ".join(words[:200])

        return jsonify({"answer": answer})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Groq request failed: {e}"}), 500
    except KeyError:
        return jsonify({"error": f"Unexpected response structure: {data}"}), 500

@app.route("/")
def home():
    return "Backend is running with Groq!"

if __name__ == "__main__":
    app.run(debug=True)
