from flask import Flask, request, jsonify, send_file
import os
from src.utils import list_pdf_fields
from src.fill_pdf import fill_pdf_from_json

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/fields", methods=["POST"])
def fields():
    """
    Get available form fields from a PDF
    """
    if "pdf" not in request.files:
        return jsonify({"error": "No PDF uploaded"}), 400

    pdf_file = request.files["pdf"]
    pdf_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
    pdf_file.save(pdf_path)

    fields = list_pdf_fields(pdf_path)
    return jsonify({"fields": fields})


@app.route("/fill", methods=["POST"])
def fill():
    """
    Fill a PDF using a JSON file and return the filled PDF
    """
    if "pdf" not in request.files or "json" not in request.files:
        return jsonify({"error": "PDF and JSON file required"}), 400

    pdf_file = request.files["pdf"]
    json_file = request.files["json"]

    pdf_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
    json_path = os.path.join(UPLOAD_FOLDER, json_file.filename)
    output_path = os.path.join(OUTPUT_FOLDER, f"filled_{pdf_file.filename}")

    pdf_file.save(pdf_path)
    json_file.save(json_path)

    # Use your existing function
    fill_pdf_from_json(pdf_path, output_path, json_path, flatten=True)

    return send_file(output_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, port=9000)
