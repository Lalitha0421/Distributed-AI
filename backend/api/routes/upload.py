from fastapi import APIRouter, UploadFile, File
import shutil
import os

from services.document_processor import extract_text_from_pdf
from services.text_chunker import split_text_into_chunks
from services.vector_store import store_chunks

router = APIRouter()

UPLOAD_FOLDER = "../data"


@router.post("/upload")
def upload_document(file: UploadFile = File(...)):

    file_location = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text_from_pdf(file_location)

    chunks = split_text_into_chunks(extracted_text)

    stored = store_chunks(chunks, file.filename)

    return {
    "message": "File uploaded successfully",
    "characters_extracted": len(extracted_text),
    "chunks_created": len(chunks),
    "chunks_stored": stored
}