# from services.vector_store import search_chunks, get_all_chunks
# from rank_bm25 import BM25Okapi


# def hybrid_search(query, source=None):

#     # VECTOR SEARCH
#     vector_results = search_chunks(query, source) or []

#     # KEYWORD SEARCH (BM25)
#     all_chunks = get_all_chunks(source)

#     if not all_chunks:
#         return vector_results

#     texts = [c["text"] for c in all_chunks]

#     tokenized = [t.split() for t in texts]

#     bm25 = BM25Okapi(tokenized)

#     scores = bm25.get_scores(query.split())

#     bm25_ranked = sorted(
#         zip(all_chunks, scores),
#         key=lambda x: x[1],
#         reverse=True
#     )

#     bm25_results = [r[0] for r in bm25_ranked[:5]]

#     # MERGE RESULTS
#     merged = { (r["source"], r["chunk_id"]): r for r in vector_results }

#     for r in bm25_results:
#         merged[(r["source"], r["chunk_id"])] = r

#     return list(merged.values())

from app.services.vector_store import search_chunks, get_all_chunks
from rank_bm25 import BM25Okapi
from app.core.logger import logger

def hybrid_search(query: str, source: str = None):
    """Hybrid search combining vector similarity and BM25 keyword search."""
    try:
        # Vector search
        vector_results = search_chunks(query, source) or []

        # Keyword search (BM25)
        all_chunks = get_all_chunks(source)

        if not all_chunks:
            return vector_results

        texts = [c["text"] for c in all_chunks]
        tokenized = [t.split() for t in texts]

        bm25 = BM25Okapi(tokenized)
        scores = bm25.get_scores(query.split())

        bm25_ranked = sorted(
            zip(all_chunks, scores),
            key=lambda x: x[1],
            reverse=True
        )

        bm25_results = [r[0] for r in bm25_ranked[:5]]

        # Merge results (remove duplicates)
        merged = {(r["source"], r.get("chunk_id")): r for r in vector_results}
        for r in bm25_results:
            merged[(r["source"], r.get("chunk_id"))] = r

        logger.info(f"Hybrid search returned {len(merged)} results for query: {query[:50]}...")
        return list(merged.values())

    except Exception as e:
        logger.error(f"Hybrid search failed: {e}")
        return []