# from fastapi import APIRouter

# from services.hybrid_search import hybrid_search
# from services.reranker import rerank
# from services.memory import add_message, get_history
# from services.llm_service import generate_answer
# from services.query_rewriter import rewrite_query

# router = APIRouter()


# @router.post("/ask")
# def ask_question(question: str, session_id: str = "default", source: str = None):

#     question = question.strip()

#     if not question:
#         return {"error": "Question cannot be empty"}

#     # Rewrite query safely
#     try:
#         rewritten_query = rewrite_query(question)
#     except Exception as e:
#         print("Rewrite error:", e)
#         rewritten_query = question

#     # Retrieve
#     chunks = hybrid_search(rewritten_query, source)

#     if not chunks:
#         return {
#             "question": question,
#             "answer": "No relevant information found.",
#             "sources": []
#         }

#     # Rerank
#     chunks = rerank(rewritten_query, chunks)

#     # Build context
#     context_parts = []
#     for i, c in enumerate(chunks[:3]):
#         context_parts.append(f"Source {i+1}:\n{c.get('text','')}")

#     context = "\n\n".join(context_parts)

#     # History
#     history = get_history(session_id)

#     # Generate answer
#     answer = generate_answer(question, context, history)

#     # Store conversation
#     add_message(session_id, "user", question)
#     add_message(session_id, "assistant", answer)

#     # Sources
#     sources = [
#         {
#             "source": c.get("source", "unknown"),
#             "chunk_id": c.get("chunk_id", "unknown")
#         }
#         for c in chunks[:3]
#     ]

#     return {
#         "question": question,
#         "rewritten_query": rewritten_query,
#         "answer": answer,
#         "sources": sources
#     }


from fastapi import APIRouter, HTTPException
from app.services.hybrid_search import hybrid_search
from app.services.reranker import rerank
from app.services.memory import add_message, get_history
from app.services.llm_service import generate_answer
from app.services.query_rewriter import rewrite_query
from app.core.logger import logger
from app.models.request_models import QuestionRequest

router = APIRouter(prefix="/ask")

@router.post("/")
async def ask_question(request: QuestionRequest, session_id: str = "default", source: str = None):
    question = request.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    logger.info(f"Received question: {question} | Session: {session_id}")

    # Query rewriting
    try:
        rewritten_query = rewrite_query(question)
    except Exception as e:
        logger.warning(f"Query rewrite failed: {e}. Using original query.")
        rewritten_query = question

    # Retrieve chunks
    chunks = hybrid_search(rewritten_query, source)

    if not chunks:
        return {
            "question": question,
            "rewritten_query": rewritten_query,
            "answer": "No relevant information found in the uploaded documents.",
            "sources": []
        }

    # Rerank
    chunks = rerank(rewritten_query, chunks)

    # Build context
    context_parts = [f"Source {i+1}:\n{c.get('text', '')}" for i, c in enumerate(chunks[:3])]
    context = "\n\n".join(context_parts)

    # Get conversation history
    history = get_history(session_id)

    # Generate answer
    try:
        answer = generate_answer(question, context, history)
    except Exception as e:
        logger.error(f"LLM generation failed: {e}")
        answer = "Sorry, I encountered an error while generating the answer."

    # Store in memory
    add_message(session_id, "user", question)
    add_message(session_id, "assistant", answer)

    # Prepare sources for response
    sources = [
        {
            "source": c.get("source", "unknown"),
            "chunk_id": c.get("chunk_id", "unknown"),
            "score": c.get("score")
        }
        for c in chunks[:3]
    ]

    return {
        "question": question,
        "rewritten_query": rewritten_query,
        "answer": answer,
        "sources": sources
    }