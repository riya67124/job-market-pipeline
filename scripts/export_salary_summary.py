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
cur = conn.cursor()
cur.execute("""
    SELECT 'Role: ' || search_term AS grp,
           COUNT(*) AS n,
           CAST(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary_min) AS INT) AS median_salary
    FROM postings
    WHERE salary_min >= 100000
    GROUP BY search_term
    UNION ALL
    SELECT 'City: ' || location,
           COUNT(*),
           CAST(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary_min) AS INT)
    FROM postings
    WHERE salary_min >= 100000 AND location <> 'Unspecified'
    GROUP BY location
    HAVING COUNT(*) >= 5
    ORDER BY median_salary DESC
""")
cols = [d[0] for d in cur.description]
df = pd.DataFrame(cur.fetchall(), columns=cols)
conn.close()

os.makedirs("dashboard/data", exist_ok=True)
df.to_csv("dashboard/data/salary_summary.csv", index=False, encoding="utf-8")
print(df.to_string(index=False))