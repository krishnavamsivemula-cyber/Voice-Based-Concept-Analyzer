"""Analysis results display components."""

import streamlit as st


def render_results_panel(transcript: str | None) -> None:
    """
    Render the analysis results section.

    Args:
        transcript: Transcribed text to display, or None to show a placeholder.
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
