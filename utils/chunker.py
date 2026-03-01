def chunk_text(text, size=250, overlap=50):
    words = text.split()

    chunks = []
    start = 0

    while start < len(words):
        chunk = words[start:start + size]
        chunks.append(" ".join(chunk))
        start += size - overlap

    return chunks