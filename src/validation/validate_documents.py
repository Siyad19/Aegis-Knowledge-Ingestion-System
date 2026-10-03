import json
from collections import Counter

KB_PATH = "processed/knowledge/knowledge_base.json"


def validate_documents():
    with open(KB_PATH, "r", encoding="utf-8") as file:
        kb = json.load(file)

    print("=== DOCUMENT VALIDATION ===")

    documents = [
        document["filename"]
        for document in kb["documents"]
    ]

    print("Total documents:", len(documents))

    for document in documents:

        entity_count = 0
        claim_count = 0
        relationship_count = 0

        for entity in kb["entities"]:
            if entity.get("provenance", {}).get("filename") == document:
                entity_count += 1

        for claim in kb["claims"]:
            if claim.get("provenance", {}).get("filename") == document:
                claim_count += 1

        for relationship in kb["relationships"]:
            if relationship.get("provenance", {}).get("filename") == document:
                relationship_count += 1

        total = (
            entity_count
            + claim_count
            + relationship_count
        )

        if total == 0:
            print(f"[WARNING] {document}: no extracted knowledge")
        else:
            print(
                f"[OK] {document}: "
                f"{total} items"
            )


if __name__ == "__main__":
    validate_documents()