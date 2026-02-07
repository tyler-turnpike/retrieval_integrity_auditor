import numpy as np


def similarity_matrix(aspect_embeddings, chunk_embeddings):
    matrix = np.zeros((len(aspect_embeddings), len(chunk_embeddings)))

    for i, a in enumerate(aspect_embeddings):
        for j, c in enumerate(chunk_embeddings):
            matrix[i][j] = np.dot(a, c) / (
                np.linalg.norm(a) * np.linalg.norm(c)
            )

    return matrix
