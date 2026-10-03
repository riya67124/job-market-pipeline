import os
import requests
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("JOOBLE_KEY")
url = f"https://jooble.org/api/{key}"
payload = {"keywords": "data analyst", "location": "India"}

response = requests.post(url, json=payload)
print("Status:", response.status_code)

data = response.json()
print("Total jobs:", data.get("totalCount"))
for job in data["jobs"][:5]:
    print(job["title"], "|", job["company"], "|", job["location"])