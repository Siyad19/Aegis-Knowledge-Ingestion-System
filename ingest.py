import json
from pathlib import Path

from src.ingestion.ingestion_pipeline import ingest_dataset


INPUT_DIR = Path("data/aegis-dataset")
OUTPUT_DIR = Path("processed/documents")


def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    documents = ingest_dataset(INPUT_DIR)

    for document in documents:

        output_file = (
            OUTPUT_DIR /
            f"{document['document_id']}.json"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                document,
                file,
                indent=2,
                ensure_ascii=False
            )

        print(
            f"Saved: {output_file}"
        )

    print("\nIngestion completed.")
    print(f"Documents processed: {len(documents)}")


if __name__ == "__main__":
    main()