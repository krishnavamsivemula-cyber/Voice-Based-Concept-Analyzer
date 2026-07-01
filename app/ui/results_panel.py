"""Analysis results display components."""

import streamlit as st


def render_results_panel(
    transcript: str | None,
    similarity_score: float | None,
    score_data: dict | None,
) -> None:
    """
    Render the analysis results section.

    Args:
        transcript: Transcribed text to display, or None to show a placeholder.
        similarity_score: Semantic similarity score between 0.0 and 1.0, or None.
        score_data: Concept understanding assessment with grade and feedback, or None.
    """
    st.subheader("Analysis Results")

    if transcript is None:
        st.info("Analysis results will appear here.")
        return

    st.markdown("**Transcript**")
    st.text_area(
        label="Transcript",
        value=transcript,
        height=200,
        disabled=True,
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("**Concept Understanding Score**")

    if similarity_score is not None:
        st.metric(
            label="Concept Understanding Score",
            value=f"{similarity_score * 100:.2f} %",
        )
    else:
        st.warning("Concept understanding score could not be computed.")

    if score_data is not None:
        st.divider()
        st.markdown("**Grade**")
        st.markdown(score_data["grade"])
        st.markdown("**Feedback**")
        st.markdown(score_data["feedback"])
