# from groq import Groq
# from core.config import GROQ_API_KEY

# client = Groq(api_key=GROQ_API_KEY)


# def rewrite_query(query):

#     prompt = f"""
# Rewrite the following user query to improve document retrieval.

# Rules:
# - Return ONLY the improved search query
# - Do NOT explain anything
# - Do NOT add sentences
# - Maximum 12 words
# - Focus on key technical terms

# User query:
# {query}

# Improved search query:
# """

#     response = client.chat.completions.create(
#         model="llama-3.1-8b-instant",
#         messages=[
#             {"role": "system", "content": "You improve search queries for document retrieval."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.1,
#         max_tokens=40
#     )

#     rewritten = response.choices[0].message.content.strip()
#     rewritten = rewritten.split("\n")[0]
#     rewritten = rewritten.replace('"', '').strip()

#     return rewritten


from groq import Groq
from app.core.config import GROQ_API_KEY
from app.core.logger import logger

client = Groq(api_key=GROQ_API_KEY)

def rewrite_query(query: str) -> str:
    """Rewrite user query to improve retrieval quality."""
    try:
        prompt = f"""
Rewrite the following user query to improve document retrieval in a RAG system.

Rules:
- Return ONLY the improved search query
- Do NOT explain anything
- Maximum 15 words
- Focus on key technical terms and make it more specific

User query: {query}

Improved search query:
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an expert query optimizer for document retrieval."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=50
        )

        rewritten = response.choices[0].message.content.strip()
        # Clean output
        rewritten = rewritten.split("\n")[0].replace('"', '').strip()
        logger.info(f"Rewritten query: {rewritten}")
        return rewritten

    except Exception as e:
        logger.warning(f"Query rewrite failed: {e}. Using original query.")
        return query