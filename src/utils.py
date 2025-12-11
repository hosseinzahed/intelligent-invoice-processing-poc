import os
import base64
from PyPDF2 import PdfReader  # PyPDF2 is used to read PDF files
import fitz  # PyMuPDF is used to convert PDF pages to images
import numpy as np
import base64
from typing import Union


def get_pdf_page_count(pdf_path: str) -> Union[int, None]:
    """ Returns the number of pages in a PDF file, or 
        None if the file cannot be read. 

    Args:
        pdf_path (str): The path to the PDF file.
    Returns:
        Union[int, None]: The number of pages in the PDF,
                          or None if the file cannot be read.
    """

    try:
        reader = PdfReader(pdf_path)
        return len(reader.pages)
    except Exception:
        return None


def load_invoices(folder_path: str):
    """ Load invoice files from a folder and return a 
        list of dictionaries with file information. 
        Each dictionary contains the file name, size in KB, 
        number of pages (if applicable).
    Args:
        folder_path (str): The path to the folder containing invoice files.
    Returns:
        list: A list of dictionaries with file information.
    """

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
                    "Pages": pages
                })
    return invoice_records


def pdf_to_images(pdf_path: str) -> list:
    """ Convert PDF to images and return each page as 
    bytes and base64 strings. 
    Args:
        pdf_path (str): The path to the PDF file.
    Returns:
        list: A list of dictionaries containing page number,
              bytes, and base64 strings for each page.
    """

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
