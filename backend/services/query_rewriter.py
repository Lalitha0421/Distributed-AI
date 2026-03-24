from groq import Groq
from core.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def rewrite_query(query):

    prompt = f"""
Rewrite the following user query to improve document retrieval.

Rules:
- Return ONLY the improved search query
- Do NOT explain anything
- Do NOT add sentences
- Maximum 12 words
- Focus on key technical terms

User query:
{query}

Improved search query:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You improve search queries for document retrieval."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=40
    )

    rewritten = response.choices[0].message.content.strip()
    rewritten = rewritten.split("\n")[0]
    rewritten = rewritten.replace('"', '').strip()

    return rewritten