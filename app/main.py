"""Streamlit application entry point for VBCUA."""

from pathlib import Path

import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from modules.transcriber import TranscriptionError, transcribe_audio
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

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUDIO_DIR = PROJECT_ROOT / "data" / "audio"


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


def save_uploaded_audio(uploaded_file: UploadedFile) -> Path:
    """
    Save an uploaded audio file to the data/audio directory.

    Args:
        uploaded_file: Audio file uploaded through the Streamlit UI.

    Returns:
        Path to the saved audio file.
    """
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    audio_path = AUDIO_DIR / uploaded_file.name

    with audio_path.open("wb") as audio_file:
        audio_file.write(uploaded_file.getbuffer())

    return audio_path


def transcribe_uploaded_audio(uploaded_file: UploadedFile) -> str | None:
    """
    Save and transcribe an uploaded audio file.

    Args:
        uploaded_file: Audio file uploaded through the Streamlit UI.

    Returns:
        The transcript string if transcription succeeds, otherwise None.
    """
    file_key = f"{uploaded_file.name}:{uploaded_file.size}"

    if st.session_state.get("transcribed_file_key") == file_key:
        return st.session_state.get("transcript")

    try:
        audio_path = save_uploaded_audio(uploaded_file)
        transcript = transcribe_audio(str(audio_path))
    except FileNotFoundError:
        st.error("The uploaded audio file could not be found. Please upload it again.")
        return None
    except TranscriptionError as exc:
        st.error(f"Transcription failed: {exc}")
        return None
    except Exception:
        st.error("An unexpected error occurred during transcription.")
        return None

    st.session_state["transcribed_file_key"] = file_key
    st.session_state["transcript"] = transcript
    return transcript


def handle_transcription(uploaded_file: UploadedFile | None) -> str | None:
    """
    Run transcription when an audio file is available.

    Args:
        uploaded_file: Audio file uploaded through the Streamlit UI.

    Returns:
        The transcript string if available, otherwise None.
    """
    if uploaded_file is None:
        st.session_state.pop("transcript", None)
        st.session_state.pop("transcribed_file_key", None)
        return None

    return transcribe_uploaded_audio(uploaded_file)


def main() -> None:
    """Run the Streamlit application."""
    configure_page()
    render_sidebar()
    render_header()

    uploaded_file = render_upload_section()
    transcript = handle_transcription(uploaded_file)

    render_results_panel(transcript)
    render_report_actions()


if __name__ == "__main__":
    main()
