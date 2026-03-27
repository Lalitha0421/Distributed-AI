# from chromadb import Client
# from chromadb.config import Settings
# from sentence_transformers import SentenceTransformer
# import os

# embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# os.makedirs("chroma_db", exist_ok=True)

# client = Client(
#     Settings(
#         persist_directory="chroma_db",
#         anonymized_telemetry=False
#     )
# )

# def get_collection(source):

#     collection_name = source.replace(".","_")

#     return client.get_or_create_collection(name=collection_name)


# def store_chunks(chunks, document_name="uploaded_document"):

#     embeddings = embedding_model.encode(chunks).tolist()

#     ids = [f"chunk_{i}" for i in range(len(chunks))]

#     metadatas = [
#     {
#         "source": document_name,
#         "chunk_id": i
#     }
#     for i in range(len(chunks))
# ]

#     collection.add(
#         documents=chunks,
#         embeddings=embeddings,
#         ids=ids,
#         metadatas=metadatas
#     )

#     return len(chunks)

# def search_chunks(query, source=None):

#     query_embedding = embedding_model.encode(query).tolist()

#     query_params = {
#         "query_embeddings": [query_embedding],
#         "n_results": 5
#     }

#     if source:
#         query_params["where"] = {"source": source}

#     results = collection.query(**query_params)

#     documents = results.get("documents", [[]])[0]
#     metadatas = results.get("metadatas", [[]])[0]
#     distances = results.get("distances", [[]])[0]

#     # VERY IMPORTANT SAFETY CHECK
#     if not documents:
#         return []

#     combined = []

#     for doc, meta, dist in zip(documents, metadatas, distances):
#         combined.append({
#             "text": doc,
#             "source": meta["source"],
#             "chunk_id": meta["chunk_id"],
#             "score": float(dist)
#         })

#     return combined

# def get_all_chunks(source=None):

#     results = collection.get()

#     documents = results.get("documents", [])
#     metadatas = results.get("metadatas", [])

#     combined = []

#     for doc, meta in zip(documents, metadatas):

#         if source and meta["source"] != source:
#             continue

#         combined.append({
#             "text": doc,
#             "source": meta["source"],
#             "chunk_id": meta["chunk_id"]
#         })

#     return combined



import os
import re
from chromadb import Client
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from app.core.logger import logger

# Load embedding model
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

os.makedirs("chroma_db", exist_ok=True)

client = Client(
    Settings(
        persist_directory="chroma_db",
        anonymized_telemetry=False
    )
)

def sanitize_collection_name(name: str) -> str:
    """Robust sanitization for ChromaDB collection names."""
    if not name:
        return "default_document"

    # Remove file extension
    name = os.path.splitext(name)[0]

    # Replace all invalid characters with underscore
    name = re.sub(r'[^a-zA-Z0-9._-]', '_', name)

    # Remove consecutive underscores
    name = re.sub(r'_+', '_', name)

    # Remove leading/trailing underscores and dots
    name = name.strip('_.-')

    # Ensure minimum length and valid start/end
    if len(name) < 3:
        name = "doc_" + name
    if not name or not name[0].isalnum():
        name = "doc_" + name
    if not name[-1].isalnum():
        name = name + "_doc"

    # Limit length
    if len(name) > 63:
        name = name[:60] + "_doc"

    return name.lower()


def get_collection(document_name: str):
    collection_name = sanitize_collection_name(document_name)
    logger.info(f"Using collection name: {collection_name} for file: {document_name}")
    return client.get_or_create_collection(name=collection_name)


def store_chunks(chunks: list, document_name: str = "uploaded_document"):
    if not chunks:
        return 0

    collection = get_collection(document_name)

    embeddings = embedding_model.encode(chunks).tolist()
    ids = [f"chunk_{i}_{document_name}" for i in range(len(chunks))]

    metadatas = [
        {
            "source": document_name,
            "chunk_id": i,
            "chunk_index": i
        }
        for i in range(len(chunks))
    ]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )

    logger.info(f"Stored {len(chunks)} chunks for document: {document_name}")
    return len(chunks)


def search_chunks(query: str, source: str = None):
    try:
        query_embedding = embedding_model.encode(query).tolist()

        query_params = {
            "query_embeddings": [query_embedding],
            "n_results": 10
        }

        if source:
            query_params["where"] = {"source": source}

        collection = get_collection(source if source else "default")
        results = collection.query(**query_params)

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        if not documents:
            return []

        combined = []
        for doc, meta, dist in zip(documents, metadatas, distances):
            combined.append({
                "text": doc,
                "source": meta.get("source"),
                "chunk_id": meta.get("chunk_id"),
                "score": float(dist) if dist is not None else None
            })
        return combined

    except Exception as e:
        logger.error(f"Vector search failed: {e}")
        return []


def get_all_chunks(source: str = None):
    try:
        collection = get_collection(source if source else "default")
        results = collection.get()

        documents = results.get("documents", [])
        metadatas = results.get("metadatas", [])

        combined = []
        for doc, meta in zip(documents, metadatas):
            if source and meta.get("source") != source:
                continue
            combined.append({
                "text": doc,
                "source": meta.get("source"),
                "chunk_id": meta.get("chunk_id")
            })
        return combined

    except Exception as e:
        logger.error(f"Get all chunks failed: {e}")
        return []