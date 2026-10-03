from pathlib import Path

from .pdf_loader import load_pdf
from .docx_loader import load_docx
from .xlsx_loader import load_xlsx
from .html_loader import load_html
from .json_loader import load_json
from .pptx_loader import load_pptx
from .image_loader import load_image


def load_file(file_path):

    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        return load_pdf(file_path)

    elif suffix == ".docx":
        return load_docx(file_path)

    elif suffix == ".xlsx":
        return load_xlsx(file_path)

    elif suffix == ".html":
        return load_html(file_path)

    elif suffix == ".json":
        return load_json(file_path)

    elif suffix == ".pptx":
        return load_pptx(file_path)

    elif suffix in [".png", ".jpg", ".jpeg"]:
        return load_image(file_path)

    else:
        raise ValueError(
            f"Unsupported file type: {suffix}"
        )


def ingest_dataset(input_directory):

    input_directory = Path(input_directory)

    documents = []

    for file_path in input_directory.rglob("*"):

        if not file_path.is_file():
            continue

        print(f"Processing: {file_path}")

        try:

            content = load_file(file_path)

            document = {
                "document_id": file_path.stem,
                "filename": file_path.name,
                "file_type": file_path.suffix.lower(),
                "relative_path": str(
                    file_path.relative_to(input_directory)
                ),
                "content": content
            }

            documents.append(document)

        except Exception as error:

            print(
                f"ERROR processing {file_path}: {error}"
            )

    return documents