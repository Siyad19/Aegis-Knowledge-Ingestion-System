import json


def load_json(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    content = []

    def extract(value, path="$"):

        if isinstance(value, dict):

            for key, child in value.items():
                extract(child, f"{path}.{key}")

        elif isinstance(value, list):

            for index, child in enumerate(value):
                extract(child, f"{path}[{index}]")

        else:

            content.append({
                "location": {
                    "json_path": path
                },
                "text": str(value),
                "extraction_method": "json"
            })

    extract(data)

    return content