import fitz  # PyMuPDF

def inspect_pdf_fields(pdf_path):
    """
    Inspect all fields in a PDF form and show their properties.
    """
    doc = fitz.open(pdf_path)
    print(f"\nInspecting PDF: {pdf_path}\n{'='*50}")

    for page_num, page in enumerate(doc, start=1):
        widget = page.first_widget
        while widget:
            field_type_map = {
                fitz.PDF_WIDGET_TYPE_TEXT: "Text",
                fitz.PDF_WIDGET_TYPE_CHECKBOX: "Checkbox",
                fitz.PDF_WIDGET_TYPE_RADIOBUTTON: "RadioButton",
                fitz.PDF_WIDGET_TYPE_COMBOBOX: "ComboBox",
                fitz.PDF_WIDGET_TYPE_LISTBOX: "ListBox",
            }
            field_type = field_type_map.get(widget.field_type, "Unknown")
            
            # Use field_flags instead of flags
            is_read_only = False
            try:
                is_read_only = bool(widget.field_flags & 1)
            except AttributeError:
                pass

            # Try to get possible choices for checkbox/radio/dropdown
            choices = None
            try:
                if field_type in ("Checkbox", "RadioButton"):
                    xref = widget._annot.xref
                    ap_dict = doc.xref_object(xref)
                    import re
                    raw = re.findall(r"/([A-Za-z0-9\.\-]+)\s", ap_dict)
                    choices = [opt for opt in raw if opt not in ("Off", "Parent", "Rect", "StructParent")]
                elif field_type in ("ComboBox", "ListBox"):
                    choices = getattr(widget, "choice_values", [])
            except Exception:
                pass

            print(f"Page {page_num} | Field: {widget.field_name}")
            print(f"  Type       : {field_type}")
            print(f"  Read-Only  : {is_read_only}")
            if choices:
                print(f"  Choices    : {choices}")
            print(f"  Current Val: {widget.field_value}\n")

            widget = widget.next

    doc.close()
    print("✅ Inspection complete.\n")


if __name__ == "__main__":
    pdf_path = input("Enter the PDF path to inspect: ").strip()
    inspect_pdf_fields(pdf_path)
