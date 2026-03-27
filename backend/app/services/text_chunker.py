

# from nltk.tokenize import sent_tokenize


# def split_text_into_chunks(text, sentences_per_chunk=7):

#     sentences = sent_tokenize(text)

#     chunks = []

#     for i in range(0, len(sentences), sentences_per_chunk):

#         chunk = " ".join(sentences[i:i+sentences_per_chunk])

#         chunks.append(chunk)

#     return chunks

from typing import List

def split_text_into_chunks(text: str, chunk_size: int = 300, chunk_overlap: int = 50) -> List[str]:
    """Better chunking for short and long documents."""
    if not text or len(text.strip()) == 0:
        return []

    text = text.strip()

    # If the entire document is very short, return it as one chunk
    if len(text) < 400:
        return [text]

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]

        # Try to break at natural points
        if end < text_length:
            last_break = max(chunk.rfind('.'), chunk.rfind('\n'), chunk.rfind(' '))
            if last_break > chunk_size // 2:
                end = start + last_break + 1
                chunk = text[start:end]

        cleaned = chunk.strip()
        if cleaned:
            chunks.append(cleaned)

        start = end - chunk_overlap

    return chunks