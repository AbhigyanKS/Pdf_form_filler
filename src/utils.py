from pypdf import PdfReader

def list_pdf_fields(pdf_path):
    """Return all form field names in the PDF."""
    reader = PdfReader(pdf_path)
    fields = reader.get_fields()
    return list(fields.keys()) if fields else []
