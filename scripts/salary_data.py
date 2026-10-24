import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def load_salary_data():
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
        SELECT p.id, p.title, p.location, p.search_term, p.salary_min,
               COALESCE(STRING_AGG(ps.skill, '|'), '') AS skills
        FROM postings p
        LEFT JOIN posting_skills ps ON ps.posting_id = p.id
        WHERE p.salary_min >= 100000
        GROUP BY p.id
    """)
    cols = [d[0] for d in cur.description]
    df = pd.DataFrame(cur.fetchall(), columns=cols)
    conn.close()

    df["salary_min"] = df["salary_min"].astype(float)
    df["band"] = pd.qcut(df["salary_min"], 3, labels=["Low", "Mid", "High"])
    return df

if __name__ == "__main__":
    df = load_salary_data()
    print("Rows with a real salary:", len(df))
    print("\nBand cut-offs (annual salary, INR):")
    print(df.groupby("band", observed=True)["salary_min"].agg(["min", "max", "count"]))