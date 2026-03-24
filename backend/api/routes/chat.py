from fastapi import APIRouter

from services.hybrid_search import hybrid_search
from services.reranker import rerank
from services.memory import add_message, get_history
from services.llm_service import generate_answer
from services.query_rewriter import rewrite_query

router = APIRouter()


@router.post("/ask")
def ask_question(question: str, session_id: str = "default", source: str = None):

    question = question.strip()

    if not question:
        return {"error": "Question cannot be empty"}

    # Rewrite query safely
    try:
        rewritten_query = rewrite_query(question)
    except Exception as e:
        print("Rewrite error:", e)
        rewritten_query = question

    # Retrieve
    chunks = hybrid_search(rewritten_query, source)

    if not chunks:
        return {
            "question": question,
            "answer": "No relevant information found.",
            "sources": []
        }

    # Rerank
    chunks = rerank(rewritten_query, chunks)

    # Build context
    context_parts = []
    for i, c in enumerate(chunks[:3]):
        context_parts.append(f"Source {i+1}:\n{c.get('text','')}")

    context = "\n\n".join(context_parts)

    # History
    history = get_history(session_id)

    # Generate answer
    answer = generate_answer(question, context, history)

    # Store conversation
    add_message(session_id, "user", question)
    add_message(session_id, "assistant", answer)

    # Sources
    sources = [
        {
            "source": c.get("source", "unknown"),
            "chunk_id": c.get("chunk_id", "unknown")
        }
        for c in chunks[:3]
    ]

    return {
        "question": question,
        "rewritten_query": rewritten_query,
        "answer": answer,
        "sources": sources
    }