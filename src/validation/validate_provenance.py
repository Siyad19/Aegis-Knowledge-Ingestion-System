import json

KB_PATH = "processed/knowledge/knowledge_base.json"


def validate_provenance():
    with open(KB_PATH, "r", encoding="utf-8") as file:
        kb = json.load(file)

    print("=== PROVENANCE VALIDATION ===")

    for item_type in ["entities", "claims", "relationships"]:

        items = kb[item_type]
        missing = 0

        for item in items:
            if "provenance" not in item:
                missing += 1

        if missing == 0:
            print(f"[OK] {item_type}: all items have provenance")
        else:
            print(
                f"[WARNING] {item_type}: "
                f"{missing} items missing provenance"
            )


if __name__ == "__main__":
    validate_provenance()