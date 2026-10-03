import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

def fetch_adzuna(search_term, pages=1):
    jobs = []
    for page in range(1, pages + 1):
        url = f"https://api.adzuna.com/v1/api/jobs/in/search/{page}"
        params = {
            "app_id": os.getenv("ADZUNA_APP_ID"),
            "app_key": os.getenv("ADZUNA_APP_KEY"),
            "what": search_term,
            "results_per_page": 50,
            "content-type": "application/json",
        }
        for attempt in range(3):
            response = requests.get(url, params=params)
            if response.status_code == 200:
                break
            print("Adzuna error", response.status_code, "- retrying in 10s")
            time.sleep(10)
        response.raise_for_status()
 
        for job in response.json()["results"]:
            jobs.append({
                "source": "adzuna",
                "job_id": str(job.get("id")),
                "title": job.get("title"),
                "company": job.get("company", {}).get("display_name"),
                "location": job.get("location", {}).get("display_name"),
                "description": job.get("description"),
                "salary_min": job.get("salary_min"),
                "salary_max": job.get("salary_max"),
                "posted_date": job.get("created"),
                "url": job.get("redirect_url"),
            })
        time.sleep(1)
    return jobs

if __name__ == "__main__":
    result = fetch_adzuna("data analyst", pages=1)
    print("Jobs fetched:", len(result))
    with_salary = [j for j in result if j["salary_min"]]
    print("Jobs with salary:", len(with_salary), "out of", len(result))
    print(result[0])