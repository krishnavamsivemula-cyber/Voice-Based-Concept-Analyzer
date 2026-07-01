"""Audio upload and recording UI components."""

import streamlit as st

SUPPORTED_EXTENSIONS = ["wav", "mp3", "m4a"]


def render_upload_section() -> None:
    """Render the audio file uploader and display the selected filename."""
    st.subheader("Upload Audio")
    st.markdown(
        "Upload a recorded answer in **WAV**, **MP3**, or **M4A** format. "
        "The file will be analyzed after processing is enabled."
    )

    uploaded_file = st.file_uploader(
        "Choose an audio file",
        type=SUPPORTED_EXTENSIONS,
        help="Accepted formats: WAV, MP3, M4A",
    )

    if uploaded_file is not None:
        st.info(f"Uploaded file: **{uploaded_file.name}**")
