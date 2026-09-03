import fitz


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from all pages of a PDF using PyMuPDF.

    Args:
        file_path: Path to the PDF file.

    Returns:
        Extracted and cleaned text from the PDF.
    """

    extracted_text = []

    with fitz.open(file_path) as document:
        for page in document:
            page_text = page.get_text()

            if page_text:
                extracted_text.append(page_text)

    return "\n".join(extracted_text).strip()