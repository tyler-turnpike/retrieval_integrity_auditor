def detect_missing_evidence(coverage_results):
    """
    Missing evidence = aspects with NO supporting or partial chunk.
    """

    missing = []

    for res in coverage_results:
        if res["coverage"] == "missing":
            missing.append({
                "aspect_text": res["aspect_text"],
                "coverage": "missing"
            })

    return missing
