import os
import requests

api_key = os.getenv("SPOONACULAR_KEY")
if not api_key:
    raise RuntimeError("Missing SPOONACULAR_KEY environment variable")

url = "https://api.spoonacular.com/food/converse"

payload = {
    "text": "Give me a pasta recipe in 200 words or less.",
    "context": "recipe assistance"
}

params = {"apiKey": api_key}

try:
    response = requests.post(url, json=payload, params=params)
    response.raise_for_status()
    data = response.json()
    print(data.get("answer", data))  # fallback to full data if "answer" is missing
except requests.exceptions.RequestException as e:
    print("API request failed:", e)
