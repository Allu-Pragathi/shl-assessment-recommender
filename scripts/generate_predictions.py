import sys
import os

# Add project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from src.recommender import SHLRecommender

OUTPUT_FILE = "allu_pragathi.csv"
TEST_DATASET_PATH = "Gen_AI Dataset.xlsx"
TOP_K = 1

def main():
    df = pd.read_excel(TEST_DATASET_PATH)
    df.columns = [c.strip().lower() for c in df.columns]

    if "query" not in df.columns:
        raise ValueError("Test dataset must contain a 'query' column")

    recommender = SHLRecommender()
    predictions = []

    for query in df["query"].dropna():
        results = recommender.recommend(query, top_k=TOP_K)
        url = results[0]["url"] if results else ""

        predictions.append({
            "query": query,
            "recommended_assessment_url": url
        })

    pd.DataFrame(predictions).to_csv(OUTPUT_FILE, index=False)

    print(f"✅ Predictions saved to {OUTPUT_FILE}")
    print(f"📊 Total predictions: {len(predictions)}")

if __name__ == "__main__":
    main()
