import os
import sys
import hashlib
import streamlit as st

# --------------------------------------------------
# Ensure project root on PYTHONPATH
# --------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# --------------------------------------------------
# Session state initialization
# --------------------------------------------------
if "vector_db" not in st.session_state:
    st.session_state.vector_db = None

if "indexed_file_hash" not in st.session_state:
    st.session_state.indexed_file_hash = None

# --------------------------------------------------
# Imports
# --------------------------------------------------
from ingestion.loader import load_uploaded_pdf
from ingestion.chunker import chunk_text
from ingestion.embedder import embed_chunks
from ingestion.index_builder import build_vector_index
from embeddings import get_embedding

from core.aspect_extractor import extract_query_aspects
from core.similarity import similarity_matrix
from core.coverage_analyzer import analyze_coverage
from core.noise_detector import detect_noise_chunks
from core.scoring import compute_retrieval_integrity_score

from explainability.explanations import generate_explanation
from explainability.recommendations import generate_recommendations
from visualization.heatmap import create_coverage_heatmap
from visualization.score_meter import create_score_meter


def file_hash(uploaded_file):
    return hashlib.md5(uploaded_file.getvalue()).hexdigest()


# --------------------------------------------------
# UI
# --------------------------------------------------
st.set_page_config(page_title="Retrieval Integrity Auditor", layout="wide")
st.title("Retrieval Integrity Auditor")
st.caption("Auditing the retrieval step of RAG systems (Track 3)")

st.sidebar.header("Knowledge Base")

uploaded_file = st.sidebar.file_uploader(
    "Upload a PDF document",
    type=["pdf"]
)

# --------------------------------------------------
# Ingestion (ONE-TIME per document)
# --------------------------------------------------
if uploaded_file is not None:
    current_hash = file_hash(uploaded_file)

    if st.session_state.indexed_file_hash != current_hash:
        with st.spinner("Indexing document (one-time cost)..."):
            documents = load_uploaded_pdf(uploaded_file)
            full_text = " ".join(doc["text"] for doc in documents)

            chunks = chunk_text(full_text)
            embeddings = embed_chunks(chunks)
            vector_db = build_vector_index(chunks, embeddings)

            st.session_state.vector_db = vector_db
            st.session_state.indexed_file_hash = current_hash

        st.sidebar.success(f"Indexed {len(chunks)} chunks")

# --------------------------------------------------
# Query + Audit
# --------------------------------------------------
query = st.text_input(
    "Enter your query",
    placeholder="Example: What is the efficient market hypothesis?"
)

if st.button("Run Retrieval Audit"):
    if st.session_state.vector_db is None:
        st.error("Please upload a document first.")
        st.stop()

    aspects = extract_query_aspects(query)
    st.subheader("1. Query Aspects")
    st.write(aspects)

    query_embedding = get_embedding(query)
    retrieved_chunks = st.session_state.vector_db.search(query_embedding, top_k=5)

    st.subheader("2. Retrieved Chunks")
    st.write(retrieved_chunks)

    aspect_embeddings = [get_embedding(a["aspect_text"]) for a in aspects]
    chunk_embeddings = [get_embedding(c["text"]) for c in retrieved_chunks]

    sim_matrix = similarity_matrix(aspect_embeddings, chunk_embeddings)

    coverage = analyze_coverage(aspects, sim_matrix, retrieved_chunks)
    noise = detect_noise_chunks(retrieved_chunks, sim_matrix, aspects)
    missing = [c for c in coverage if c["coverage"] == "missing"]

    score, breakdown = compute_retrieval_integrity_score(coverage, noise, missing)

    st.subheader("3. Retrieval Integrity Score")
    st.plotly_chart(create_score_meter(score), use_container_width=True)
    st.write(breakdown)

    st.subheader("4. Coverage Heatmap")
    st.plotly_chart(
        create_coverage_heatmap(aspects, retrieved_chunks, sim_matrix),
        use_container_width=True
    )

    st.subheader("5. Explanation")
    st.write(generate_explanation(coverage, noise, missing))

    st.subheader("6. Recommendations")
    for rec in generate_recommendations(coverage, noise, missing):
        st.markdown(f"- {rec}")
