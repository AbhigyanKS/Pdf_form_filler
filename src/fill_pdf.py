import fitz  # PyMuPDF
import os
import json
from datetime import datetime
from .form_map import FORM_MAPS   


def detect_form_type(user_data):
    """Decide which field map to use based on JSON keys/values."""
    if user_data.get("dlStateCountry", "").lower() == "california":
        return "CA_DL"
    elif user_data.get("dlStateCountry", "").lower() == "ny":
        return "NY_DL"
    elif "passportNumber" in user_data:
        return "PASSPORT"
    elif "first_name" in user_data or "Selection" in user_data:
        # DS-11 style passport application
        return "PASSPORT_DS11"
    else:
        raise ValueError("❌ Unknown form type: cannot detect mapping")


def translate_json_keys(user_data, field_map):
    """
    Translate user JSON keys → PDF field names for both text and choice fields.
    """
    translated = {}

    # 1️⃣ Text fields
    for key, value in user_data.items():
        if key in field_map.get("text", {}):
            translated[field_map["text"][key]] = value

    # 2️⃣ Choice fields (checkbox, radio, dropdown)
    for pdf_field, json_key in field_map.get("choice", {}).items():
        if json_key in user_data:
            translated[pdf_field] = user_data[json_key]

    return translated



def fill_pdf(input_pdf, output_pdf, data, flatten=False):
    """Fill PDF form with translated data"""
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    doc = fitz.open(input_pdf)

    for page in doc:
        widget = page.first_widget
        while widget:
            print("DEBUG:", widget.field_name, widget.field_type, widget.field_value, widget.choice_values)

            if widget.field_name in data:
                try:
                    value = data[widget.field_name]

                    # Format dates if needed
                    if isinstance(value, str) and "date" in widget.field_name.lower():
                        try:
                            value = datetime.strptime(value, "%Y-%m-%d").strftime("%m/%d/%Y")
                        except Exception:
                            pass

                    if widget.field_type == fitz.PDF_WIDGET_TYPE_TEXT:
                        widget.field_value = str(value)
                    elif widget.field_type == fitz.PDF_WIDGET_TYPE_CHECKBOX:
    # Most forms use "Yes"/"Off", but sometimes it's "On"/"Off"
                       on_value = "Yes"
                       off_value = "Off"

    # If it's currently unset, check possible values
                       if widget.field_value not in (on_value, off_value, None):
        # fallback if PDF uses "On"/"Off"
                        on_value = "On"
                        off_value = "Off"

                       if str(value).lower() in ("yes", "true", "1", on_value.lower()):
                          widget.field_value = on_value
                          
                       else:
                          widget.field_value = off_value


                    elif widget.field_type == fitz.PDF_WIDGET_TYPE_RADIOBUTTON:
                      widget.field_value = str(value)  
                    elif widget.field_type == fitz.PDF_WIDGET_TYPE_COMBOBOX:
                        options = widget.choice_values
                        if str(value) in options:
                            widget.field_value = str(value)
                    elif widget.field_type == fitz.PDF_WIDGET_TYPE_LISTBOX:
                        options = widget.choice_values
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


def fill_pdf_from_json(input_pdf, output_pdf, json_file, flatten=False):
    """Main entry: fill a PDF given a JSON file and auto-selected field map"""
    with open(json_file, "r") as f:
        user_data = json.load(f)

    # 1. Detect form type
    form_type = detect_form_type(user_data)
    print(f"✅ Detected form type: {form_type}")

    # 2. Pick correct map
    field_map = FORM_MAPS[form_type]

    # 3. Translate JSON keys → PDF field names
    form_data = translate_json_keys(user_data, field_map)

    # 4. Fill PDF
    fill_pdf(input_pdf, output_pdf, form_data, flatten)




import os
from datetime import datetime
import fitz  # PyMuPDF

def fill_pdf_direct(input_pdf, output_pdf, user_data, flatten=False):
    """
    Fill a PDF form using the JSON keys as PDF field names directly,
    without any mapping. Fully debug-ready.
    Handles text, checkboxes, radio buttons, combo/list boxes.
    """
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)

    # Open PDF
    doc = fitz.open(input_pdf)

    # Iterate pages
    for page_number, page in enumerate(doc, start=1):
        widget = page.first_widget
        while widget:
            field_name = widget.field_name
            value = user_data.get(field_name)

            # Debug info
            print(f"\nDEBUG PAGE {page_number}: Field '{field_name}'")
            print(f"  Type: {widget.field_type}")
            print(f"  Current value: {widget.field_value}")
            if hasattr(widget, "choice_values"):
                print(f"  Choice values: {widget.choice_values}")
            print(f"  User JSON value: {value}")

            if value is not None:
                try:
                    # Format dates automatically if field name contains 'date'
                    if isinstance(value, str) and "date" in field_name.lower():
                        try:
                            value = datetime.strptime(value, "%Y-%m-%d").strftime("%m/%d/%Y")
                        except Exception:
                            pass

                    # Fill based on widget type
                    if widget.field_type == fitz.PDF_WIDGET_TYPE_TEXT:
                        widget.field_value = str(value)
                        print(f"  ✅ Filled TEXT with '{value}'")

                    elif widget.field_type == fitz.PDF_WIDGET_TYPE_CHECKBOX:
    # Get actual PDF checkbox options
                      choices = getattr(widget, "choice_values", ["Yes", "Off"])

    # Decide what value to tick
                      if str(value).lower() in ("yes", "true", "1"):
        # Pick first option that is NOT "Off" (usually the "checked" value)
                        widget.field_value = next((c for c in choices if c.lower() != "off"), choices[0])
                      else:
        # Pick the "off" value
                       widget.field_value = next((c for c in choices if c.lower() == "off"), choices[0])

                       widget.update()


                    elif widget.field_type == fitz.PDF_WIDGET_TYPE_RADIOBUTTON:
                        choices = getattr(widget, "choice_values", [])
                        if str(value) in choices:
                            widget.field_value = str(value)
                        elif str(value).lower() in [c.lower() for c in choices]:
                            widget.field_value = next(c for c in choices if c.lower() == str(value).lower())
                        else:
                            if choices:
                                widget.field_value = choices[0]  # fallback
                        print(f"  ✅ Filled RADIOBUTTON with '{widget.field_value}'")

                    elif widget.field_type in (fitz.PDF_WIDGET_TYPE_COMBOBOX,
                                               fitz.PDF_WIDGET_TYPE_LISTBOX):
                        choices = getattr(widget, "choice_values", [])
                        if str(value) in choices:
                            widget.field_value = str(value)
                            print(f"  ✅ Filled COMBO/LISTBOX with '{widget.field_value}'")

                    # Update widget
                    widget.update()

                except Exception as e:
                    print(f"⚠️ Skipping widget '{field_name}': {e}")

            # Move to next widget
            widget = widget.next

    # Save the PDF
    temp_output = output_pdf + ".tmpout.pdf"
    doc.save(temp_output, deflate=True, clean=True)
    doc.close()
    os.replace(temp_output, output_pdf)
    print(f"\n✅ PDF filled successfully at {output_pdf}")



