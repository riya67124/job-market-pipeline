import glob
import json
from clean import standardize_location

def make_key(job):
    title = (job.get("title") or "").lower().strip()
    company = (job.get("company") or "").lower().strip()
    city = standardize_location(job.get("location")).lower()
    return f"{title}|{company}|{city}"

def remove_duplicates(jobs):
    seen = set()
    unique = []
    for job in jobs:
        key = make_key(job)
        if key not in seen:
            seen.add(key)
            unique.append(job)
    return unique

if __name__ == "__main__":
    latest = sorted(glob.glob("data/raw/jobs_*.json"))[-1]
    print("Reading:", latest)
    with open(latest, encoding="utf-8") as f:
        jobs = json.load(f)

    unique = remove_duplicates(jobs)
    print("Before:", len(jobs))
    print("After:", len(unique))
    print("Duplicates removed:", len(jobs) - len(unique))