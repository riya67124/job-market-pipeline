import re
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import (
    RepeatedStratifiedKFold, StratifiedKFold, cross_val_predict, cross_val_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from salary_data import load_salary_data

def seniority(title):
    t = title.lower()
    if re.search(r"\b(senior|sr|lead|manager|head|principal)\b", t):
        return "senior"
    if re.search(r"\b(junior|jr|intern|trainee|fresher)\b", t):
        return "junior"
    return "unspecified"

def split_skills(s):
    return [x for x in s.split("|") if x]

df = load_salary_data()
df["seniority"] = df["title"].apply(seniority)
X = df[["search_term", "location", "seniority", "skills"]]
y = df["band"].astype(str)

pre = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="infrequent_if_exist", min_frequency=3),
     ["search_term", "location", "seniority"]),
    ("skills", CountVectorizer(tokenizer=split_skills, token_pattern=None,
                               lowercase=False, binary=True), "skills"),
])

model = Pipeline([("pre", pre), ("clf", LogisticRegression(max_iter=1000, C=0.5))])
baseline = DummyClassifier(strategy="most_frequent")

cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=42)
acc = cross_val_score(model, X, y, cv=cv, scoring="accuracy")
base = cross_val_score(baseline, X, y, cv=cv, scoring="accuracy")

print("Rows used:", len(df))
print("Band counts:", y.value_counts().to_dict())
print(f"Model accuracy:    {acc.mean():.0%}  (+/- {acc.std():.0%})")
print(f"Plain-guess accuracy: {base.mean():.0%}")

pred = cross_val_predict(model, X, y, cv=StratifiedKFold(5, shuffle=True, random_state=42))
order = ["Low", "Mid", "High"]
rank = {b: i for i, b in enumerate(order)}
within_one = sum(abs(rank[a] - rank[p]) <= 1 for a, p in zip(y, pred)) / len(y)
print(f"Within one band:   {within_one:.0%}")

cm = pd.DataFrame(confusion_matrix(y, pred, labels=order),
                  index=[f"actual {b}" for b in order],
                  columns=[f"predicted {b}" for b in order])
print("\n", cm)