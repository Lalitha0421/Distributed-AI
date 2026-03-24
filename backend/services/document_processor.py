from pypdf import PdfReader
import pytesseract
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

POPPLER_PATH = r"C:\Users\DELL\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin"


def extract_text_from_pdf(file_path):

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    if len(text.strip()) < 50:

        images = convert_from_path(
            file_path,
            poppler_path=POPPLER_PATH
        )

        for img in images:
            text += pytesseract.image_to_string(img)

    return text