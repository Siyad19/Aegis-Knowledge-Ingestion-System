import json
from pathlib import Path

from src.knowledge.extraction.chunk_knowledge_extraction import (
    extract_knowledge_from_document
)

PROCESSED_DIR = Path("processed/documents")
OUTPUT_DIR = Path("processed/knowledge")


def build_knowledge_base():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    knowledge_base = {
        "documents": [],
        "entities": [],
        "claims": [],
        "requirements": [],
        "relationships": [],
        "warnings": []
    }

    document_files = list(
        PROCESSED_DIR.glob("*.json")
    )

    print(f"Found {len(document_files)} documents.")

    for file_path in document_files:

        print(f"\nProcessing: {file_path.name}")

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            document = json.load(file)

        document_id = document.get(
            "document_id",
            file_path.stem
        )

        filename = document.get(
            "filename",
            file_path.name
        )

        # -------------------------
        # STORE DOCUMENT INFORMATION
        # -------------------------

        knowledge_base["documents"].append({
            "document_id": document_id,
            "filename": filename,
            "file_type": document.get("file_type")
        })

        # -------------------------
        # PROCESS EVERY TEXT CHUNK
        # -------------------------

        for chunk in document.get("content", []):

            text = chunk.get("text", "").strip()

            if not text:
                continue

            location = chunk.get(
                "location",
                {}
            )

            # Provenance comes from the
            # original document, not the LLM
            provenance = {
                "document_id": document_id,
                "filename": filename,
                "location": location
            }

            # -------------------------
            # KNOWLEDGE EXTRACTION
            # -------------------------

            try:

                result = extract_knowledge_from_document(text)

            except Exception as e:

                print(
                    f"Knowledge extraction failed: "
                    f"{filename} | {location} | {e}"
                )

                result = {
                    "entities": [],
                    "claims": [],
                    "requirements": [],
                    "relationships": [],
                    "warnings": []
                }

            # -------------------------
            # ENTITIES
            # -------------------------

            for entity in result.get(
                "entities",
                []
            ):

                entity["provenance"] = provenance

                knowledge_base["entities"].append(
                    entity
                )

            # -------------------------
            # CLAIMS
            # -------------------------

            for claim in result.get(
                "claims",
                []
            ):

                claim["provenance"] = provenance

                knowledge_base["claims"].append(
                    claim
                )

            # -------------------------
            # REQUIREMENTS
            # -------------------------

            for requirement in result.get(
                "requirements",
                []
            ):

                requirement["provenance"] = provenance

                knowledge_base["requirements"].append(
                    requirement
                )

            # -------------------------
            # RELATIONSHIPS
            # -------------------------

            for relationship in result.get(
                "relationships",
                []
            ):

                relationship["provenance"] = provenance

                knowledge_base["relationships"].append(
                    relationship
                )

            # -------------------------
            # WARNINGS
            # -------------------------

            for warning in result.get(
                "warnings",
                []
            ):

                warning["provenance"] = provenance

                knowledge_base["warnings"].append(
                    warning
                )

    # -------------------------
    # EXTRACTION SUMMARY
    # -------------------------

    print("\nExtraction summary:")

    print(
        f"Entities: "
        f"{len(knowledge_base['entities'])}"
    )

    print(
        f"Claims: "
        f"{len(knowledge_base['claims'])}"
    )

    print(
        f"Requirements: "
        f"{len(knowledge_base['requirements'])}"
    )

    print(
        f"Relationships: "
        f"{len(knowledge_base['relationships'])}"
    )

    print(
        f"Warnings: "
        f"{len(knowledge_base['warnings'])}"
    )

    # -------------------------
    # SAVE KNOWLEDGE BASE
    # -------------------------

    output_file = OUTPUT_DIR / "knowledge_base.json"

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            knowledge_base,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(
        "\nKnowledge base created successfully."
    )

    print(
        f"Saved to: {output_file}"
    )


if __name__ == "__main__":
    build_knowledge_base()