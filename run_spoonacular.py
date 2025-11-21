import os
import requests

api_key = os.getenv("SPOONACULAR_KEY")
if not api_key:
    raise RuntimeError("Missing SPOONACULAR_KEY environment variable")

url = "https://api.spoonacular.com/food/converse"

params = {
    "text": "Give me a pasta recipe in 200 words or less.",
    "context": "recipe assistance",
    "apiKey": api_key,
}

try:
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    print(data.get("answer", data))
except requests.exceptions.RequestException as e:
    print("API request failed:", e)
