import streamlit as st
import pandas as pd
from src.recommender import SHLRecommender

# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="SHL Assessment Recommender",
    page_icon="🧠",
    layout="centered"
)

# --------------------------------------------------
# Load recommender (cached)
# --------------------------------------------------
@st.cache_resource
def load_recommender():
    return SHLRecommender()

recommender = load_recommender()

# --------------------------------------------------
# Title & description
# --------------------------------------------------
st.title("🧠 SHL Assessment Recommender")
st.write(
    """
    This tool recommends the **Top-K relevant SHL assessments** based on a hiring requirement
    or job description using **semantic search (RAG)**.
    """
)

# --------------------------------------------------
# Example queries
# --------------------------------------------------
st.subheader("Example queries")

examples = [
    "numerical reasoning test",
    "cognitive ability assessment",
    "coding test for developers",
    "personality assessment for managers"
]

cols = st.columns(len(examples))
selected_example = None
for col, ex in zip(cols, examples):
    if col.button(ex):
        selected_example = ex

# --------------------------------------------------
# User input
# --------------------------------------------------
query = st.text_input(
    "Enter your hiring requirement",
    value=selected_example if selected_example else "",
    placeholder="e.g. numerical reasoning test for analysts"
)

# --------------------------------------------------
# Controls
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    TOP_K = st.slider("Top-K recommendations", 3, 10, 5)

with col2:
    min_score = st.slider("Minimum relevance threshold", 0.0, 1.0, 0.0, 0.05)

# --------------------------------------------------
# Session history
# --------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# --------------------------------------------------
# Recommendation logic
# --------------------------------------------------
if query.strip():
    st.session_state.history.append(query)

    with st.spinner("Finding Top-K relevant SHL assessments..."):
        results = recommender.recommend(query, top_k=TOP_K)

    # Apply score threshold safely
    results = [r for r in results if r.get("score", 0) >= min_score]

    st.subheader(f"Top {len(results)} Relevant SHL Assessments")

    if not results:
        st.warning("No assessments matched your query.")
    else:
        df_results = pd.DataFrame(results)

        for i, r in enumerate(results, start=1):
            assessment_name = r.get("assessment_name", "Unknown Assessment")
            score = r.get("score", 0.0)
            url = r.get("url", "")

            search_url = (
                "https://www.shl.com/search/?q="
                + assessment_name.replace(" ", "%20")
            )

            st.markdown(f"### {i}. {assessment_name}")
            st.write(f"**Relevance Score:** `{score:.3f}`")
            st.progress(min(score, 1.0))

            if url:
                st.markdown(f"🔗 [Search this assessment on SHL]({search_url})")

            with st.expander("Why this assessment?"):
                st.write(
                    "This assessment was recommended because its semantic meaning "
                    "closely matches the hiring requirement you entered."
                )

            st.divider()

        # Download results
        st.download_button(
            "⬇️ Download results as CSV",
            df_results.to_csv(index=False),
            file_name="shl_assessment_recommendations.csv",
            mime="text/csv"
        )

else:
    st.warning("Please enter a hiring requirement to get recommendations.")

# --------------------------------------------------
# Sidebar: Search history
# --------------------------------------------------
st.sidebar.subheader("Recent Searches")
if st.session_state.history:
    for q in st.session_state.history[-5:][::-1]:
        st.sidebar.write(f"• {q}")
else:
    st.sidebar.write("No searches yet.")
