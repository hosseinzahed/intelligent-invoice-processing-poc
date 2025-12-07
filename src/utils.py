import os
from PyPDF2 import PdfReader

# Get the number of pages in a PDF file
def get_pdf_page_count(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        return len(reader.pages)
    except Exception:
        return None

# Load raw invoice files from a folder
def load_raw_invoices(folder_path):
    invoice_records = []
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                size_kb = round(os.path.getsize(file_path) / 1024, 2)
                pages = get_pdf_page_count(
                    file_path) if filename.lower().endswith('.pdf') else None
                invoice_records.append({
                    "Name": filename,
                    "Size (KB)": size_kb,
                    "Pages": pages,
                    "Status": "Unprocessed"
                })
    return invoice_records
