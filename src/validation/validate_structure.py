import json

KB_PATH = "processed/knowledge/knowledge_base.json"


def validate_structure():
    with open(KB_PATH, "r", encoding="utf-8") as file:
        kb = json.load(file)

    required_keys = [
        "documents",
        "entities",
        "claims",
        "relationships"
    ]

    print("=== STRUCTURE VALIDATION ===")

    for key in required_keys:
        if key in kb:
            print(f"[OK] {key}")
        else:
            print(f"[ERROR] Missing: {key}")

    print("\n=== COUNTS ===")
    print("Documents     :", len(kb["documents"]))
    print("Entities      :", len(kb["entities"]))
    print("Claims        :", len(kb["claims"]))
    print("Relationships :", len(kb["relationships"]))


if __name__ == "__main__":
    validate_structure()