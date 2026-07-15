"""Report download and export UI components."""

from pathlib import Path

import streamlit as st


def render_report_actions() -> None:
    """
    Render report download actions based on the generated report path.

    Displays a disabled placeholder button when no report is available,
    or an active download button when a PDF report exists in session state.
    """
    st.subheader("Report")

    report_path = st.session_state.get("report_path")

    if not report_path:
        st.button(
            "Generate a report by analyzing an audio file.",
            disabled=True,
        )
        return

    try:
        pdf_bytes = Path(report_path).read_bytes()
    except FileNotFoundError:
        st.warning("Report file could not be found. Please analyze an audio file again.")
        st.button(
            "Generate a report by analyzing an audio file.",
            disabled=True,
        )
        return

    st.download_button(
        label="Download PDF Report",
        data=pdf_bytes,
        file_name="concept_report.pdf",
        mime="application/pdf",
    )