import sys
from load import get_connection

with open(sys.argv[1], encoding="utf-8") as f:
    sql = f.read()

conn = get_connection()
cur = conn.cursor()
cur.execute(sql)
conn.commit()
conn.close()
print("Ran:", sys.argv[1])
