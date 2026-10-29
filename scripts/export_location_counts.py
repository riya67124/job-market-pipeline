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
cur.execute(
    "SELECT location, COUNT(*) AS postings FROM postings "
    "WHERE location <> 'Unspecified' "
    "GROUP BY location ORDER BY postings DESC LIMIT 10"
)
cols = [d[0] for d in cur.description]
df = pd.DataFrame(cur.fetchall(), columns=cols)
conn.close()

os.makedirs("dashboard/data", exist_ok=True)
df.to_csv("dashboard/data/location_counts.csv", index=False, encoding="utf-8")
print(df.to_string(index=False))