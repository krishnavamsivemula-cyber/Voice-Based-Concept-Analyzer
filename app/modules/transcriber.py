"""Speech-to-text transcription using Whisper."""

from pathlib import Path

import whisper

_whisper_model = None


class TranscriptionError(Exception):
    """Raised when Whisper model loading or transcription fails."""


def _load_whisper_model() -> whisper.Whisper:
    """
    Load and cache the Whisper 'base' model.

    Returns:
        The loaded Whisper model instance.

    Raises:
        TranscriptionError: If the model cannot be loaded.
    """
    global _whisper_model

    if _whisper_model is not None:
        return _whisper_model

    try:
        _whisper_model = whisper.load_model("base")
    except Exception as exc:
        raise TranscriptionError(
            "Failed to load Whisper 'base' model. "
            "Ensure dependencies are installed and sufficient memory is available."
        ) from exc

    return _whisper_model


def transcribe_audio(audio_path: str) -> str:
    """
    Transcribe an audio file to text using OpenAI Whisper.

    Args:
        audio_path: Filesystem path to a supported audio file.

    Returns:
        The transcript as a plain string with leading and trailing whitespace removed.

    Raises:
        FileNotFoundError: If the audio file does not exist.
        TranscriptionError: If model loading or transcription fails.
    """
    path = Path(audio_path)

    if not path.is_file():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    try:
        model = _load_whisper_model()
    except TranscriptionError:
        raise

    try:
        result = model.transcribe(str(path))
    except Exception as exc:
        raise TranscriptionError(
            f"Failed to transcribe audio file '{audio_path}'."
        ) from exc

    transcript = result.get("text", "")
    if not isinstance(transcript, str):
        raise TranscriptionError(
            f"Unexpected transcription result for '{audio_path}'."
        )

    return transcript.strip()
