import pandas as pd
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from pathlib import Path

DATA_PATH = Path("data/shl_catalog.csv")
OUTPUT_PATH = Path("data/embeddings.pkl")

def main():
    print("🔄 Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    df = pd.read_csv(DATA_PATH)

    texts = []
    for _, row in df.iterrows():
        text = f"""
        Assessment Name: {row['assessment_name']}
        Description: {row['description']}
        Test Type: {row['test_type']}
        Duration: {row['duration_minutes']} minutes
        Remote Support: {row['remote_support']}
        Adaptive Support: {row['adaptive_support']}
        """
        texts.append(text.strip())

    print("🔄 Generating embeddings...")
    embeddings = model.encode(
        texts,
        batch_size=16,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "wb") as f:
        pickle.dump(
            {
                "embeddings": embeddings,
                "catalog": df.to_dict(orient="records")
            },
            f
        )

    print("✅ Embeddings generated")
    print(f"📐 Shape: {embeddings.shape}")

if __name__ == "__main__":
    main()
