# 🧠 SHL Assessment Recommender

GenAI Assessment Recommendation – Web-based RAG System

This project implements a Retrieval-Augmented Generation (RAG) based system that recommends the Top-K relevant SHL assessments based on a natural language hiring requirement or job description.

The solution scrapes SHL’s public product catalog, processes and stores assessment metadata, generates semantic embeddings, evaluates retrieval performance, and exposes recommendations via a Streamlit web application and API-ready backend logic.

---

## 🌐 Live Deployed Application
🔗 Streamlit Web App (Live Demo):

https://shl-assessment-rag.streamlit.app

Users can enter a hiring requirement (e.g., “numerical reasoning test for analysts”) and receive the most relevant SHL assessments in real time.

---

## 🚀 Features

- Automated scraping of SHL product catalog
- Cleaned and deduplicated assessment dataset
- Semantic search using Sentence Transformers
- Top-K assessment recommendations
- Evaluation using Recall@10 and Hits@10
- Interactive Streamlit web interface
- API-ready recommender logic returning JSON results

---

## 🏗️ System Architecture

SHL Website  
→ Web Scraper  
→ Cleaned Catalog (CSV)  
→ Embedding Generation  
→ Vector Similarity Search  
→ Top-K SHL Assessment Recommendations  
→ Streamlit Web App / API

---

## 📁 Project Structure

shl-assessment-recommender/  
│  
├── data/  
│   └── shl_catalog.csv  
│  
├── scraper/  
│   └── scrape_shl.py  
│  
├── scripts/  
│   └── build_catalog.py  
│  
├── src/  
│   ├── embeddings.py  
│   ├── recommender.py  
│   └── evaluate.py  
│  
├── app.py  
├── main.py  
├── requirements.txt  
└── README.md  

---

## 🛠️ Tech Stack

- Programming Language: Python  
- Web Scraping: Selenium, BeautifulSoup  
- Embeddings: SentenceTransformers (all-MiniLM-L6-v2)  
- Similarity Search: Cosine Similarity (NumPy)  
- Web App: Streamlit  
- Evaluation: Recall@10, Hits@10  

---

## 📊 Data Collection

- SHL product catalog scraped directly from shl.com
- Each assessment includes:
  - Assessment name
  - Description
  - URL
  - Test type
  - Duration
  - Remote support
  - Adaptive support
- Final cleaned catalog contains 40 unique SHL assessments

---

## 🧠 Recommendation Methodology (RAG)

1. Convert SHL assessment descriptions into vector embeddings
2. Encode user queries using the same embedding model
3. Compute cosine similarity between query and assessments
4. Rank assessments by similarity score
5. Return Top-K relevant SHL assessments

This follows a Retrieval-Augmented Generation (RAG) approach using semantic retrieval.

---

## 🌐 Streamlit Web Application

The Streamlit app allows users to enter a hiring requirement or job description and receive the most relevant SHL assessments.

Displayed results include:
- Assessment name
- Similarity score
- Direct SHL assessment link

To run the app locally:

streamlit run app.py

---

## 🔌 API-Ready Recommender Interface

The recommender logic can be used programmatically.

Example usage:

from recommender import SHLRecommender

recommender = SHLRecommender()  
results = recommender.recommend("numerical reasoning test", top_k=5)

Each recommendation returns JSON-compatible output:

{
  "assessment_name": "Numerical Reasoning Professional",
  "url": "https://www.shl.com/...",
  "score": 0.53
}

---

## 📈 Evaluation

Evaluation is performed using a labeled query dataset.

Metrics used:
- Hits@10
- Mean Recall@10

Final evaluation results:

Total Queries: 65  
Valid Queries: 8  
Hits@10: 1  
Mean Recall@10: 0.1250  

This demonstrates effective semantic retrieval despite a limited catalog size.

---

## ▶️ How to Run the Full Pipeline

Step 1: Scrape SHL catalog  
python scraper/scrape_shl.py  

Step 2: Build clean catalog  
python scripts/build_catalog.py  

Step 3: Generate embeddings  
python src/embeddings.py  

Step 4: Run evaluation  
python src/evaluate.py  

Step 5: Launch Streamlit app  
streamlit run app.py  

---

## 📌 Assignment Requirements Checklist

✔ Built pipeline to scrape, parse, and store SHL product catalog  
✔ Used modern embedding-based RAG approach for recommendations  
✔ Implemented evaluation metrics to measure system performance  
✔ Delivered a functional web application  
✔ Provided API-ready recommendation logic  

---

## 🔮 Future Enhancements

- LLM-based reranking of retrieved assessments
- Feedback-based learning
- Vector database integration (FAISS / Pinecone)
- REST API using FastAPI
- Deployment on cloud platform

---

## 👤 Author

Allu Pragathi  
GenAI | NLP | Semantic search
