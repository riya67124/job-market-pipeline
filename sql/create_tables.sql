CREATE TABLE IF NOT EXISTS postings (
    id SERIAL PRIMARY KEY,
    dedupe_key TEXT UNIQUE NOT NULL,
    source VARCHAR(20),
    job_id VARCHAR(60),
    title TEXT NOT NULL,
    company TEXT,
    location TEXT,
    description TEXT,
    salary_min NUMERIC,
    salary_max NUMERIC,
    posted_date DATE,
    url TEXT,
    search_term TEXT,
    first_seen TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS posting_skills (
    posting_id INT REFERENCES postings(id) ON DELETE CASCADE,
    skill TEXT NOT NULL,
    PRIMARY KEY (posting_id, skill)
);

CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id SERIAL PRIMARY KEY,
    run_time TIMESTAMP DEFAULT NOW(),
    jobs_fetched INT,
    duplicates_removed INT,
    new_jobs_loaded INT,
    missing_salary INT,
    seconds_taken NUMERIC,
    status TEXT
);