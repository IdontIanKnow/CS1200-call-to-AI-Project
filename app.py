from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai

app = Flask(__name__)
CORS(app, origins=["https://idontianknow.github.io"])

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/ask", methods=["POST"])
def ask():
    user_text = request.json.get("text", "")

    prompt = (
        f"You are a helpful cooking assistant. Generate a recipe based on the following request, "
        f"keeping the response under 200 words:\n\n{user_text}"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful cooking assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600
        )

        answer = response.choices[0].message.content.strip()
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Backend is running with OpenAI!"
