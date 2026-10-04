import os
from dotenv import load_dotenv

load_dotenv()
pw = os.getenv("DB_PASSWORD") or ""

print("User:", os.getenv("DB_USER"))
print("Password length:", len(pw))
print("Has a space inside or around it:", pw != pw.strip() or " " in pw)
print("Has quote marks:", '"' in pw or "'" in pw)