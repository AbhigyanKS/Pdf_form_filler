import fitz  # PyMuPDF

pdf_path = r"C:\Users\Abhigyan tripathi\Downloads\Renewal PP_ds82.pdf"


def list_checkboxes(pdf_path):
    doc = fitz.open(pdf_path)
    for page_num, page in enumerate(doc, start=1):
        for widget in page.widgets():
            if widget.field_type == fitz.PDF_WIDGET_TYPE_CHECKBOX:
                print(
                    f"Page {page_num} | Field: {widget.field_name} | "
                    f"Value: {widget.field_value} | "
                    f"Possible states: {widget.button_states()}"
                )
    doc.close()

if __name__ == "__main__":
    list_checkboxes(pdf_path)   # replace with your file
