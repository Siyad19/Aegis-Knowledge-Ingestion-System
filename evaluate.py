import csv
import json
import time
from pathlib import Path

from src.answering.answer_question import answer_question


# --------------------------------------------------
# FILE PATHS
# --------------------------------------------------

QUESTIONS_FILE = Path(
    "evaluation/evaluation_questions.csv"
)

RESULTS_FILE = Path(
    "evaluation/evaluation_results.json"
)


# --------------------------------------------------
# LOAD QUESTIONS
# --------------------------------------------------

with open(
    QUESTIONS_FILE,
    "r",
    encoding="utf-8-sig",
    newline=""
) as file:

    questions = list(
        csv.DictReader(file)
    )


print("=" * 60)
print("AEGIS KNOWLEDGE BASE EVALUATION")
print("=" * 60)

print(
    f"\nFound {len(questions)} evaluation questions."
)


# --------------------------------------------------
# RUN QUESTIONS
# --------------------------------------------------

results = []

for index, item in enumerate(questions, start=1):

    question_id = item["question_id"]
    question = item["question"]

    print("\n" + "-" * 60)
    print(
        f"{question_id} "
        f"({index}/{len(questions)})"
    )
    print(question)

    start_time = time.perf_counter()

    try:

        # Run your existing QA system
        output = answer_question(question)

        elapsed = time.perf_counter() - start_time

        result = {
            "question_id": question_id,
            "question": question,

            "system_answer": output.get(
                "answer",
                ""
            ),

            "evidence": output.get(
                "evidence",
                []
            ),

            "conflicts": output.get(
                "conflicts",
                []
            ),

            "uncertainty": output.get(
                "uncertainty",
                []
            ),

            "gaps": output.get(
                "gaps",
                []
            ),

            "latency_seconds": round(
                elapsed,
                2
            ),

            "error": None
        }

    except Exception as e:

        elapsed = time.perf_counter() - start_time

        result = {
            "question_id": question_id,
            "question": question,

            "system_answer": "",

            "evidence": [],

            "conflicts": [],

            "uncertainty": [],

            "gaps": [],

            "latency_seconds": round(
                elapsed,
                2
            ),

            "error": str(e)
        }

    results.append(result)

    # --------------------------------------------------
    # PRINT RESULT
    # --------------------------------------------------

    print("\nANSWER:")
    print(result["system_answer"])

    print("\nEVIDENCE:")

    for evidence in result["evidence"]:

        if isinstance(evidence, dict):

            print(
                f"- {evidence.get('statement', '')}"
            )

            print(
                f"  Source: "
                f"{evidence.get('filename', '')}"
            )

            print(
                f"  Location: "
                f"{evidence.get('location', '')}"
            )

        else:

            print(f"- {evidence}")

    if result["conflicts"]:

        print("\nCONFLICTS:")

        for conflict in result["conflicts"]:
            print(f"- {conflict}")

    if result["uncertainty"]:

        print("\nUNCERTAINTY:")

        for uncertainty in result["uncertainty"]:
            print(f"- {uncertainty}")

    if result["gaps"]:

        print("\nINFORMATION GAPS:")

        for gap in result["gaps"]:
            print(f"- {gap}")

    print(
        f"\nLatency: "
        f"{result['latency_seconds']} seconds"
    )


# --------------------------------------------------
# SAVE RESULTS
# --------------------------------------------------

RESULTS_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

with open(
    RESULTS_FILE,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        results,
        file,
        indent=2,
        ensure_ascii=False
    )


# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

successful = sum(
    1
    for result in results
    if result["error"] is None
)

failed = len(results) - successful

average_latency = (
    sum(
        result["latency_seconds"]
        for result in results
    ) / len(results)
    if results
    else 0
)

print("\n" + "=" * 60)
print("EVALUATION COMPLETE")
print("=" * 60)

print(
    f"Total questions : {len(results)}"
)

print(
    f"Successful      : {successful}"
)

print(
    f"Failed          : {failed}"
)

print(
    f"Average latency : "
    f"{average_latency:.2f} seconds"
)

print(
    f"\nResults saved to:"
    f"\n{RESULTS_FILE}"
)