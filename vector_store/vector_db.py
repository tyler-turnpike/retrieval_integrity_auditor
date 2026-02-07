import numpy as np


class VectorDB:
    def __init__(self):
        self.embeddings = []
        self.texts = []
        self.chunk_ids = []

    def add(self, chunk_id, embedding, text):
        self.embeddings.append(np.array(embedding))
        self.texts.append(text)
        self.chunk_ids.append(chunk_id)

    def search(self, query_embedding, top_k=5):
        query_vec = np.array(query_embedding)

        similarities = []
        for emb in self.embeddings:
            sim = np.dot(query_vec, emb) / (
                np.linalg.norm(query_vec) * np.linalg.norm(emb)
            )
            similarities.append(sim)

        top_indices = np.argsort(similarities)[::-1][:top_k]

        return [
            {
                "chunk_id": self.chunk_ids[i],
                "text": self.texts[i],
                "similarity_score": float(similarities[i])
            }
            for i in top_indices
        ]
