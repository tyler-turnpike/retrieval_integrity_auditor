def generate_recommendations(coverage, noise, missing):
    recs = []

    if missing:
        recs.append("Increase retrieval depth or improve query formulation.")

    if any(n["classification"] == "noise" for n in noise):
        recs.append("Apply re-ranking or filtering to remove noisy chunks.")

    if not recs:
        recs.append("Retrieval quality is sufficient.")

    return recs
