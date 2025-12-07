import os
import io
import base64
from PyPDF2 import PdfReader
import fitz  # PyMuPDF

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

# Convert PDF to images and return each page as bytes


def pdf_to_images(pdf_path) -> list:

    doc = fitz.open(pdf_path)
    images = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=300)
        img_bytes = pix.tobytes("png")
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")
        images.append(
            {
                "page_num": page_num+1,
                "bytes": img_bytes,
                "base64": img_base64
            })
    return images


if __name__ == "__main__":

    doc = fitz.open("453-3633210941.pdf")
    base_name = os.path.splitext(os.path.basename("453-3633210941.pdf"))[0]
    image_paths = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=300)
        image_filename = f"{base_name}_page_{page_num+1}.png"
        image_path = os.path.join("documents/images", image_filename)
        pix.save(image_path)
        image_paths.append(image_path)
