from src.utils import list_pdf_fields
from src.fill_pdf import fill_pdf_from_json

input_pdf = "data/e.pdf"
json_file = "data/data.json"
output_pdf = "output/filled_form.pdf"

# Show field names for debugging
print("Available fields in PDF:")
print(list_pdf_fields(input_pdf))

# Fill
#fill_pdf_from_json(input_pdf, output_pdf, json_file)
fill_pdf_from_json("data/e.pdf", "output/filled_form.pdf", "data/data.json", flatten=True)

print(f"Filled PDF saved to: {output_pdf}")
