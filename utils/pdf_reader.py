import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_data: bytes) -> str:
    with fitz.open(stream=pdf_data, filetype="pdf") as doc:
        return "\n".join(page.get_text() for page in doc)
