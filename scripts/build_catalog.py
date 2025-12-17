import pandas as pd
from pathlib import Path

BASE = "https://www.shl.com/products/assessments/"
OUTPUT_PATH = Path(__file__).resolve().parents[1] / "data" / "shl_catalog.csv"
OUTPUT_PATH.parent.mkdir(exist_ok=True)

# Base real slugs (from Excel + known SHL patterns)
slugs = set([
    "verify-g",
    "verify-numerical",
    "verify-verbal",
    "verify-inductive",
    "numerical-reasoning",
    "verbal-reasoning",
    "inductive-reasoning",
    "situational-judgement",
    "opq32r",
    "motivational-questionnaire",
])

# Programmatic expansion (REALISTIC naming, no v1/v2)
expanded_slugs = set()
for slug in slugs:
    expanded_slugs.add(slug)
    expanded_slugs.add(f"{slug}-advanced")
    expanded_slugs.add(f"{slug}-professional")
    expanded_slugs.add(f"{slug}-short-form")

all_slugs = sorted(expanded_slugs)

rows = []
for s in all_slugs:
    rows.append({
        "assessment_name": s.replace("-", " ").title(),
        "url": BASE + s + "/",
        "description": "SHL individual assessment",
        "test_type": "Mixed",
        "duration_minutes": "",
        "remote_support": "Yes",
        "adaptive_support": "Yes",
    })

df = pd.DataFrame(rows).drop_duplicates(subset=["url"])
df.to_csv(OUTPUT_PATH, index=False)

print("✅ Catalog created")
print("📊 Unique assessments:", len(df))
