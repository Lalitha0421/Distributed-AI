
# # llm_service.py
# # llm_service.py
# # llm_service.py
# # llm_service.py

# from groq import Groq
# from core.config import GROQ_API_KEY, MODEL_NAME

# client = Groq(api_key=GROQ_API_KEY)


# def generate_answer(question, context,history):

#     prompt = f"""
# You are an AI assistant answering questions from documents.

# Use ONLY the information provided in the context.
# Conversation history:
# {history}


# Context:
# {context}

# Question:
# {question}

# Instructions:
# - Write a clear explanation
# - Remove duplicate information
# - Do NOT include raw newline characters like \\n
# - Do NOT repeat the context
# - Keep the answer concise
# - Use bullet points only if helpful
# - If the context does not contain the answer, respond exactly:
#   "No relevant information found in the selected document."

# Answer:
# """

#     response = client.chat.completions.create(
#         model=MODEL_NAME,
#         messages=[
#             {"role": "system", "content": "Answer using only the context."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.3,
#         max_tokens=400
#     )

#     answer = response.choices[0].message.content
#     answer = answer.replace("\n\n", "\n").strip()
#     return answer


from groq import Groq
from app.core.config import GROQ_API_KEY, MODEL_NAME
from app.core.logger import logger

client = Groq(api_key=GROQ_API_KEY)

def generate_answer(question: str, context: str, history: list):
    """Generate answer using Groq LLM with context and conversation history."""
    try:
        # Format history for prompt
        history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history]) if history else "No previous conversation."

        prompt = f"""
You are a helpful AI assistant answering questions based ONLY on the provided document context.

Conversation History:
{history_str}

Context from documents:
{context}

Question: {question}

Instructions:
- Answer using ONLY the information in the context above.
- Be clear, concise, and accurate.
- If the context does not contain the answer, respond exactly: "No relevant information found in the selected document."
- Do not add information from your general knowledge.
- Use bullet points only if it improves readability.

Answer:
"""

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a precise document-based assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )

        answer = response.choices[0].message.content.strip()
        logger.info(f"Generated answer for question: {question[:60]}...")
        return answer

    except Exception as e:
        logger.error(f"LLM generation failed: {e}")
        return "Sorry, I encountered an error while generating the answer. Please try again."