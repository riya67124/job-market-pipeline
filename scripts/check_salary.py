import os
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
    SELECT
        COUNT(*),
        COUNT(salary_min),
        MIN(salary_min),
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary_min),
        MAX(salary_min)
    FROM postings
""")
total, with_salary, low, median, high = cur.fetchone()
conn.close()

print("Total postings:", total)
print("Postings with salary:", with_salary)
print("Salary range (min / median / max):", low, "/", median, "/", high)