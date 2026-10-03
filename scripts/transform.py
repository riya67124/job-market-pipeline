import glob
import json
from collections import Counter
from clean import clean_text, standardize_location, find_city_in_text
from skills import extract_skills
from dedupe import remove_duplicates

def clean_job(job):
    title = clean_text(job.get("title")) or ""
    description = clean_text(job.get("description")) or ""
    location = standardize_location(job.get("location"))
    if location == "Unspecified":
        location = find_city_in_text(title + " " + description) or "Unspecified"
    return {
        "source": job.get("source"),
        "job_id": job.get("job_id"),
        "title": title,
        "company": clean_text(job.get("company")) or "Unknown",
        "location": location,
        "description": description,
        "salary_min": job.get("salary_min"),
        "salary_max": job.get("salary_max"),
        "posted_date": (job.get("posted_date") or "")[:10] or None,
        "url": job.get("url"),
        "search_term": job.get("search_term"),
        "skills": extract_skills(title + " " + description),
    }

def transform(raw_jobs):
    raw_jobs = [j for j in raw_jobs if j.get("title")]
    unique = remove_duplicates(raw_jobs)
    return [clean_job(j) for j in unique]

if __name__ == "__main__":
    latest = sorted(glob.glob("data/raw/jobs_*.json"))[-1]
    with open(latest, encoding="utf-8") as f:
        raw = json.load(f)

    cleaned = transform(raw)
    print("Raw jobs:", len(raw))
    print("Clean jobs:", len(cleaned))
    print("Jobs with at least 1 skill:", sum(1 for j in cleaned if j["skills"]))
    print("Unknown company:", sum(1 for j in cleaned if j["company"] == "Unknown"))
    print("Unspecified location:", sum(1 for j in cleaned if j["location"] == "Unspecified"))

    counts = Counter(s for j in cleaned for s in j["skills"])
    print("\nTop 10 skills:")
    for skill, n in counts.most_common(10):
        print(" ", skill, "-", n)