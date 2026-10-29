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
    SELECT CASE
             WHEN salary_min < 300000 THEN '1. Under 3 LPA'
             WHEN salary_min < 600000 THEN '2. 3 to 6 LPA'
             WHEN salary_min < 1000000 THEN '3. 6 to 10 LPA'
             ELSE '4. 10 LPA and above'
           END AS salary_range,
           COUNT(*) AS postings
    FROM postings
    WHERE salary_min >= 100000
    GROUP BY 1
    ORDER BY 1
""")
cols = [d[0] for d in cur.description]
df = pd.DataFrame(cur.fetchall(), columns=cols)
conn.close()

os.makedirs("dashboard/data", exist_ok=True)
df.to_csv("dashboard/data/salary_buckets.csv", index=False, encoding="utf-8")
print(df.to_string(index=False))