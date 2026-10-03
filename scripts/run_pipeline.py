import json
import time
from datetime import datetime
from fetch_all import fetch_all
from transform import transform
from load import get_connection, load_jobs

def log_run(conn, fetched, dupes, new, missing_salary, seconds, status):
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO pipeline_runs
        (jobs_fetched, duplicates_removed, new_jobs_loaded, missing_salary, seconds_taken, status)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (fetched, dupes, new, missing_salary, round(seconds, 2), status),
    )
    conn.commit()

def run():
    start = time.time()
    conn = get_connection()
    try:
        raw = fetch_all()

        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"data/raw/jobs_{stamp}.json", "w", encoding="utf-8") as f:
            json.dump(raw, f, indent=2)

        cleaned = transform(raw)
        new_jobs = load_jobs(cleaned, conn)
        missing = sum(1 for j in cleaned if not j["salary_min"])

        log_run(conn, len(raw), len(raw) - len(cleaned), new_jobs,
                missing, time.time() - start, "success")

        cur = conn.cursor()
        cur.execute("SELECT * FROM pipeline_runs ORDER BY run_id DESC LIMIT 1")
        print("Run logged:", cur.fetchone())
    except Exception as e:
        conn.rollback()
        log_run(conn, 0, 0, 0, 0, time.time() - start, "failed: " + type(e).__name__)
        print("Pipeline failed:", type(e).__name__)
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    run()