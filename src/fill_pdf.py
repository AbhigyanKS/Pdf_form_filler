import fitz  # PyMuPDF
import os
import json
from datetime import datetime

# -------------------------
# Mapping of user JSON keys → PDF field names
# Can include dicts for checkbox/radio buttons
# -------------------------
from .field_maps import FIELD_MAPS

def get_field_map(file_path: str):
    """Choose field map based on file name keywords."""
    file_name = os.path.basename(file_path).lower()
    if "passport" in file_name:
        return FIELD_MAPS["passport"]
    elif "ny_license" in file_name or "dl" in file_name:
        return FIELD_MAPS["driver_license"]
    elif "passport_apply" in file_name:
        return FIELD_MAPS["passport_apply"]
    else:
        raise ValueError(f"No field map found for file: {file_name}")




# -------------------------
# PDF Filling Logic
# -------------------------
'''
def fill_pdf(input_pdf, output_pdf, data, flatten=False):
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    doc = fitz.open(input_pdf)

    for page in doc:
        widget = page.first_widget
        while widget:
            if widget.field_name in data:
                try:
                    value = data[widget.field_name]

                    # Format dates automatically if field name contains 'date'
                    if isinstance(value, str) and "date" in widget.field_name.lower():
                        try:
                            value = datetime.strptime(value, "%Y-%m-%d").strftime("%m/%d/%Y")
                        except Exception:
                            pass

                    # Fill based on widget type
                    if widget.field_type == fitz.PDF_WIDGET_TYPE_TEXT:
                        widget.field_value = str(value)
                    elif widget.field_type == fitz.PDF_WIDGET_TYPE_CHECKBOX:
                        print(widget.field_name, "choices:", widget.field_choices, "set to:", widget.field_value)
 
                        choices = widget.field_choices
                        if choices and len(choices) > 0:
                            on_value = choices[0]
                        else:
                            on_value = "Yes"
                        if str(value).lower() in ("yes", "true", "1", "Yes", "checked"):
                            widget.field_value = on_value    
                        else:        
                         widget.field_value = "Off"

                    elif widget.field_type == fitz.PDF_WIDGET_TYPE_RADIOBUTTON:
                        widget.field_value = str(value)
                    elif widget.field_type in (fitz.PDF_WIDGET_TYPE_COMBOBOX, fitz.PDF_WIDGET_TYPE_LISTBOX):
                        options = getattr(widget, "choice_values", [])
                        if str(value) in options:
                            widget.field_value = str(value)

                    widget.update()

                except Exception as e:
                    print(f"⚠️ Skipping widget {widget.field_name}: {e}")

            widget = widget.next

    temp_output = output_pdf + ".tmpout.pdf"
    doc.save(temp_output, deflate=True, clean=True)
    doc.close()
    os.replace(temp_output, output_pdf)
'''


import fitz
import os
from datetime import datetime

def fill_pdf(input_pdf, output_pdf, data, flatten=False):
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    doc = fitz.open(input_pdf)

    seen_radio_groups = set()  # track processed radio groups

    for page_num, page in enumerate(doc, start=1):
        widget = page.first_widget
        while widget:
            if widget.field_name in data:
                try:
                    value = data[widget.field_name]

                    # Auto-format date fields
                    if isinstance(value, str) and "date" in widget.field_name.lower():
                        try:
                            value = datetime.strptime(value, "%Y-%m-%d").strftime("%m/%d/%Y")
                        except Exception:
                            pass

                    # Handle text field
                    if widget.field_type == fitz.PDF_WIDGET_TYPE_TEXT:
                        widget.field_value = str(value)

                    # Handle checkboxes
                    elif widget.field_type == fitz.PDF_WIDGET_TYPE_CHECKBOX:
                        try:
                            choices = getattr(widget, "field_choices", None)
                        except Exception:
                            choices = None

                        on_value = "Yes"
                        if choices and len(choices) > 0:
                            on_value = choices[0]

                        print(f"[Page {page_num}] Checkbox '{widget.field_name}' expects on_value='{on_value}', input='{value}'")

                        if str(value).lower() in ("yes", "true", "1", "checked", "on"):
                            widget.field_value = on_value
                        else:
                            widget.field_value = "Off"

                    # Handle radio buttons
                    elif widget.field_type == fitz.PDF_WIDGET_TYPE_RADIOBUTTON:
                        # skip if group already handled
                        if widget.field_name in seen_radio_groups:
                            widget = widget.next
                            continue

                        options = []
                        try:
                            xref = widget._annot.xref
                            ap_dict = doc.xref_object(xref)
                            if "/AP" in ap_dict and "/N" in ap_dict:
                                import re
                                raw = re.findall(r"/([A-Za-z0-9\.\-]+)\s", ap_dict.split("/N")[1])
                                options = [opt for opt in raw if opt not in ("Off", "Parent", "Rect", "StructParent")]
                        except Exception as e:
                            print(f"⚠️ Could not extract AP states: {e}")

                        print(f"[Page {page_num}] Radio '{widget.field_name}' options={options}, input='{value}'")

                        # decide group value once
                        if value and options and str(value) in options:
                            widget.field_value = str(value)
                        elif options:
                            print(f"⚠️ Input '{value}' not in options {options}, skipping")
                            # if you want default instead of skip, uncomment below:
                            # widget.field_value = options[0]

                        seen_radio_groups.add(widget.field_name)

                    # Handle dropdowns / listboxes
                    elif widget.field_type in (fitz.PDF_WIDGET_TYPE_COMBOBOX, fitz.PDF_WIDGET_TYPE_LISTBOX):
                        options = getattr(widget, "choice_values", [])
                        print(f"[Page {page_num}] Dropdown/Listbox '{widget.field_name}' options={options}, input='{value}'")

                        if str(value) in options:
                            widget.field_value = str(value)
                        else:
                            if options:
                                print(f"⚠️ Input '{value}' not in options, defaulting to '{options[0]}'")
                                widget.field_value = options[0]

                    widget.update()

                except Exception as e:
                    print(f"⚠️ Skipping widget '{widget.field_name}': {e}")

            widget = widget.next

    temp_output = output_pdf + ".tmpout.pdf"
    doc.save(temp_output, deflate=True, clean=True)
    doc.close()
    os.replace(temp_output, output_pdf)

# -------------------------
# JSON → PDF mapping + fill
# -------------------------
def fill_pdf_from_json(input_pdf, output_pdf, json_file, flatten=False):
    
    with open(json_file, "r") as f:
        user_data = json.load(f)

    # Apply mapping: convert user JSON keys → PDF field names
    field_map = get_field_map(input_pdf)
    form_data = {}
    for user_key, value in user_data.items():
        pdf_field = field_map.get(user_key)
        if pdf_field is None:
            continue  # ignore unmapped keys

        # Handle checkbox/radio button mapping
        if isinstance(pdf_field, dict):
            value = pdf_field.get(str(value))
            if value is None:
                continue
            pdf_field = next(iter(pdf_field.values()))  # pick the first as actual field name

        form_data[pdf_field] = value

    # Fill PDF
    fill_pdf(input_pdf, output_pdf, form_data, flatten)



