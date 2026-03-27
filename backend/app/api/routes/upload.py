# from fastapi import APIRouter, UploadFile, File
# import shutil
# import os

# from services.document_processor import extract_text_from_pdf
# from services.text_chunker import split_text_into_chunks
# from services.vector_store import store_chunks

# router = APIRouter()

# UPLOAD_FOLDER = "../data"


# @router.post("/upload")
# def upload_document(file: UploadFile = File(...)):

#     file_location = os.path.join(UPLOAD_FOLDER, file.filename)

#     with open(file_location, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     extracted_text = extract_text_from_pdf(file_location)

#     chunks = split_text_into_chunks(extracted_text)

#     stored = store_chunks(chunks, file.filename)

#     return {
#     "message": "File uploaded successfully",
#     "characters_extracted": len(extracted_text),
#     "chunks_created": len(chunks),
#     "chunks_stored": stored
# }


from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
from app.services.document_processor import extract_text_from_file
from app.services.text_chunker import split_text_into_chunks
from app.services.vector_store import store_chunks
from app.core.logger import logger

router = APIRouter(prefix="/upload")

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "../../data")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/")
async def upload_document(file: UploadFile = File(...)):
    allowed_extensions = {'.pdf', '.txt', '.docx'}
    file_ext = os.path.splitext(file.filename)[1].lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail="Only PDF, TXT, and DOCX files are allowed"
        )

    file_location = os.path.join(UPLOAD_FOLDER, file.filename)

    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"File saved: {file.filename}")

        extracted_text = extract_text_from_file(file_location)
        chunks = split_text_into_chunks(extracted_text)

        stored_count = store_chunks(chunks, document_name=file.filename)

        logger.info(f"Successfully processed {file.filename}: {len(chunks)} chunks stored")

        return {
            "message": "Document uploaded and processed successfully",
            "filename": file.filename,
            "characters_extracted": len(extracted_text),
            "chunks_created": len(chunks),
            "chunks_stored": stored_count
        }

    except Exception as e:
        logger.error(f"Upload/processing failed for {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")