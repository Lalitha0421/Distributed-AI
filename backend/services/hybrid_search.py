from services.vector_store import search_chunks, get_all_chunks
from rank_bm25 import BM25Okapi


def hybrid_search(query, source=None):

    # VECTOR SEARCH
    vector_results = search_chunks(query, source) or []

    # KEYWORD SEARCH (BM25)
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

    # MERGE RESULTS
    merged = { (r["source"], r["chunk_id"]): r for r in vector_results }

    for r in bm25_results:
        merged[(r["source"], r["chunk_id"])] = r

    return list(merged.values())