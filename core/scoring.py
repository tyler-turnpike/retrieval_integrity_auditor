def compute_retrieval_integrity_score(coverage_results, noise_results, missing_results):
    """
    Compute a balanced retrieval integrity score (0–100).
    """

    total_aspects = len(coverage_results)

    supported = sum(1 for a in coverage_results if a["coverage"] == "supported")
    partial = sum(1 for a in coverage_results if a["coverage"] == "partial")
    missing = len(missing_results)

    coverage_score = ((supported + 0.5 * partial) / total_aspects) * 100

    noise_chunks = sum(1 for n in noise_results if n["classification"] == "noise")
    noise_penalty = min(30, noise_chunks * 10)

    missing_penalty = min(30, missing * 15)

    final_score = max(0, coverage_score - noise_penalty - missing_penalty)

    return round(final_score, 1), {
        "coverage_score": round(coverage_score, 2),
        "noise_penalty": noise_penalty,
        "missing_penalty": missing_penalty
    }
