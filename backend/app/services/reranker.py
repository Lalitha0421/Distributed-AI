# from sentence_transformers import CrossEncoder

# reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


# def rerank(query, chunks):

#     pairs = [(query, c["text"]) for c in chunks]

#     scores = reranker.predict(pairs)

#     ranked = sorted(
#         zip(chunks, scores),
#         key=lambda x: x[1],
#         reverse=True
#     )

#     return [r[0] for r in ranked]


from sentence_transformers import CrossEncoder
from app.core.logger import logger

# Load reranker once
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(query: str, chunks: list):
    if not chunks:
        return []

    try:
        pairs = [(query, c["text"]) for c in chunks]
        scores = reranker.predict(pairs)

        ranked = sorted(
            zip(chunks, scores),
            key=lambda x: x[1],
            reverse=True
        )

        logger.info(f"Reranked {len(chunks)} chunks")
        return [r[0] for r in ranked]

    except Exception as e:
        logger.warning(f"Reranking failed: {e}. Returning original order.")
        return chunks