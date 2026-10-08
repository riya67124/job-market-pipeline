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

cur.execute("SELECT COUNT(*) FROM postings")
print("Can read postings:", cur.fetchone()[0])

try:
    cur.execute("UPDATE postings SET title = title WHERE id = -1")
    print("PROBLEM: this login can write")
except Exception as e:
    print("Write blocked (good):", type(e).__name__)

conn.rollback()
conn.close()