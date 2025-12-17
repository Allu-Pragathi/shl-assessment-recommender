import pandas as pd

df = pd.read_excel("Gen_AI Dataset.xlsx")

df = df.rename(columns={
    "Assessment Name": "assessment_name",
    "Assessment URL": "url",
    "Test Type": "test_type",
    "Description": "description"
})

df = df.dropna(subset=["assessment_name", "url"])
df = df.drop_duplicates(subset=["url"])

df["duration_minutes"] = df.get("duration_minutes", "")
df["remote_support"] = "Yes"
df["adaptive_support"] = "Yes"

df.to_csv("data/shl_catalog.csv", index=False)

print("Catalog size:", len(df))
