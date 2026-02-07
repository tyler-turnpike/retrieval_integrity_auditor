from embeddings import client


def embed_chunks(chunks):
    """
    Embed all chunks in ONE OpenAI API call.
    This is the biggest performance improvement.
    """

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=chunks
    )

    return [d.embedding for d in response.data]
