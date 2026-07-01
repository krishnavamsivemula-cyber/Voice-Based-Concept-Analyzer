"""Report download and export UI components."""

import streamlit as st


def render_report_actions() -> None:
    """Render report-related actions, including a disabled download button."""
    st.subheader("Report")
    st.button(
        "Download Report",
        disabled=True,
        help="Available after analysis is complete.",
    )
