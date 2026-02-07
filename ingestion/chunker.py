def chunk_text(text: str, chunk_size: int = 180, overlap: int = 40):
    """
    Split text into small, high-quality overlapping chunks.
    Filters headers, footers, and low-value fragments.
    """

    chunks = []
    start = 0
    length = len(text)

    while start < length:
        end = start + chunk_size
        chunk = text[start:end].strip()

        if (
            len(chunk) > 80 and
            not chunk.lower().startswith(
                ("page ", "chapter", "figure", "table")
            )
        ):
            chunks.append(chunk)

        start = end - overlap

    return chunks
