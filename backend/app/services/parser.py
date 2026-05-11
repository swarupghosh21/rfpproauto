import os
import PyPDF2

from app.services.textract_service import extract_text_from_pdf


def parse_pdf(path):
    # If enabled, use AWS Textract (best for scanned PDFs).
    use_textract = os.getenv("USE_TEXTRACT", "").lower() in {"1", "true", "yes"}
    if use_textract:
        return extract_text_from_pdf(path)

    # Fallback: local PDF text extraction (best for digital PDFs).
    text = ""
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""

    return text