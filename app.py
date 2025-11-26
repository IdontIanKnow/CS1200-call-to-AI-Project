from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai

app = Flask(__name__)
CORS(app, origins=["https://idontianknow.github.io"])

# Make sure you set your OpenAI API key in Render as OPENAI_API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/ask", methods=["POST"])
def ask():
    user_text = request.json.get("text", "")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Free-tier, fast, reliable
            messages=[
                {"role": "system", "content": "You are a helpful cooking assistant. Keep responses under 200 words."},
                {"role": "user", "content": user_text}
            ],
            max_tokens=300,
            temperature=0.7
        )

        answer = response['choices'][0]['message']['content']
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Backend is running with OpenAI!"
