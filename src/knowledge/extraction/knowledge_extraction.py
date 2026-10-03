import json
import time

from llm.model import get_llm
from prompts.knowledge_extraction_prompt import (
    get_knowledge_extraction_prompt
)


def empty_result():
    return {
        "entities": [],
        "claims": [],
        "requirements": [],
        "relationships": [],
        "warnings": []
    }


def extract_knowledge(text):

    prompt = get_knowledge_extraction_prompt(text)

    llm = get_llm()

    for attempt in range(2):

        try:

            response = llm.invoke(prompt)

            content = response.content

            finish_reason = (
                response.response_metadata.get(
                    "finish_reason"
                )
            )

            print(
                f"    Finish reason: {finish_reason}"
            )

            print(
                f"    Response length: "
                f"{len(content) if content else 0}"
            )

            # --------------------------------
            # INCOMPLETE RESPONSE
            # --------------------------------

            if not content or finish_reason == "length":

                print(
                    "    Incomplete LLM response."
                )

                return empty_result()

            # --------------------------------
            # CLEAN RESPONSE
            # --------------------------------

            content = content.replace(
                "```json",
                ""
            ).replace(
                "```",
                ""
            ).strip()

            # --------------------------------
            # PARSE JSON
            # --------------------------------

            try:

                result = json.loads(content)

                # Make sure all expected categories exist
                return {
                    "entities": result.get(
                        "entities", []
                    ),
                    "claims": result.get(
                        "claims", []
                    ),
                    "requirements": result.get(
                        "requirements", []
                    ),
                    "relationships": result.get(
                        "relationships", []
                    ),
                    "warnings": result.get(
                        "warnings", []
                    )
                }

            except json.JSONDecodeError:

                print(
                    "    Invalid JSON returned by LLM."
                )

                return empty_result()

        except Exception as e:

            if "429" in str(e):

                if attempt == 0:

                    print(
                        "\n    Rate limit reached."
                    )

                    print(
                        "    Waiting 60 seconds..."
                    )

                    time.sleep(60)

                else:

                    print(
                        "    Rate limit still active."
                    )

                    return empty_result()

            else:

                raise

    return empty_result()