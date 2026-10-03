import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

def fetch_jooble(search_term, pages=1):
    jobs = []
    key = os.getenv("JOOBLE_KEY")
    url = f"https://jooble.org/api/{key}"

    for page in range(1, pages + 1):
        payload = {"keywords": search_term, "location": "India", "page": page}

        for attempt in range(3):
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                break
            print("Jooble error", response.status_code, "- retrying in 10s")
            time.sleep(10)
        response.raise_for_status()

        for job in response.json().get("jobs", []):
            jobs.append({
                "source": "jooble",
                "job_id": str(job.get("id")),
                "title": job.get("title"),
                "company": job.get("company"),
                "location": job.get("location"),
                "description": job.get("snippet"),
                "salary_min": None,
                "salary_max": None,
                "salary_text": job.get("salary"),
                "posted_date": job.get("updated"),
                "url": job.get("link"),
            })
        time.sleep(1)
    return jobs

if __name__ == "__main__":
    result = fetch_jooble("data analyst", pages=1)
    print("Jobs fetched:", len(result))
    with_salary = [j for j in result if j["salary_text"]]
    print("Jobs with salary text:", len(with_salary), "out of", len(result))
    print(result[0])