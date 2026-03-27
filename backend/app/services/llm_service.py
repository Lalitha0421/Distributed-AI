
# # from groq import Groq
# # from app.core.config import GROQ_API_KEY, MODEL_NAME
# # from app.core.logger import logger

# # client = Groq(api_key=GROQ_API_KEY)

# # def generate_answer(question: str, context: str, history: list):
# #     """Generate answer using Groq LLM with context and conversation history."""
# #     try:
# #         # Format history for prompt
# #         history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history]) if history else "No previous conversation."

# #         prompt = f"""
# # You are a helpful AI assistant answering questions based ONLY on the provided document context.

# # Conversation History:
# # {history_str}

# # Context from documents:
# # {context}

# # Question: {question}

# # Instructions:
# # - Answer using ONLY the information in the context above.
# # - Be clear, concise, and accurate.
# # - If the context does not contain the answer, respond exactly: "No relevant information found in the selected document."
# # - Do not add information from your general knowledge.
# # - Use bullet points only if it improves readability.

# # Answer:
# # """

# #         response = client.chat.completions.create(
# #             model=MODEL_NAME,
# #             messages=[
# #                 {"role": "system", "content": "You are a precise document-based assistant."},
# #                 {"role": "user", "content": prompt}
# #             ],
# #             temperature=0.3,
# #             max_tokens=500
# #         )

# #         answer = response.choices[0].message.content.strip()
# #         logger.info(f"Generated answer for question: {question[:60]}...")
# #         return answer

# #     except Exception as e:
# #         logger.error(f"LLM generation failed: {e}")
# #         return "Sorry, I encountered an error while generating the answer. Please try again."

# from groq import Groq
# from app.core.config import GROQ_API_KEY, MODEL_NAME
# from app.core.logger import logger

# client = Groq(api_key=GROQ_API_KEY)

# # backend/app/services/llm_service.py  (replace only the function, keep the imports)

# # async def generate_answer_stream(question: str, context: str, history: list):
# #     """Improved streaming with better token handling for readability. Clean streaming with larger, more natural tokens."""
# #     try:
# #         history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history]) if history else "No previous conversation."

# #         prompt = f"""
# # You are a helpful assistant answering questions from the given document.
# # You are a helpful, clear assistant. Answer naturally using only the provided document content.
# # Always use proper spacing, punctuation, and full names. Never break words.
# # Write in complete, readable sentences.

# # Document Content:
# # {context}

# # Question: {question}

# # Answer the question clearly and naturally using the document content.
# # Use proper spacing and punctuation.
# # If the document is short, still provide the best possible answer from what is available.
# # Do not say "No relevant information" if any part of the document is related.
# # Provide a clear, well-formatted answer based on the document.
# # Answer:
# # """

# #         stream = client.chat.completions.create(
# #             model=MODEL_NAME,
# #             messages=[
# #                 {"role": "system", "content": "You are a precise assistant that answers from the provided document."},
# #                 {"role": "user", "content": prompt}
# #             ],
# #             temperature=0.2,
# #             max_tokens=1000,
# #             stream=True
# #         )

# #         full_answer = ""
# #         for chunk in stream:
# #             if chunk.choices[0].delta.content is not None:
# #                 content = chunk.choices[0].delta.content
# #                 # full_answer += content
# #                 yield content   # Yield raw token

# #         logger.info(f"Streamed answer for: {question[:60]}...")

# #     except Exception as e:
# #         logger.error(f"Streaming generation failed: {e}")
# #         yield "Sorry, I encountered an error while generating the answer."


# async def generate_answer_stream(question: str, context: str, history: list):
#     """Clean streaming with larger, more natural tokens."""
#     try:
#         history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history]) if history else ""

#         system_prompt = """You are a helpful, clear assistant. Answer naturally using only the provided document content.
# Always use proper spacing, punctuation, and full names. Never break words.
# Write in complete, readable sentences."""

#         user_prompt = f"""Document Content:
# {context}

# Conversation History:
# {history_str}

# Question: {question}

# Provide a clear, well-formatted answer based on the document."""

#         stream = client.chat.completions.create(
#             model=MODEL_NAME,
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": user_prompt}
#             ],
#             temperature=0.2,      # Lower = more consistent output
#             max_tokens=1000,
#             stream=True
#         )

#         for chunk in stream:
#             if chunk.choices[0].delta.content is not None:
#                 token = chunk.choices[0].delta.content
#                 yield token   # Still stream for real-time feel

#     except Exception as e:
#         logger.error(f"Streaming error: {e}")
#         yield "\nSorry, I encountered an error while generating the answer."

from groq import Groq
from app.core.config import GROQ_API_KEY, MODEL_NAME
from app.core.logger import logger

client = Groq(api_key=GROQ_API_KEY)

async def generate_answer_stream(question: str, context: str, history: list):
    """Final clean streaming - forces natural, well-spaced output."""
    try:
        history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history]) if history else ""

        system_prompt = """You are a clear, professional assistant. 
Always output complete words with proper spacing and punctuation.
Never break names or technical terms into pieces.
Use full sentences and natural readable English.
Write as if you are speaking clearly to a student."""

        user_prompt = f"""Document Content:
{context}

Previous Conversation:
{history_str}

Question: {question}

Provide a clear, well-formatted, natural answer based only on the document.
Use proper spacing between every word. Do not break any names or words."""

        stream = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,   # Very low for consistent, clean output
            max_tokens=1200,
            stream=True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                token = chunk.choices[0].delta.content
                yield token

        logger.info(f"Successfully streamed answer for: {question[:80]}...")

    except Exception as e:
        logger.error(f"Streaming generation failed: {e}")
        yield "\nSorry, I encountered an error while generating the answer. Please try again."