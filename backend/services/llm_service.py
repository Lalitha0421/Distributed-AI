
# llm_service.py
# llm_service.py
# llm_service.py
# llm_service.py

from groq import Groq
from core.config import GROQ_API_KEY, MODEL_NAME

client = Groq(api_key=GROQ_API_KEY)


def generate_answer(question, context,history):

    prompt = f"""
You are an AI assistant answering questions from documents.

Use ONLY the information provided in the context.
Conversation history:
{history}


Context:
{context}

Question:
{question}

Instructions:
- Write a clear explanation
- Remove duplicate information
- Do NOT include raw newline characters like \\n
- Do NOT repeat the context
- Keep the answer concise
- Use bullet points only if helpful
- If the context does not contain the answer, respond exactly:
  "No relevant information found in the selected document."

Answer:
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "Answer using only the context."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=400
    )

    answer = response.choices[0].message.content
    answer = answer.replace("\n\n", "\n").strip()
    return answer