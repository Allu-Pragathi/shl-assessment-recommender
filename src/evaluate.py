import pandas as pd
from recommender import SHLRecommender


DATASET_PATH = "Gen_AI Dataset.xlsx"


def normalize(text: str) -> str:
    return (
        text.lower()
        .strip()
        .replace("-", " ")
        .replace("_", " ")
    )


def extract_slug(url: str) -> str:
    return normalize(url.rstrip("/").split("/")[-1])


def main():
    df = pd.read_excel(DATASET_PATH)
    df.columns = [c.strip().lower() for c in df.columns]
    df = df.rename(columns={"assessment_url": "true_url"})

    recommender = SHLRecommender()

    # Pre-compute catalog slugs
    catalog_slugs = [
        extract_slug(item["url"]) for item in recommender.catalog
    ]

    hits = 0
    valid_queries = 0
    total = len(df)

    for idx, row in df.iterrows():
        query = str(row["query"])
        true_url = str(row["true_url"])

        true_slug = extract_slug(true_url)

        # ✅ VALIDITY CHECK: slug overlap, not URL equality
        if not any(true_slug in cs or cs in true_slug for cs in catalog_slugs):
            continue

        valid_queries += 1

        results = recommender.recommend(query, top_k=10)

        hit = False
        for r in results:
            predicted_slug = extract_slug(r["url"])
            if true_slug in predicted_slug or predicted_slug in true_slug:
                hit = True
                break

        if hit:
            hits += 1

        if (idx + 1) % 10 == 0:
            print(f"Processed {idx + 1}/{total}")

    recall_at_10 = hits / valid_queries if valid_queries > 0 else 0

    print("\n🎯 Evaluation Complete")
    print(f"Total Queries: {total}")
    print(f"Valid Queries: {valid_queries}")
    print(f"Hits@10: {hits}")
    print(f"Mean Recall@10: {recall_at_10:.4f}")


if __name__ == "__main__":
    main()
