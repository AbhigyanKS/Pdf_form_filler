from pypdf import PdfReader

def list_pdf_fields(pdf_path):
    """Return all form field names in the PDF."""
    reader = PdfReader(pdf_path)
    fields = reader.get_fields()
    return list(fields.keys()) if fields else []


import fitz  # PyMuPDF
import json
import os

# Map PyMuPDF field type integers → human-readable
FIELD_TYPE_MAP = {
    fitz.PDF_WIDGET_TYPE_TEXT: "text",
    fitz.PDF_WIDGET_TYPE_CHECKBOX: "checkbox",
    fitz.PDF_WIDGET_TYPE_RADIOBUTTON: "radio",
    fitz.PDF_WIDGET_TYPE_COMBOBOX: "combobox",
    fitz.PDF_WIDGET_TYPE_LISTBOX: "listbox",
    fitz.PDF_WIDGET_TYPE_SIGNATURE: "signature",
}

def analyze_pdf_fields(input_pdf, output_json=None):
    """
    Analyze PDF form fields and export a JSON schema describing them.
    """
    doc = fitz.open(input_pdf)
    field_info = {}

    for page_num, page in enumerate(doc, start=1):
        widget = page.first_widget
        while widget:
            field_name = widget.field_name or f"unnamed_{page_num}"
            field_type = FIELD_TYPE_MAP.get(widget.field_type, "unknown")

            field_entry = {
                "type": field_type,
                "page": page_num,
                "default": widget.field_value,
            }

            # Add possible choices for dropdowns, radios, checkboxes
            if widget.field_type in (fitz.PDF_WIDGET_TYPE_COMBOBOX, fitz.PDF_WIDGET_TYPE_LISTBOX):
                field_entry["options"] = widget.choice_values
            elif widget.field_type in (fitz.PDF_WIDGET_TYPE_RADIOBUTTON, fitz.PDF_WIDGET_TYPE_CHECKBOX):
                # PyMuPDF doesn’t directly expose “on states”, so we infer
                field_entry["options"] = ["Yes", "Off"]

            field_info[field_name] = field_entry
            widget = widget.next

    doc.close()

    # Save JSON if requested
    if output_json:
        os.makedirs(os.path.dirname(output_json), exist_ok=True)
        with open(output_json, "w") as f:
            json.dump(field_info, f, indent=2)

    return field_info
