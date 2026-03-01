import faiss
import numpy as np
from rag.embedder import get_embedding

index = None
documents = []

def build_index(text_chunks):
    global index, documents

    if not text_chunks:
        return

    documents = text_chunks
    embeddings = get_embedding(text_chunks)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

def retrieve(query, k=3):
    global index

    if index is None:
        return []

    query_embedding = get_embedding([query])
    distances, indices = index.search(query_embedding, k)

    results = []
    for idx in indices[0]:
        if idx < len(documents):
            results.append(documents[idx])

    return results