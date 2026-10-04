import streamlit as st
import json

from src.answering.answer_question import answer_question


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Aegis Knowledge Assistant",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("Aegis Knowledge Assistant")

st.write(
    "Ask questions about the Aegis Series-7 HCS documentation."
)

st.caption(
    "Answers are based only on the available documentation "
    "and include evidence and provenance."
)


# ============================================================
# QUESTION
# ============================================================

question = st.text_input(
    "Enter your question",
    placeholder=(
        "e.g. Which document introduced the change "
        "from PS-04 to PS-04A?"
    )
)


# ============================================================
# ASK
# ============================================================

if st.button("Ask", type="primary"):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Searching documentation..."
        ):

            try:

                result = answer_question(
                    question
                )

                # Convert JSON string to Python dictionary
                # if answer_question() returns JSON text.
                if isinstance(result, str):

                    result = json.loads(result)

            except json.JSONDecodeError:

                st.error(
                    "The answer returned by the AI "
                    "was not valid JSON."
                )

                st.stop()

            except Exception as e:

                st.error(
                    f"An error occurred: {e}"
                )

                st.stop()


        # ====================================================
        # ANSWER
        # ====================================================

        st.subheader("Answer")

        answer = result.get(
            "answer",
            "No answer available."
        )

        st.write(answer)


        # ====================================================
        # EVIDENCE
        # ====================================================

        evidence = result.get(
            "evidence",
            []
        )

        with st.expander(
            "Supporting Evidence",
            expanded=True
        ):

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

                        if statement:

                            st.markdown(
                                f"**{statement}**"
                            )

                        st.caption(
                            f"Source: {filename} — {location}"
                        )

                    else:

                        st.markdown(
                            f"- {item}"
                        )

            else:

                st.write(
                    "No supporting evidence found."
                )


        # ====================================================
        # CONFLICTS
        # ====================================================

        conflicts = result.get(
            "conflicts",
            []
        )

        if conflicts:

            with st.expander(
                "Conflicts",
                expanded=True
            ):

                for item in conflicts:

                    if isinstance(item, dict):

                        st.markdown(
                            f"- {item}"
                        )

                    else:

                        st.markdown(
                            f"- {item}"
                        )


        # ====================================================
        # UNCERTAINTY
        # ====================================================

        uncertainty = result.get(
            "uncertainty",
            []
        )

        if uncertainty:

            with st.expander(
                "Uncertainty",
                expanded=True
            ):

                for item in uncertainty:

                    if isinstance(item, dict):

                        st.markdown(
                            f"- {item}"
                        )

                    else:

                        st.markdown(
                            f"- {item}"
                        )


        # ====================================================
        # INFORMATION GAPS
        # ====================================================

        gaps = result.get(
            "gaps",
            []
        )

        if gaps:

            with st.expander(
                "Information Gaps",
                expanded=True
            ):

                # Handle a single dictionary
                if isinstance(gaps, dict):

                    question_text = gaps.get(
                        "question",
                        ""
                    )

                    reason = gaps.get(
                        "reason",
                        ""
                    )

                    if question_text:

                        st.markdown(
                            f"**Question:** {question_text}"
                        )

                    if reason:

                        st.markdown(
                            f"**Reason:** {reason}"
                        )

                # Handle a list of gaps
                else:

                    for item in gaps:

                        if isinstance(item, dict):

                            question_text = item.get(
                                "question",
                                ""
                            )

                            reason = item.get(
                                "reason",
                                ""
                            )

                            if question_text:

                                st.markdown(
                                    f"**Question:** "
                                    f"{question_text}"
                                )

                            if reason:

                                st.markdown(
                                    f"**Reason:** "
                                    f"{reason}"
                                )

                        else:

                            st.markdown(
                                f"- {item}"
                            )