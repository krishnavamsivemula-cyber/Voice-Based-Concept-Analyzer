"""Audio upload and recording UI components."""

import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

SUPPORTED_EXTENSIONS = ["wav", "mp3", "m4a"]


def render_upload_section() -> UploadedFile | None:
    """
    Render the audio file uploader and display the selected filename.

    Returns:
        The uploaded file, or None if no file has been selected.
    """

    st.subheader("📤 Upload Student Response")

    st.caption(
        "Upload a student's recorded explanation for AI-powered concept evaluation."
    )

    with st.container(border=True):

        st.markdown(
            "**Supported formats:** WAV • MP3 • M4A"
        )

        uploaded_file = st.file_uploader(
            "Choose an audio file",
            type=SUPPORTED_EXTENSIONS,
            help="Accepted formats: WAV, MP3, M4A",
            key="audio_uploader",
            label_visibility="collapsed",
        )

        if uploaded_file is not None:
            st.success(f"✅ Uploaded: **{uploaded_file.name}**")

    return uploaded_file
