import numpy as np


def analyze_coverage(
    aspects,
    similarity_matrix,
    retrieved_chunks,
    support_threshold=0.6,
    partial_threshold=0.35
):
    """
    Determine coverage for each query aspect.
    Adds a small heuristic boost for definitional text.
    """

    results = []
    definition_keywords = [
        "is defined as",
        "refers to",
        "means that",
        "can be defined as"
    ]

    for i, aspect in enumerate(aspects):
        sims = similarity_matrix[i]

        best_idx = int(np.argmax(sims))
        best_sim = float(sims[best_idx])

        # Heuristic boost for definitions
        chunk_text = retrieved_chunks[best_idx]["text"].lower()
        if any(k in chunk_text for k in definition_keywords):
            best_sim += 0.15

        if best_sim >= support_threshold:
            coverage = "supported"
        elif best_sim >= partial_threshold:
            coverage = "partial"
        else:
            coverage = "missing"

        results.append({
            "aspect_id": aspect["aspect_id"],
            "aspect_text": aspect["aspect_text"],
            "best_chunk_index": best_idx,
            "best_similarity": round(best_sim, 3),
            "coverage": coverage
        })

    return results
