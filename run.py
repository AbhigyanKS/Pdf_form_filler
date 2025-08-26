from flask import Flask, request, jsonify, send_file
import os
import tempfile
from src.utils import list_pdf_fields
from src.fill_pdf import fill_pdf_from_json

app = Flask(__name__)


@app.route("/fields", methods=["POST"])
def fields():
    """
    Get available form fields from a PDF
    """
    if "pdf" not in request.files:
        return jsonify({"error": "No PDF uploaded"}), 400

    pdf_file = request.files["pdf"]

    # Save PDF temporarily (ensure closed on Windows)
    tmp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    try:
        pdf_file.save(tmp_pdf.name)
        pdf_path = tmp_pdf.name
    finally:
        tmp_pdf.close()

    try:
        fields = list_pdf_fields(pdf_path)
    finally:
        # Safe cleanup
        try:
            os.remove(pdf_path)
        except Exception:
            pass

    return jsonify({"fields": fields})

'''
@app.route("/fill", methods=["POST"])
def fill():
    """
    Fill a PDF using a JSON file and return the filled PDF
    """
    if "pdf" not in request.files or "json" not in request.files:
        return jsonify({"error": "PDF and JSON file required"}), 400

    pdf_file = request.files["pdf"]
    json_file = request.files["json"]

    # Create temporary input files (ensure closed properly on Windows)
    tmp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tmp_json = tempfile.NamedTemporaryFile(delete=False, suffix=".json")

    try:
        pdf_file.save(tmp_pdf.name)
        json_file.save(tmp_json.name)
        pdf_path = tmp_pdf.name
        json_path = tmp_json.name
    finally:
        tmp_pdf.close()
        tmp_json.close()

    # Create output file safely with mkstemp (avoids locking issues on Windows)
    fd, output_path = tempfile.mkstemp(suffix=".pdf")
    os.close(fd)  # Close immediately so it's not locked

    # Fill PDF
    fill_pdf_from_json(pdf_path, output_path, json_path, flatten=True)

    # Cleanup input files
    try:
        os.remove(pdf_path)
    except Exception:
        pass
    try:
        os.remove(json_path)
    except Exception:
        pass

    # Send file back to client
    response = send_file(output_path, as_attachment=True, download_name="filled_form.pdf")

    # Ensure output is deleted after response is sent
    @response.call_on_close
    def cleanup():
        try:
            os.remove(output_path)
        except Exception:
            pass

    return response

'''
@app.route("/fill", methods=["POST"])
def fill():
    """
    Fill a PDF using a JSON file and return the filled PDF
    """
    if "pdf" not in request.files or "json" not in request.files:
        return jsonify({"error": "PDF and JSON file required"}), 400

    pdf_file = request.files["pdf"]
    json_file = request.files["json"]

    # ✅ Keep original names
    upload_dir = tempfile.mkdtemp()
    pdf_path = os.path.join(upload_dir, pdf_file.filename)
    json_path = os.path.join(upload_dir, json_file.filename)

    pdf_file.save(pdf_path)
    json_file.save(json_path)

    # Create output file safely
    fd, output_path = tempfile.mkstemp(suffix=".pdf")
    os.close(fd)

    # Fill PDF
    fill_pdf_from_json(pdf_path, output_path, json_path, flatten=True)

    # Send file back to client
    response = send_file(output_path, as_attachment=True, download_name="filled_form.pdf")

    # Cleanup after response
    @response.call_on_close
    def cleanup():
        try:
            os.remove(pdf_path)
            os.remove(json_path)
            os.remove(output_path)
            os.rmdir(upload_dir)  # remove temp dir
        except Exception:
            pass

    return response

if __name__ == "__main__":
    app.run(debug=True, port=9000)
