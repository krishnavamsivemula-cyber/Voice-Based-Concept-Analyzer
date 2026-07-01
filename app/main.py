"""Streamlit application entry point for VBCUA."""

import streamlit as st

from ui.report_actions import render_report_actions
from ui.results_panel import render_results_panel
from ui.sidebar import render_sidebar
from ui.upload_section import render_upload_section

PAGE_TITLE = "Voice-Based Concept Understanding Analyzer"
PAGE_ICON = "🎙️"

PROJECT_HEADING = "Voice-Based Concept Understanding Analyzer"
PROJECT_DESCRIPTION = (
    "VBCUA helps evaluate how well a student understands a concept based on "
    "their spoken explanation. Upload an audio answer to transcribe speech, "
    "compare it against reference answers, and generate an assessment report."
)


def configure_page() -> None:
    """Configure Streamlit page layout and metadata."""
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout="wide",
    )


def render_header() -> None:
    """Render the main page heading and project description."""
    st.title(PROJECT_HEADING)
    st.markdown(PROJECT_DESCRIPTION)


def main() -> None:
    """Run the Streamlit application."""
    configure_page()
    render_sidebar()
    render_header()
    render_upload_section()
    render_results_panel()
    render_report_actions()


if __name__ == "__main__":
    main()
