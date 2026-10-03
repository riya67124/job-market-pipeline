from load import get_connection

with open("sql/create_tables.sql", encoding="utf-8") as f:
    sql = f.read()

conn = get_connection()
cur = conn.cursor()
cur.execute(sql)
conn.commit()

cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
print("Tables in job_market:", [r[0] for r in cur.fetchall()])
conn.close()