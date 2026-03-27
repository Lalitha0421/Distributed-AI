# from pypdf import PdfReader
# import pytesseract
# from pdf2image import convert_from_path

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# POPPLER_PATH = r"C:\Users\DELL\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin"


# def extract_text_from_pdf(file_path):

#     reader = PdfReader(file_path)

#     text = ""

#     for page in reader.pages:
#         page_text = page.extract_text()
#         if page_text:
#             text += page_text

#     if len(text.strip()) < 50:

#         images = convert_from_path(
#             file_path,
#             poppler_path=POPPLER_PATH
#         )

#         for img in images:
#             text += pytesseract.image_to_string(img)

#     return text


import os
from pypdf import PdfReader
from docx import Document
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

# Windows paths - change only if your paths are different
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\Users\DELL\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin"

def extract_text_from_file(file_path: str) -> str:
    """Extract text from PDF, TXT, or DOCX with OCR fallback for scanned PDFs."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    text = ""

    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

    elif ext == ".docx":
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])

    elif ext == ".pdf":
        # Normal text extraction
        reader = PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        # OCR fallback if very little text extracted
        if len(text.strip()) < 100:
            try:
                images = convert_from_path(file_path, poppler_path=POPPLER_PATH)
                for img in images:
                    text += pytesseract.image_to_string(img) + "\n"
            except Exception as e:
                print(f"OCR failed for {file_path}: {e}")
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

    return text.strip()