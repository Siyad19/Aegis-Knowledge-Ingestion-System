from pathlib import Path

import pytesseract
from PIL import Image


def load_image(file_path):

    file_path = Path(file_path)

    image = Image.open(file_path)

    text = pytesseract.image_to_string(image).strip()

    return [
        {
            "location": {
                "file": file_path.name
            },
            "text": text,
            "extraction_method": "ocr"
        }
    ]