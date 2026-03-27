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
from fastapi.responses import StreamingResponse
from app.services.hybrid_search import hybrid_search
from app.services.reranker import rerank
from app.services.memory import add_message, get_history
from app.services.llm_service import generate_answer_stream
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
        logger.warning(f"Query rewrite failed: {e}")
        rewritten_query = question

    # Retrieve and rerank
    chunks = hybrid_search(rewritten_query, source)
    if not chunks:
        async def no_info_stream():
            yield "data: No relevant information found in the uploaded documents.\n\n"
        return StreamingResponse(no_info_stream(), media_type="text/event-stream")

    chunks = rerank(rewritten_query, chunks)

    # Build context
    context_parts = [f"Source {i+1}:\n{c.get('text', '')}" for i, c in enumerate(chunks[:3])]
    context = "\n\n".join(context_parts)

    # Get history
    history = get_history(session_id)

    # Stream the answer
    async def stream_response():
        full_answer = ""
        async for token in generate_answer_stream(question, context, history):
            full_answer += token
            yield f"data: {token}\n\n"

        # Store final answer in memory
        add_message(session_id, "user", question)
        add_message(session_id, "assistant", full_answer)

        # Send sources at the end
        sources = [
            {
                "source": c.get("source", "unknown"),
                "chunk_id": c.get("chunk_id", "unknown"),
                "score": c.get("score")
            }
            for c in chunks[:3]
        ]
        yield f"data: [SOURCES]{sources}\n\n"

    return StreamingResponse(stream_response(), media_type="text/event-stream")