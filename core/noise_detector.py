def detect_noise_chunks(retrieved_chunks, similarity_matrix, aspects):
    """
    Classify chunks based on their maximum support for ANY aspect.
    """

    results = []

    for j, chunk in enumerate(retrieved_chunks):
        max_support = max(
            similarity_matrix[i][j] for i in range(len(aspects))
        )

        if max_support >= 0.65:
            classification = "supporting"
        elif max_support >= 0.4:
            classification = "partial"
        else:
            classification = "noise"

        results.append({
            "chunk_id": chunk["chunk_id"],
            "classification": classification
        })

    return results
