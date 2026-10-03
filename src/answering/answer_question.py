import json

from llm.model import get_llm
from src.retrieval.retriever import hybrid_search
from prompts.answer_question_prompt import get_answer_question_prompt


# ============================================================
# SOURCE DEDUPLICATION
# ============================================================

def deduplicate_sources(sources):

    unique_sources = []
    seen = set()

    for source in sources:

        filename = source.get(
            "filename",
            "Unknown"
        )

        location = source.get(
            "location",
            "Unknown"
        )

        location_key = json.dumps(
            location,
            sort_keys=True,
            ensure_ascii=False
        )

        key = (
            filename,
            location_key
        )

        if key not in seen:

            seen.add(key)

            unique_sources.append({
                "filename": filename,
                "location": location
            })

    return unique_sources


# ============================================================
# ANSWER QUESTION
# ============================================================

def answer_question(question):

    # --------------------------------------------------------
    # Retrieve evidence
    # --------------------------------------------------------

    results = hybrid_search(
        question,
        top_k=10
    )

    # --------------------------------------------------------
    # No evidence
    # --------------------------------------------------------

    if not results:

        return {
            "answer": (
                "The available documentation does not "
                "provide enough evidence to answer this question."
            ),
            "evidence": [],
            "conflicts": [],
            "uncertainty": [
                "The answer cannot be established from "
                "the available documentation."
            ],
            "gaps": [
                "No relevant evidence was found."
            ]
        }

    # --------------------------------------------------------
    # Build evidence text
    # --------------------------------------------------------

    evidence = ""

    for number, result in enumerate(
        results,
        start=1
    ):

        item = result["item"]

        evidence += f"""
Evidence {number}:

Knowledge type:
{result["type"]}

Retrieval method:
{result["method"]}

Retrieval score:
{result["score"]}

Knowledge item:
{json.dumps(
    item,
    ensure_ascii=False,
    indent=2
)}
"""

    # --------------------------------------------------------
    # Create answer prompt
    # --------------------------------------------------------

    prompt = get_answer_question_prompt(
        question,
        evidence
    )

    # --------------------------------------------------------
    # Call LLM
    # --------------------------------------------------------

    llm = get_llm()

    response = llm.invoke(prompt)

    content = response.content.strip()

    # --------------------------------------------------------
    # Remove markdown JSON fences if returned
    # --------------------------------------------------------

    content = content.replace(
        "```json",
        ""
    )

    content = content.replace(
        "```",
        ""
    )

    content = content.strip()

    # --------------------------------------------------------
    # Parse JSON
    # --------------------------------------------------------

    try:

        result = json.loads(content)

    except json.JSONDecodeError:

        return {
            "answer": (
                "The available evidence could not be "
                "converted into a reliable answer."
            ),
            "evidence": [],
            "conflicts": [],
            "uncertainty": [
                "The answer model did not return valid "
                "structured information."
            ],
            "gaps": []
        }

    # --------------------------------------------------------
    # Ensure required fields exist
    # --------------------------------------------------------

    result.setdefault(
        "answer",
        "The available documentation does not provide enough evidence."
    )

    result.setdefault(
        "evidence",
        []
    )

    result.setdefault(
        "conflicts",
        []
    )

    result.setdefault(
        "uncertainty",
        []
    )

    result.setdefault(
        "gaps",
        []
    )

    # --------------------------------------------------------
    # Return result
    # --------------------------------------------------------

    return result


# ============================================================
# PRINT HELPERS
# ============================================================

def print_section(title):

    print("\n" + "=" * 60)

    print(title)

    print("=" * 60)


# ============================================================
# PRINT ANSWER
# ============================================================

def print_answer(result):

    # --------------------------------------------------------
    # ANSWER
    # --------------------------------------------------------

    print_section("ANSWER")

    print(
        result["answer"]
    )

    # --------------------------------------------------------
    # EVIDENCE
    # --------------------------------------------------------

    print_section("EVIDENCE")

    evidence = result.get(
        "evidence",
        []
    )

    if evidence:

        for item in evidence:

            if isinstance(item, dict):

                statement = item.get(
                    "statement",
                    ""
                )

                filename = item.get(
                    "filename",
                    "Unknown"
                )

                location = item.get(
                    "location",
                    "Unknown"
                )

                print(
                    f"- {statement}"
                )

                print(
                    f"  Source: {filename} — {location}"
                )

            else:

                print(
                    f"- {item}"
                )

    else:

        print("- None")

    # --------------------------------------------------------
    # CONFLICTS
    # --------------------------------------------------------

    print_section("CONFLICTS")

    conflicts = result.get(
        "conflicts",
        []
    )

    if conflicts:

        for item in conflicts:

            print(
                f"- {item}"
            )

    else:

        print("- None identified")

    # --------------------------------------------------------
    # UNCERTAINTY
    # --------------------------------------------------------

    print_section("UNCERTAINTY")

    uncertainty = result.get(
        "uncertainty",
        []
    )

    if uncertainty:

        for item in uncertainty:

            print(
                f"- {item}"
            )

    else:

        print("- None identified")

    # --------------------------------------------------------
    # GAPS
    # --------------------------------------------------------

    print_section("INFORMATION GAPS")

    gaps = result.get(
        "gaps",
        []
    )

    if gaps:

        for item in gaps:

            print(
                f"- {item}"
            )

    else:

        print("- None identified")

    print()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    question = input(
        "Enter your question: "
    )

    result = answer_question(
        question
    )

    print_answer(
        result
    )