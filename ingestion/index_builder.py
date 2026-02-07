from vector_store.vector_db import VectorDB


def build_vector_index(chunks, embeddings):
    """
    Build an in-memory vector index from chunks + embeddings.
    """

    vector_db = VectorDB()

    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        vector_db.add(
            chunk_id=f"chunk_{i}",
            embedding=emb,
            text=chunk
        )

    return vector_db
