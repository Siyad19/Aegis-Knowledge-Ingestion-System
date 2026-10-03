import pymupdf
import pytesseract
from PIL import Image
import io


def load_pdf(file_path):
    document = pymupdf.open(file_path)

    pages = []

    for page_number, page in enumerate(document, start=1):

        text = page.get_text("text").strip()

        # If little/no text exists, try OCR
        if len(text) < 30:
            pix = page.get_pixmap(dpi=200)
            image = Image.open(io.BytesIO(pix.tobytes("png")))
            text = pytesseract.image_to_string(image).strip()

            extraction_method = "ocr"
        else:
            extraction_method = "text"

        pages.append({
            "location": {
                "page": page_number
            },
            "text": text,
            "extraction_method": extraction_method
        })

    document.close()

    return pages