

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
    chunk_size: int = 500, 
    chunk_overlap: int = 50
) -> List[str]:
    """Split text into overlapping chunks for better RAG context."""
    if not text or len(text.strip()) == 0:
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        
        # Get chunk
        chunk = text[start:end]
        
        # Try to cut at sentence end for cleaner chunks
        if end < text_length:
            last_period = chunk.rfind('.')
            if last_period > chunk_size // 2:
                end = start + last_period + 1
                chunk = text[start:end]
        
        cleaned_chunk = chunk.strip()
        if cleaned_chunk:
            chunks.append(cleaned_chunk)
        
        # Move window with overlap
        start = end - chunk_overlap

    return chunks