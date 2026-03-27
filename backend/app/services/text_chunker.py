

# from nltk.tokenize import sent_tokenize


# def split_text_into_chunks(text, sentences_per_chunk=7):

#     sentences = sent_tokenize(text)

#     chunks = []

#     for i in range(0, len(sentences), sentences_per_chunk):

#         chunk = " ".join(sentences[i:i+sentences_per_chunk])

#         chunks.append(chunk)

#     return chunks

from typing import List

def split_text_into_chunks(
    text: str, 
    chunk_size: int = 400, 
    chunk_overlap: int = 80
) -> List[str]:
    """Improved chunking that works better for short documents."""
    if not text or len(text.strip()) == 0:
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]

        # Try to cut at sentence end for cleaner chunks
        if end < text_length:
            last_period = max(chunk.rfind('.'), chunk.rfind('\n'))
            if last_period > chunk_size // 2:
                end = start + last_period + 1
                chunk = text[start:end]

        cleaned = chunk.strip()
        if cleaned:
            chunks.append(cleaned)

        start = end - chunk_overlap

    # If document is very short, return the whole text as one chunk
    if not chunks and text.strip():
        chunks.append(text.strip())

    return chunks