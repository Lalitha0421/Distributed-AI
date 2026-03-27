
# from groq import Groq
# from app.core.config import GROQ_API_KEY, MODEL_NAME
# from app.core.logger import logger

# client = Groq(api_key=GROQ_API_KEY)

# def generate_answer(question: str, context: str, history: list):
#     """Generate answer using Groq LLM with context and conversation history."""
#     try:
#         # Format history for prompt
#         history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history]) if history else "No previous conversation."

#         prompt = f"""
# You are a helpful AI assistant answering questions based ONLY on the provided document context.

# Conversation History:
# {history_str}

# Context from documents:
# {context}

# Question: {question}

# Instructions:
# - Answer using ONLY the information in the context above.
# - Be clear, concise, and accurate.
# - If the context does not contain the answer, respond exactly: "No relevant information found in the selected document."
# - Do not add information from your general knowledge.
# - Use bullet points only if it improves readability.

# Answer:
# """

#         response = client.chat.completions.create(
#             model=MODEL_NAME,
#             messages=[
#                 {"role": "system", "content": "You are a precise document-based assistant."},
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.3,
#             max_tokens=500
#         )

#         answer = response.choices[0].message.content.strip()
#         logger.info(f"Generated answer for question: {question[:60]}...")
#         return answer

#     except Exception as e:
#         logger.error(f"LLM generation failed: {e}")
#         return "Sorry, I encountered an error while generating the answer. Please try again."

from groq import Groq
from app.core.config import GROQ_API_KEY, MODEL_NAME
from app.core.logger import logger

client = Groq(api_key=GROQ_API_KEY)

# backend/app/services/llm_service.py  (replace only the function, keep the imports)

async def generate_answer_stream(question: str, context: str, history: list):
    """Generate answer with streaming support and better handling for short documents."""
    try:
        history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history]) if history else "No previous conversation."

        prompt = f"""
You are a helpful assistant answering questions from the given document.

Document Content:
{context}

Question: {question}

Answer the question based on the document above. 
If the document has relevant information, use it. 
If the document is short or partial, still give the best answer possible from what is available.
Keep the answer clear and direct.
"""

        stream = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a precise assistant that answers from given document context."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=600,
            stream=True
        )

        full_answer = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                full_answer += content
                yield content

        logger.info(f"Streamed answer for: {question[:60]}...")

    except Exception as e:
        logger.error(f"Streaming generation failed: {e}")
        yield "Sorry, I encountered an error while generating the answer. Please try again."