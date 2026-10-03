import json

KB_PATH = "processed/knowledge/knowledge_base.json"

IMPORTANT_TERMS = [
    "PS-04",
    "PS-04A",
    "PS-40",
    "A17",
    "IV-21",
    "ECN-1058",
    "AEG-CR-700",
    "3.2",
    "150 bar",
    "200 bar"
]


def validate_content():
    with open(KB_PATH, "r", encoding="utf-8") as file:
        kb = json.load(file)

    print("=== CONTENT VALIDATION ===")

    all_text = json.dumps(
        kb,
        ensure_ascii=False
    ).lower()

    for term in IMPORTANT_TERMS:

        if term.lower() in all_text:
            print(f"[FOUND] {term}")
        else:
            print(f"[MISSING] {term}")


if __name__ == "__main__":
    validate_content()