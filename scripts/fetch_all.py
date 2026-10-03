import json
from datetime import datetime
from fetch_adzuna import fetch_adzuna
from fetch_jooble import fetch_jooble

SEARCH_TERMS = ["data analyst", "business analyst"]

def fetch_all():
    all_jobs = []
    for term in SEARCH_TERMS:
        batch = fetch_adzuna(term, pages=1) + fetch_jooble(term, pages=1)
        for job in batch:
            job["search_term"] = term
            job.setdefault("salary_text", None)
        all_jobs += batch
    return all_jobs

if __name__ == "__main__":
    jobs = fetch_all()
    print("Total jobs fetched:", len(jobs))

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"data/raw/jobs_{stamp}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2)
    print("Saved raw backup to", path)