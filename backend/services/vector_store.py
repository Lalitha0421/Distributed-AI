from chromadb import Client
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import os

embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

os.makedirs("chroma_db", exist_ok=True)

client = Client(
    Settings(
        persist_directory="chroma_db",
        anonymized_telemetry=False
    )
)

def get_collection(source):

    collection_name = source.replace(".","_")

    return client.get_or_create_collection(name=collection_name)


def store_chunks(chunks, document_name="uploaded_document"):

    embeddings = embedding_model.encode(chunks).tolist()

    ids = [f"chunk_{i}" for i in range(len(chunks))]

    metadatas = [
    {
        "source": document_name,
        "chunk_id": i
    }
    for i in range(len(chunks))
]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )

    return len(chunks)

def search_chunks(query, source=None):

    query_embedding = embedding_model.encode(query).tolist()

    query_params = {
        "query_embeddings": [query_embedding],
        "n_results": 5
    }

    if source:
        query_params["where"] = {"source": source}

    results = collection.query(**query_params)

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    # VERY IMPORTANT SAFETY CHECK
    if not documents:
        return []

    combined = []

    for doc, meta, dist in zip(documents, metadatas, distances):
        combined.append({
            "text": doc,
            "source": meta["source"],
            "chunk_id": meta["chunk_id"],
            "score": float(dist)
        })

    return combined

def get_all_chunks(source=None):

    results = collection.get()

    documents = results.get("documents", [])
    metadatas = results.get("metadatas", [])

    combined = []

    for doc, meta in zip(documents, metadatas):

        if source and meta["source"] != source:
            continue

        combined.append({
            "text": doc,
            "source": meta["source"],
            "chunk_id": meta["chunk_id"]
        })

    return combined