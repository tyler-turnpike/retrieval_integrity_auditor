def generate_explanation(coverage, noise, missing):
    """
    Generate clear, non-technical explanations.
    """

    explanations = []

    for c in coverage:
        if c["coverage"] == "supported":
            explanations.append(
                f"The aspect '{c['aspect_text']}' is directly supported by the retrieved documents."
            )
        elif c["coverage"] == "partial":
            explanations.append(
                f"The aspect '{c['aspect_text']}' is partially supported, "
                f"but no chunk provides a clear, direct explanation."
            )
        else:
            explanations.append(
                f"The aspect '{c['aspect_text']}' is missing from the retrieved documents."
            )

    if not explanations:
        explanations.append("Retrieved documents sufficiently cover the query.")

    return explanations
