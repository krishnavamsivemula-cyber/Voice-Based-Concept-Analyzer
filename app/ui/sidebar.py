"""Sidebar layout and navigation components."""

import streamlit as st

PROJECT_NAME = "Voice-Based Concept Understanding Analyzer (VBCUA)"

PROJECT_OBJECTIVES = [
    "Speech-to-text transcription",
    "Semantic similarity analysis",
    "Concept understanding scoring",
    "Downloadable PDF reports",
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

        st.markdown("## 🎙️ VBCUA")

        st.caption("AI-powered Concept Understanding Analyzer")

        st.divider()

        with st.expander("🎯 Project Objectives", expanded=True):
            for objective in PROJECT_OBJECTIVES:
                st.markdown(f"• {objective}")

        with st.expander("🎵 Supported Formats", expanded=True):
            st.markdown(" • ".join(SUPPORTED_AUDIO_FORMATS))

        with st.expander("🛠 Technology Stack", expanded=True):
            for technology in TECHNOLOGY_STACK:
                st.markdown(f"• {technology}")

        st.divider()

        st.caption("Version 1.0")
        st.caption("Built with ❤️ using Python, Streamlit & AI")
