"""Sidebar layout and navigation components."""

import streamlit as st

PROJECT_NAME = "Voice-Based Concept Understanding Analyzer (VBCUA)"

PROJECT_OBJECTIVES = [
    "Convert spoken answers into text using speech recognition.",
    "Evaluate concept understanding through semantic similarity analysis.",
    "Generate structured PDF reports for review and assessment.",
]

SUPPORTED_AUDIO_FORMATS = ["WAV", "MP3", "M4A"]

TECHNOLOGY_STACK = [
    "Python 3.12",
    "Streamlit",
    "OpenAI Whisper",
    "Sentence Transformers",
    "Librosa",
    "ReportLab",
]


def render_sidebar() -> None:
    """Render the application sidebar with project information."""
    with st.sidebar:
        st.header(PROJECT_NAME)

        st.subheader("Objectives")
        for objective in PROJECT_OBJECTIVES:
            st.markdown(f"- {objective}")

        st.subheader("Supported Audio Formats")
        st.markdown(", ".join(SUPPORTED_AUDIO_FORMATS))

        st.subheader("Technology Stack")
        for technology in TECHNOLOGY_STACK:
            st.markdown(f"- {technology}")
