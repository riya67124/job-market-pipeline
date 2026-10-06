import os
import pandas as pd
import psycopg2
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def cfg(name):
    try:
        return st.secrets[name]
    except Exception:
        return os.getenv(name)

@st.cache_data(ttl=600)
def run_query(sql, params=None):
    conn = psycopg2.connect(
        host=cfg("DB_HOST"),
        port=cfg("DB_PORT"),
        dbname=cfg("DB_NAME"),
        user=cfg("DB_USER"),
        password=cfg("DB_PASSWORD"),
        sslmode=cfg("DB_SSLMODE") or "require",
    )
    cur = conn.cursor()
    cur.execute(sql, params)
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    conn.close()
    return pd.DataFrame(rows, columns=cols)

st.title("Job Market Intelligence")
st.caption("Data and Business Analyst roles in India, updated daily")

total = run_query("SELECT COUNT(*) AS n FROM postings")["n"][0]
st.metric("Job postings tracked", int(total))

st.subheader("Top skills in demand")
skills = run_query(
    "SELECT skill, COUNT(*) AS postings FROM posting_skills GROUP BY skill ORDER BY 2 DESC LIMIT 10"
)
st.bar_chart(skills, x="skill", y="postings", sort="-postings")

st.subheader("Search jobs")
col1, col2 = st.columns(2)
text = col1.text_input("Job title or company contains")
skill_list = run_query("SELECT DISTINCT skill FROM posting_skills ORDER BY skill")["skill"].tolist()
chosen = col2.multiselect("Must mention these skills", skill_list)

sql = """
    SELECT p.title, p.company, p.location, p.posted_date, p.url
    FROM postings p
    WHERE (p.title ILIKE %s OR p.company ILIKE %s)
"""
params = [f"%{text}%", f"%{text}%"]
for s in chosen:
    sql += " AND EXISTS (SELECT 1 FROM posting_skills ps WHERE ps.posting_id = p.id AND ps.skill = %s)"
    params.append(s)
sql += " ORDER BY p.posted_date DESC NULLS LAST LIMIT 100"

results = run_query(sql, tuple(params))
st.write(f"{len(results)} matching postings (showing up to 100)")
st.dataframe(
    results,
    hide_index=True,
    column_config={"url": st.column_config.LinkColumn("Link")},
)