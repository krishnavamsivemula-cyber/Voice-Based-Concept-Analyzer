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
    st.subheader("Upload Audio")
    st.markdown(
        "Upload a recorded answer in **WAV**, **MP3**, or **M4A** format. "
        "The file will be analyzed after processing is enabled."
    )

    uploaded_file = st.file_uploader(
        "Choose an audio file",
        type=SUPPORTED_EXTENSIONS,
        help="Accepted formats: WAV, MP3, M4A",
        key="audio_uploader",
    )

    if uploaded_file is not None:
        st.info(f"Uploaded file: **{uploaded_file.name}**")

    return uploaded_file
