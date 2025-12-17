import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

EMBEDDINGS_PATH = Path("data/embeddings.pkl")


class SHLRecommender:
    def __init__(self):
        with open(EMBEDDINGS_PATH, "rb") as f:
            data = pickle.load(f)

        self.embeddings = data["embeddings"]
        self.catalog = data["catalog"]

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def recommend(self, query: str, top_k: int = 5):
        """
        Always returns Top-K relevant SHL assessments
        """
        # Light query expansion (improves generic queries)
        expanded_query = f"{query} assessment test"

        query_embedding = self.model.encode(
            expanded_query,
            normalize_embeddings=True
        )

        # Cosine similarity via dot product (normalized vectors)
        scores = np.dot(self.embeddings, query_embedding)

        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []
        for idx in top_indices:
            item = self.catalog[idx]
            results.append({
                "assessment_name": item["assessment_name"],
                "description": item["description"],
                "test_type": item["test_type"],
                "url": item["url"],
                "score": float(scores[idx])
            })

        return results
