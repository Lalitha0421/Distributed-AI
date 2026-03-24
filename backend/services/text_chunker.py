


from nltk.tokenize import sent_tokenize


def split_text_into_chunks(text, sentences_per_chunk=7):

    sentences = sent_tokenize(text)

    chunks = []

    for i in range(0, len(sentences), sentences_per_chunk):

        chunk = " ".join(sentences[i:i+sentences_per_chunk])

        chunks.append(chunk)

    return chunks