from bs4 import BeautifulSoup


def load_html(file_path):

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        html = file.read()

    soup = BeautifulSoup(html, "html.parser")

    content = []

    for index, element in enumerate(
        soup.find_all(["h1", "h2", "h3", "p", "li", "table"]),
        start=1
    ):

        text = element.get_text(" ", strip=True)

        if text:

            content.append({
                "location": {
                    "element": index,
                    "tag": element.name
                },
                "text": text,
                "extraction_method": "html"
            })

    return content