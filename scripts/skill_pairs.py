from load import get_connection

with open("sql/skill_pairs.sql", encoding="utf-8") as f:
    query = f.read()

conn = get_connection()
cur = conn.cursor()
cur.execute(query)
rows = cur.fetchall()
conn.close()

print("Total skill pairs found:", len(rows))
print("\nTop 10 pairs:")
for skill_1, skill_2, count in rows[:10]:
    print(f"  {skill_1} + {skill_2}: {count}")