from src.recommender import SHLRecommender

def main():
    recommender = SHLRecommender()

    query = "numerical assessment"
    results = recommender.recommend(query, top_k=5)

    print("\nTop-5 Relevant SHL Assessments:\n")
    for i, r in enumerate(results, start=1):
        print(f"{i}. {r['assessment_name']} ({r['score']:.3f})")

if __name__ == "__main__":
    main()
