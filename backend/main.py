# from fastapi import FastAPI, UploadFile, File
# import shutil
# import os

# from services.hybrid_search import hybrid_search
# from services.reranker import rerank
# from services.memory import add_message, get_history

# from services.document_processor import extract_text_from_pdf
# from services.text_chunker import split_text_into_chunks
# from services.vector_store import store_chunks, search_chunks
# from services.llm_service import generate_answer

# app = FastAPI()

# UPLOAD_FOLDER = "../data"


# @app.get("/")
# def home():
#     return {"message": "AI Knowledge System Running"}


# @app.post("/upload")
# def upload_document(file: UploadFile = File(...)):

#     file_location = os.path.join(UPLOAD_FOLDER, file.filename)

#     with open(file_location, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     extracted_text = extract_text_from_pdf(file_location)

#     chunks = split_text_into_chunks(extracted_text)

#     stored = store_chunks(chunks)

#     return {
#         "message": "File uploaded successfully",
#         "characters_extracted": len(extracted_text),
#         "chunks_created": len(chunks),
#         "chunks_stored": stored
#     }


# @app.post("/ask")
# def ask_question(question: str):

#     # retrieve
#     chunks = hybrid_search(question)

#     # rerank
#     chunks = rerank(question, chunks)

#     context = "\n".join(chunks[:3])

#     # conversation history
#     history = get_history()

#     answer = generate_answer(question, context)

#     add_message("user", question)
#     add_message("assistant", answer)

#     return {
#         "question": question,
#         "answer": answer,
#         "sources": chunks[:3]
#     }

from fastapi import FastAPI

from api.routes.upload import router as upload_router
from api.routes.chat import router as chat_router

app = FastAPI(title="AI Knowledge System")

app.include_router(upload_router)
app.include_router(chat_router)


@app.get("/")
def home():
    return {"message": "AI Knowledge System Running"}