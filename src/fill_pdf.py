import fitz  # PyMuPDF
import os
import json
from datetime import datetime

def fill_pdf(input_pdf, output_pdf, data, flatten=False):
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    doc = fitz.open(input_pdf)

    for page in doc:
        widget = page.first_widget
        while widget:
            if widget.field_name in data:
                try:
                    value = data[widget.field_name]

                    # Format dates if they look like YYYY-MM-DD and field is text
                    if isinstance(value, str) and "date" in widget.field_name.lower():
                        try:
                            value = datetime.strptime(value, "%Y-%m-%d").strftime("%m/%d/%Y")
                        except Exception:
                            pass

                    # TEXT FIELDS
                    if widget.field_type == fitz.PDF_WIDGET_TYPE_TEXT:
                        widget.field_value = str(value)

                    # CHECKBOXES
                    elif widget.field_type == fitz.PDF_WIDGET_TYPE_CHECKBOX:
                        widget.field_value = "Yes" if str(value).lower() in ("yes", "true", "1") else "Off"

                    # RADIO BUTTONS
                    elif widget.field_type == fitz.PDF_WIDGET_TYPE_RADIOBUTTON:
                        widget.field_value = str(value)

                    # DROPDOWNS / COMBOBOXES
                    elif widget.field_type == fitz.PDF_WIDGET_TYPE_COMBOBOX:
                        # Ensure the value is in the available options
                        options = widget.choice_values
                        if str(value) in options:
                            widget.field_value = str(value)
                        else:
                            print(f"Dropdown '{widget.field_name}' value '{value}' not in options {options}")

                    # LIST BOXES
                    elif widget.field_type == fitz.PDF_WIDGET_TYPE_LISTBOX:
                        options = widget.choice_values
                        if str(value) in options:
                            widget.field_value = str(value)
                        else:
                            print(f"Listbox '{widget.field_name}' value '{value}' not in options {options}")

                    widget.update()

                except Exception as e:
                    print(f"Skipping widget {widget.field_name}: {e}")

            widget = widget.next

    temp_output = output_pdf + ".tmpout.pdf"
    doc.save(temp_output, deflate=True, clean=True)
    doc.close()
    os.replace(temp_output, output_pdf)


def fill_pdf_from_json(input_pdf, output_pdf, json_file, flatten=False):
    with open(json_file, "r") as f:
        form_data = json.load(f)
    fill_pdf(input_pdf, output_pdf, form_data, flatten)
