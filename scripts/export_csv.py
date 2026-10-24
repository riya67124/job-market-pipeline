import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("READER_USER"),
    password=os.getenv("READER_PASSWORD"),
    sslmode="require",
)

TABLES = {
    "postings": "SELECT id, source, title, company, location, salary_min, salary_max, posted_date, url, search_term, first_seen FROM postings",
    "posting_skills": "SELECT posting_id, skill FROM posting_skills",
    "skill_pairs": "SELECT skill_1, skill_2, pair_count FROM skill_pairs",
    "pipeline_runs": "SELECT * FROM pipeline_runs",
}

os.makedirs("dashboard/data", exist_ok=True)
cur = conn.cursor()
for name, sql in TABLES.items():
    cur.execute(sql)
    cols = [d[0] for d in cur.description]
    df = pd.DataFrame(cur.fetchall(), columns=cols)
    df.to_csv(f"dashboard/data/{name}.csv", index=False, encoding="utf-8")
    print(name, "->", len(df), "rows")
conn.close()