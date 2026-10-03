import os
import glob
import json
import psycopg2
from dotenv import load_dotenv
from transform import transform
from dedupe import make_key

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        sslmode=os.getenv("DB_SSLMODE", "prefer"),
    )

def load_jobs(cleaned, conn):
    new_count = 0
    cur = conn.cursor()
    for job in cleaned:
        cur.execute(
            """
            INSERT INTO postings
            (dedupe_key, source, job_id, title, company, location, description,
             salary_min, salary_max, posted_date, url, search_term)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (dedupe_key) DO NOTHING
            RETURNING id
            """,
            (make_key(job), job["source"], job["job_id"], job["title"],
             job["company"], job["location"], job["description"],
             job["salary_min"], job["salary_max"], job["posted_date"],
             job["url"], job["search_term"]),
        )
        row = cur.fetchone()
        if row:
            new_count += 1
            for skill in job["skills"]:
                cur.execute(
                    "INSERT INTO posting_skills (posting_id, skill) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                    (row[0], skill),
                )
    conn.commit()
    return new_count

if __name__ == "__main__":
    latest = sorted(glob.glob("data/raw/jobs_*.json"))[-1]
    with open(latest, encoding="utf-8") as f:
        raw = json.load(f)

    cleaned = transform(raw)
    conn = get_connection()
    new_jobs = load_jobs(cleaned, conn)
    print("Clean jobs:", len(cleaned))
    print("New jobs loaded:", new_jobs)

    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM postings")
    print("Total rows in postings:", cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM posting_skills")
    print("Total rows in posting_skills:", cur.fetchone()[0])
    conn.close()