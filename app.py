import streamlit as st

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
    placeholder="e.g. Which document introduced the change from PS-04 to PS-04A?"
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

            except Exception as e:

                st.error(
                    f"An error occurred: {e}"
                )

                st.stop()


        # ====================================================
        # ANSWER
        # ====================================================

        st.subheader("Answer")

        st.write(
            result.get(
                "answer",
                "No answer available."
            )
        )


        # ====================================================
        # EVIDENCE
        # ====================================================

        evidence = result.get(
            "evidence",
            []
        )

        with st.expander(
            "Evidence",
            expanded=True
        ):

            if evidence:

                for item in evidence:

                    if isinstance(item, dict):

                        st.markdown(
                            f"**{item.get('statement', '')}**"
                        )

                        st.caption(
                            f"Source: "
                            f"{item.get('filename', 'Unknown')} — "
                            f"{item.get('location', 'Unknown')}"
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
                "⚠️ Conflicts",
                expanded=True
            ):

                for item in conflicts:

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
                "❓ Uncertainty",
                expanded=True
            ):

                for item in uncertainty:

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
                "🔎 Information Gaps",
                expanded=True
            ):

                for item in gaps:

                    st.markdown(
                        f"- {item}"
                    )


