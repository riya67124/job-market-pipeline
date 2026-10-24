# Job Market Intelligence Pipeline

An automated pipeline that tracks Data Analyst and Business Analyst job postings in India and turns them into skill-demand insights. It runs every day in the cloud with no manual work.

**Live app:** https://job-market-pipeline-n4qyxxqdzzfsbtk5cckztg.streamlit.app/

## What it does

- Pulls job postings daily from two sources (Adzuna API and Jooble API)
- Cleans the text, removes duplicates, standardizes city names and detects skills (SQL, Python, Power BI and more)
- Stores everything in a PostgreSQL database
- Shows skill demand and a searchable job list in a public Streamlit app
- Emails a weekly summary of top skills and hiring cities
- Builds a skill co-occurrence network showing which skills appear together

## Architecture

    Adzuna API + Jooble API
            |
    Python: fetch -> normalize -> clean -> dedupe -> skill extraction
            |
    Supabase PostgreSQL (postings, posting_skills, pipeline_runs)
            |
    +-------+----------------+------------------+
    |                        |                  |
    Streamlit app      Weekly email digest   Skill network (networkx) + Power BI

GitHub Actions runs the pipeline daily (8:00 AM IST) and the email digest every Monday.

## Tech stack

Python, pandas, requests, psycopg2, networkx, matplotlib, PostgreSQL (Supabase), GitHub Actions, Streamlit, Power BI

## Design decisions

- **Two job sources** so one API outage or gap does not stop the pipeline.
- **GitHub Actions** for scheduling: free, runs without my laptop, and keeps the pipeline code and schedule together.
- **Duplicate protection** on title + company + city, so repeated daily pulls never create duplicate rows.
- **Run log table** (`pipeline_runs`) records every run: jobs fetched, duplicates removed, new jobs loaded, time taken and status.
- **Read-only database login** for the public app, so the public link can never change or delete data.
- **Secrets in GitHub Secrets**, never in the code.

## Skill co-occurrence network

![Skill network](docs/skill_network.png)

## Known limitations

- Both APIs return only a short snippet of each job description, so skill detection misses skills mentioned later in the full posting. Real skill percentages are higher than shown.
- Most Indian postings have no salary field, so salary analysis is limited.
- Location is sometimes only "India" in the source data, so those jobs are marked Unspecified.

## Project structure

    scripts/    fetch, clean, dedupe, load, digest and analysis scripts
    sql/        table definitions and views
    docs/       skill network image
    app.py      Streamlit app
    .github/    GitHub Actions workflows (daily pipeline, weekly digest)

## Author

Riya Vaishya