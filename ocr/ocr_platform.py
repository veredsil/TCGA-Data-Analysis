import argparse
import os
import sys
from pdf2image import convert_from_path
import pytesseract
from docx import Document
from PIL import Image

def pdf_to_docx(pdf_path, docx_path, lang='heb'):
    """
    Converts a PDF containing handwritten/printed text to a DOCX file using OCR.
    """
    if not os.path.exists(pdf_path):
        print(f"Error: The input file {pdf_path} does not exist.")
        sys.exit(1)

    print(f"Loading PDF from {pdf_path}...")
    try:
        # Convert PDF pages to images
        images = convert_from_path(pdf_path)
    except Exception as e:
        print(f"Error converting PDF to images: {e}")
        sys.exit(1)

    print(f"Successfully converted {len(images)} pages to images.")

    # Initialize a new Word document
    document = Document()
    document.add_heading('OCR Output', 0)

    # Process each image page
    for i, image in enumerate(images):
        print(f"Processing page {i + 1}/{len(images)}...")

        # Read text from image using pytesseract
        try:
            # pytesseract takes PIL image directly
            text = pytesseract.image_to_string(image, lang=lang)

            if text.strip():
                document.add_paragraph(f"--- Page {i + 1} ---")
                document.add_paragraph(text)
            else:
                document.add_paragraph(f"--- Page {i + 1} ---")
                document.add_paragraph("[No text detected]")

        except Exception as e:
            print(f"Error processing OCR on page {i + 1}: {e}")
            document.add_paragraph(f"--- Page {i + 1} ---")
            document.add_paragraph(f"[Error processing page: {e}]")

    # Save the resulting DOCX file
    print(f"Saving extracted text to {docx_path}...")
    try:
        document.save(docx_path)
        print("Success!")
    except Exception as e:
        print(f"Error saving DOCX file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF with handwritten text in Hebrew to a DOCX file with printed text.")
    parser.add_argument("input_pdf", help="Path to the input PDF file.")
    parser.add_argument("output_docx", help="Path to the output DOCX file.")
    parser.add_argument("--lang", default="heb", help="Language code for OCR (default: 'heb').")

    args = parser.parse_args()

    pdf_to_docx(args.input_pdf, args.output_docx, args.lang)
