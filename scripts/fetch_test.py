import os
import requests
from dotenv import load_dotenv

load_dotenv()

url = "https://api.adzuna.com/v1/api/jobs/in/search/1"
params = {
    "app_id": os.getenv("ADZUNA_APP_ID"),
    "app_key": os.getenv("ADZUNA_APP_KEY"),
    "what": "data analyst",
    "results_per_page": 5,
    "content-type": "application/json",
}

response = requests.get(url, params=params)
print("Status:", response.status_code)

data = response.json()
for job in data["results"]:
    print(job["title"], "|", job["company"]["display_name"], "|", job["location"]["display_name"])
import json
with open("data/raw/adzuna_test.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
print("Saved raw data")