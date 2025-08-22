from flask import Flask, request, jsonify, send_file
import os
import tempfile
import json

from src.utils import list_pdf_fields ,  analyze_pdf_fields
from src.fill_pdf import fill_pdf, detect_form_type, translate_json_keys , fill_pdf_direct
from src.form_map import FORM_MAPS

app = Flask(__name__)

@app.route("/fill_direct", methods=["POST"])
def fill_direct():
    """
    Fill a PDF form using uploaded JSON data directly,
    without mapping. JSON keys must match PDF field names.
    """
    if "pdf" not in request.files or "json" not in request.files:
        return jsonify({"error": "PDF and JSON file required"}), 400

    pdf_file = request.files["pdf"]
    json_file = request.files["json"]

    tmp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tmp_json = tempfile.NamedTemporaryFile(delete=False, suffix=".json")

    try:
        pdf_file.save(tmp_pdf.name)
        json_file.save(tmp_json.name)
    finally:
        tmp_pdf.close()
        tmp_json.close()

    # Load user JSON
    with open(tmp_json.name, "r") as f:
        user_data = json.load(f)

    # Create output file
    fd, output_path = tempfile.mkstemp(suffix=".pdf")
    os.close(fd)

    # Directly fill the PDF
    fill_pdf_direct(tmp_pdf.name, output_path, user_data, flatten=True)

    response = send_file(output_path, as_attachment=True, download_name="filled_form.pdf")

    @response.call_on_close
    def cleanup():
        # cleanup temp files AFTER response is sent
        for f in (tmp_pdf.name, tmp_json.name, output_path):
            try:
                os.remove(f)
            except Exception:
                pass

    return response


@app.route("/fields", methods=["POST"])
def fields():
    """
    Get available form fields from a PDF
    """
    if "pdf" not in request.files:
        return jsonify({"error": "No PDF uploaded"}), 400

    pdf_file = request.files["pdf"]

    tmp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    try:
        pdf_file.save(tmp_pdf.name)
        pdf_path = tmp_pdf.name
    finally:
        tmp_pdf.close()

    try:
        fields = list_pdf_fields(pdf_path)
    finally:
        try:
            os.remove(pdf_path)
        except Exception:
            pass

    return jsonify({"fields": fields})


@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Analyze a PDF and return field names, types, and options (clean JSON schema).
    """
    if "pdf" not in request.files:
        return jsonify({"error": "No PDF uploaded"}), 400

    pdf_file = request.files["pdf"]

    tmp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    try:
        pdf_file.save(tmp_pdf.name)
        pdf_path = tmp_pdf.name
    finally:
        tmp_pdf.close()

    try:
        schema = analyze_pdf_fields(pdf_path)   # ✅ call your utils function
    finally:
        try:
            os.remove(pdf_path)
        except Exception:
            pass

    return jsonify({"schema": schema})

@app.route("/fill", methods=["POST"])
def fill():
    """
    Fill a PDF form using uploaded JSON data
    """
    if "pdf" not in request.files or "json" not in request.files:
        return jsonify({"error": "PDF and JSON file required"}), 400

    pdf_file = request.files["pdf"]
    json_file = request.files["json"]

    tmp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tmp_json = tempfile.NamedTemporaryFile(delete=False, suffix=".json")

    try:
        pdf_file.save(tmp_pdf.name)
        json_file.save(tmp_json.name)
    finally:
        tmp_pdf.close()
        tmp_json.close()

    # Load user JSON
    with open(tmp_json.name, "r") as f:
        raw_data = json.load(f)

    # 1. Detect form type (CA, NY, Passport…)
    try:
        form_type = detect_form_type(raw_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # 2. Pick correct field map
    field_map = FORM_MAPS[form_type]

    # 3. Translate user JSON → PDF fields
    mapped_data = translate_json_keys(raw_data, field_map)

    # 4. Create output file
    fd, output_path = tempfile.mkstemp(suffix=".pdf")
    os.close(fd)

    fill_pdf(tmp_pdf.name, output_path, mapped_data, flatten=True)

    response = send_file(output_path, as_attachment=True, download_name="filled_form.pdf")

    @response.call_on_close
    def cleanup():
        # cleanup temp files AFTER response is sent
        for f in (tmp_pdf.name, tmp_json.name, output_path):
            try:
                os.remove(f)
            except Exception:
                pass

    return response


if __name__ == "__main__":
    app.run(debug=True, port=9000)
