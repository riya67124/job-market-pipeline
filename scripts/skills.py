import re

SKILLS = {
    "Python": ["python"],
    "SQL": ["sql"],
    "Excel": ["excel", "advanced excel", "ms excel"],
    "Power BI": ["power bi", "powerbi"],
    "Tableau": ["tableau"],
    "R": ["r programming", "rstudio"],
    "Java": ["java"],
    "JavaScript": ["javascript"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "Machine Learning": ["machine learning"],
    "Deep Learning": ["deep learning"],
    "Statistics": ["statistics", "statistical"],
    "Data Visualization": ["data visualization", "data visualisation"],
    "ETL": ["etl"],
    "Data Warehousing": ["data warehouse", "data warehousing"],
    "MySQL": ["mysql"],
    "PostgreSQL": ["postgresql", "postgres"],
    "MongoDB": ["mongodb"],
    "Oracle": ["oracle"],
    "SQL Server": ["sql server", "mssql"],
    "Snowflake": ["snowflake"],
    "BigQuery": ["bigquery"],
    "AWS": ["aws"],
    "Azure": ["azure"],
    "GCP": ["gcp", "google cloud"],
    "Spark": ["spark", "pyspark"],
    "Hadoop": ["hadoop"],
    "Airflow": ["airflow"],
    "Git": ["git", "github"],
    "Looker": ["looker"],
    "SAS": ["sas"],
    "SPSS": ["spss"],
    "DAX": ["dax"],
    "Power Query": ["power query"],
    "VBA": ["vba"],
    "Google Sheets": ["google sheets"],
    "Google Analytics": ["google analytics"],
    "A/B Testing": ["a/b testing", "ab testing"],
    "Data Modeling": ["data modeling", "data modelling"],
    "Data Cleaning": ["data cleaning", "data wrangling"],
    "Communication": ["communication"],
    "Stakeholder Management": ["stakeholder"],
    "Problem Solving": ["problem solving", "problem-solving"],
    "Jira": ["jira"],
}

def extract_skills(text):
    if not text:
        return []
    text = text.lower()
    found = []
    for skill, variants in SKILLS.items():
        for v in variants:
            pattern = r"(?<![a-z0-9])" + re.escape(v) + r"(?![a-z0-9])"
            if re.search(pattern, text):
                found.append(skill)
                break
    return found

if __name__ == "__main__":
    sample = "We need Python, SQL and Power BI. Knowledge of Tableau and MySQL is a plus."
    print(extract_skills(sample))