from pdfminer.high_level import extract_text
from docx import Document

def parse_pdf(file_path):
    text = extract_text(file_path)
    return text


def parse_docx(file_path):
    doc = Document(file_path)
    text = []

    for para in doc.paragraphs:
        text.append(para.text)

    return "\n".join(text)


def parse_document(file_path):

    if file_path.endswith(".pdf"):
        return parse_pdf(file_path)

    if file_path.endswith(".docx"):
        return parse_docx(file_path)

    raise Exception("Unsupported file format")