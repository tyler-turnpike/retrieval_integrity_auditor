Below is a **clean, submission-ready `README.md`** you can directly copy into your project root.
It is written for **hackathon judges + technical reviewers**, aligned strictly with **Track-3**.

---

# Retrieval Integrity Auditor for RAG Systems (Track 3)

## Overview

This project implements a **Retrieval Integrity Auditor** that evaluates the **retrieval step** of a Retrieval-Augmented Generation (RAG) pipeline.
Instead of generating answers, the system **audits whether retrieved documents sufficiently support a user query**, identifies gaps, detects noise, and provides clear, explainable feedback.

The system is designed to be **explainable to non-technical reviewers**, fast enough for live demos, and fully aligned with the Track-3 problem statement.

---

## Key Idea

> *Bad RAG answers are often caused by poor retrieval, not poor generation.*

This tool answers:

* Are the retrieved documents relevant to the query?
* Which parts of the query are supported or missing?
* Which retrieved chunks are noise?
* How can retrieval be improved?

---

## Features

* **Query Aspect Decomposition**
  Breaks a user query into concrete, retrievable aspects.

* **Retrieval Coverage Analysis**
  Evaluates whether each query aspect is:

  * Supported
  * Partially supported
  * Missing

* **Chunk Classification**
  Classifies retrieved chunks as:

  * Supporting
  * Partial
  * Noise

* **Missing Evidence Detection**
  Identifies critical query aspects that lack sufficient evidence.

* **Retrieval Integrity Score (0–100)**
  A diagnostic score reflecting coverage quality, noise, and missing evidence.

* **Explainability Layer**
  Human-readable explanations describing *why* retrieval is sufficient or insufficient.

* **Actionable Recommendations**
  Suggests concrete improvements such as:

  * Query reformulation
  * Increasing retrieval depth
  * Hybrid retrieval (BM25 + embeddings)
  * Re-ranking strategies

* **Mandatory Visualization**
  Aspect × Chunk coverage heatmap highlighting supported and missing areas.

---

## System Architecture (High Level)

```
User Query
    │
    ├─ Query Aspect Extraction
    │
Uploaded Document (PDF)
    │
    ├─ Text Extraction
    ├─ Chunking
    ├─ Embedding (batched)
    ├─ Vector Index (in-memory)
    │
    ├─ Retrieval (Top-K chunks)
    │
    ├─ Similarity Matrix
    │
    ├─ Coverage + Noise Analysis
    │
    ├─ Retrieval Integrity Scoring
    │
    └─ Explanations + Visualizations
```
## Architecture Diagram

### High-Level Retrieval Integrity Audit Pipeline

```mermaid
flowchart TD
    Q[User Query]
    A[Aspect Extraction]
    QA[Query Aspects]

    D[PDF Document]
    C[Chunking]
    E[Embedding]
    V[Vector Index]

    R[Top-K Retrieval]
    S[Similarity Matrix]

    CA[Coverage Analysis]
    ND[Noise Detection]
    MS[Missing Evidence]

    SC[Integrity Score]
    EX[Explanation & Recommendations]
    HM[Coverage Heatmap]

    Q --> A --> QA
    D --> C --> E --> V
    QA --> S
    Q --> E
    V --> R --> S
    S --> CA
    S --> ND
    CA --> MS
    CA --> SC
    ND --> SC
    MS --> SC
    SC --> EX
    CA --> HM

---

## Inputs (as per Track-3)

* **User Query** (string)
* **Knowledge Base**

  * Documents split into chunks with metadata
* **Retrieval Output**

  * Top-K retrieved chunks with similarity scores
* *(Optional)* Ground-truth relevant chunks (not required for demo)

> Note: For demonstration purposes, retrieval is simulated using an in-memory vector store.
> The audit logic operates **after retrieval** and is independent of how retrieval is implemented.

---

## Outputs (as per Track-3)

* Retrieval Integrity Score (0–100)
* Aspect-wise coverage analysis
* Chunk classification (supporting / partial / noise)
* Missing critical evidence
* Improvement recommendations
* Explainable, non-technical reasoning
* Aspect × Chunk coverage heatmap

---

## Tech Stack

* **Language:** Python 3
* **UI:** Streamlit
* **Embeddings:** OpenAI `text-embedding-3-small`
* **LLM (aspects):** OpenAI `gpt-4o-mini`
* **Vector Store:** In-memory NumPy cosine similarity
* **PDF Parsing:** PyMuPDF
* **Visualization:** Plotly
* **Environment:** python-dotenv

---

## Performance Optimizations

* Batched embeddings (single API call per document)
* File hashing to avoid re-indexing unchanged PDFs
* Chunk pruning to remove low-value text
* Session-state caching for fast re-queries

Typical ingestion time:

* First upload: ~3–6 seconds
* Re-queries on same document: instant

---

## How to Run

### 1. Clone the repository

```bash
git clone <repo-url>
cd retrieval_integrity_auditor
```

### 2. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set environment variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

### 5. Run the app

```bash
streamlit run app.py
```

---

## How to Use the Application

1. Upload a PDF document (knowledge base)
2. Enter any natural language query
3. Click **Run Retrieval Audit**
4. Review:

   * Query aspects
   * Retrieved chunks
   * Coverage heatmap
   * Integrity score
   * Explanations and recommendations

---

## Track-3 Alignment Summary

| Requirement                | Status |
| -------------------------- | ------ |
| Audit retrieval only       | ✅      |
| No generation              | ✅      |
| Explainable outputs        | ✅      |
| Coverage + noise detection | ✅      |
| Missing evidence detection | ✅      |
| Integrity score            | ✅      |
| Mandatory visualization    | ✅      |
| Demo-ready under 5s        | ✅      |

---

## Future Enhancements

* Hybrid retrieval (BM25 + embeddings)
* Cross-encoder re-ranking
* Multi-document knowledge bases
* Ground-truth based evaluation mode
* Exportable audit reports

---

## Final Note

This project focuses on **retrieval quality as a first-class concern** in enterprise RAG systems.
It provides a transparent, explainable way to diagnose failures **before generation**, which is critical for trust, safety, and reliability.

---

If you want, I can also:

* shorten this to a **1-page judge README**
* add an **architecture diagram**
* write a **2-minute demo script**
* or tailor the README exactly to the competition portal

Just tell me.
