import os
from collections import Counter
import requests
from dotenv import load_dotenv

load_dotenv()

url = "https://api.adzuna.com/v1/api/jobs/in/search/1"
params = {
    "app_id": os.getenv("ADZUNA_APP_ID"),
    "app_key": os.getenv("ADZUNA_APP_KEY"),
    "what": "data analyst",
    "results_per_page": 50,
    "content-type": "application/json",
}
r = requests.get(url, params=params)
r.raise_for_status()
jobs = r.json()["results"]

with_salary = [j for j in jobs if j.get("salary_min")]
print("Jobs fetched:", len(jobs))
print("With a salary:", len(with_salary))
print("salary_is_predicted values:", Counter(str(j.get("salary_is_predicted")) for j in with_salary))