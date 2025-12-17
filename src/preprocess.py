import pandas as pd

INPUT_PATH = "data/shl_catalog.csv"
OUTPUT_PATH = "data/shl_catalog_processed.csv"

def build_text(row):
    return f"""
    Assessment Name: {row['assessment_name']}
    Description: {row['description']}
    Test Type: {row['test_type']}
    """

def main():
    df = pd.read_csv(INPUT_PATH)
    df["combined_text"] = df.apply(build_text, axis=1)
    df.to_csv(OUTPUT_PATH, index=False)

    print("✅ Preprocessing complete")
    print("📊 Rows:", len(df))

if __name__ == "__main__":
    main()
