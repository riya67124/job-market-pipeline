from salary_data import load_salary_data

df = load_salary_data()
low = df.sort_values("salary_min").head(10)
print(low[["salary_min", "title", "location", "search_term"]].to_string(index=False))