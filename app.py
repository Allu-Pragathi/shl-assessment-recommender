import streamlit as st
import pandas as pd
from src.recommender import SHLRecommender

@st.cache_resource
def load_recommender():
    return SHLRecommender()

recommender = load_recommender()
# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="SHL Assessment Recommender",
    page_icon="🧠",
    layout="centered"
)

# --------------------------------------------------
# Title & description
# --------------------------------------------------
st.title("🧠 SHL Assessment Recommender")
st.write(
    """
    This tool recommends the **Top-K relevant SHL assessments** based on a hiring requirement.
    It uses **semantic embeddings** to understand intent and match assessments intelligently.
    """
)

# --------------------------------------------------
# Load recommender (cached)
# --------------------------------------------------
@st.cache_resource
def load_recommender():
    return SHLRecommender()

recommender = load_recommender()

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
    TOP_K = st.slider(
        "Top-K recommendations",
        min_value=3,
        max_value=10,
        value=5
    )

with col2:
    min_score = st.slider(
        "Minimum relevance threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.05
    )

test_type_filter = st.multiselect(
    "Filter by assessment type (optional)",
    options=["Personality", "Cognitive", "Knowledge & Skills"]
)

sort_option = st.selectbox(
    "Sort results by",
    ["Relevance (default)", "Assessment Name", "Test Type"]
)

# --------------------------------------------------
# Detect query intent (light AI UX)
# --------------------------------------------------
intent = "General"
q_lower = query.lower()
if any(k in q_lower for k in ["cognitive", "aptitude", "reasoning"]):
    intent = "Cognitive"
elif any(k in q_lower for k in ["personality", "behavior", "behaviour"]):
    intent = "Personality"
elif any(k in q_lower for k in ["coding", "skills", "technical"]):
    intent = "Knowledge & Skills"

if query:
    st.info(f"🔍 Detected query intent: **{intent}**")

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

    # Apply relevance threshold
    results = [r for r in results if r["score"] >= min_score]

    # Apply test type filter
    if test_type_filter:
        results = [r for r in results if r["test_type"] in test_type_filter]

    # Sorting
    if sort_option == "Assessment Name":
        results = sorted(results, key=lambda x: x["assessment_name"])
    elif sort_option == "Test Type":
        results = sorted(results, key=lambda x: x["test_type"])

    st.subheader(f"Top {len(results)} Relevant SHL Assessments")

    if not results:
        st.warning("No assessments match the selected filters.")
    else:
        # Convert to DataFrame for download
        df_results = pd.DataFrame(results)

        for i, r in enumerate(results, start=1):
            search_url = (
                "https://www.shl.com/search/?q="
                + r["assessment_name"].replace(" ", "%20")
            )

            st.markdown(
                f"""
### {i}. {r['assessment_name']}
**Type:** {r['test_type']}  
**Description:** {r['description']}  
🔗 [Search this assessment on SHL]({search_url})
"""
            )

            st.write(f"Relevance Score: `{r['score']:.3f}`")
            st.progress(min(r["score"], 1.0))

            with st.expander("Why this assessment?"):
                st.write(
                    "This assessment was recommended because its semantic meaning "
                    "closely matches the hiring requirement you entered."
                )

            st.divider()

        # Download button
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
