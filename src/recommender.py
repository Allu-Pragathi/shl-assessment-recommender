import os
import pickle
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

DATA_PATH = "data/shl_catalog.csv"
EMBEDDINGS_PATH = "data/embeddings.npy"
METADATA_PATH = "data/metadata.pkl"

class SHLRecommender:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Load catalog
        self.df = pd.read_csv(DATA_PATH)

        # Generate or load embeddings
        if os.path.exists(EMBEDDINGS_PATH) and os.path.exists(METADATA_PATH):
            self.embeddings = np.load(EMBEDDINGS_PATH)
            with open(METADATA_PATH, "rb") as f:
                self.metadata = pickle.load(f)
        else:
            self._build_embeddings()

    def _build_embeddings(self):
        texts = (
            self.df["assessment_name"].fillna("") + " "
            + self.df["description"].fillna("") + " "
            + self.df["test_type"].fillna("")
        ).tolist()

        self.embeddings = self.model.encode(texts, show_progress_bar=False)

        self.metadata = self.df[["assessment_name", "url"]].to_dict(orient="records")

        os.makedirs("data", exist_ok=True)
        np.save(EMBEDDINGS_PATH, self.embeddings)

        with open(METADATA_PATH, "wb") as f:
            pickle.dump(self.metadata, f)

    def recommend(self, query, top_k=5):
        query_embedding = self.model.encode([query])
        scores = cosine_similarity(query_embedding, self.embeddings)[0]

        top_indices = scores.argsort()[::-1][:top_k]

        results = []
        for idx in top_indices:
            results.append({
                "assessment_name": self.metadata[idx]["assessment_name"],
                "url": self.metadata[idx]["url"],
                "score": float(scores[idx])
            })

        return results
