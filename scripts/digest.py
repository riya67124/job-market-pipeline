from load import get_connection

def build_digest():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM postings WHERE first_seen >= NOW() - INTERVAL '7 days'")
    total = cur.fetchone()[0]

    cur.execute("""
        SELECT ps.skill, COUNT(*)
        FROM posting_skills ps
        JOIN postings p ON p.id = ps.posting_id
        WHERE p.first_seen >= NOW() - INTERVAL '7 days'
        GROUP BY ps.skill
        ORDER BY 2 DESC
        LIMIT 5
    """)
    skills = cur.fetchall()

    cur.execute("""
        SELECT location, COUNT(*)
        FROM postings
        WHERE first_seen >= NOW() - INTERVAL '7 days'
          AND location <> 'Unspecified'
        GROUP BY location
        ORDER BY 2 DESC
        LIMIT 3
    """)
    cities = cur.fetchall()
    conn.close()

    lines = [f"New job postings this week: {total}", "", "Top skills in demand:"]
    for skill, n in skills:
        pct = round(100 * n / total) if total else 0
        lines.append(f"  - {skill}: {n} postings ({pct}%)")
    lines += ["", "Top hiring cities:"]
    for city, n in cities:
        lines.append(f"  - {city}: {n} postings")
    lines += ["", "Note: skills are detected from short job snippets, so real percentages are higher."]

    return "Weekly Job Market Digest", "\n".join(lines)

if __name__ == "__main__":
    subject, body = build_digest()
    print(subject)
    print()
    print(body)