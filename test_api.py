import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OMDB_API_KEY")
print("Key loaded:", bool(api_key))
print("Key length:", len(api_key) if api_key else 0)
url = "https://www.omdbapi.com/"

params = {
    "apikey": api_key,
    "t": "Titanic",
    "y": "1997"
}

response = requests.get(url, params=params)

data = response.json()

print("API Status:", data.get("Response"))
print("Movie:", data.get("Title"))
print("Director:", data.get("Director"))
print("API Error:", data.get("Error"))