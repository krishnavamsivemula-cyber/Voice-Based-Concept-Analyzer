"""File read and write helpers."""

from pathlib import Path


def load_reference_answer(file_path: str) -> str:
    """
    Load a reference answer from a UTF-8 text file.

    Args:
        file_path: Path to the reference answer text file.

    Returns:
        The file contents as a string with leading and trailing whitespace removed.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is empty or contains only whitespace.
    """
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"Reference answer file not found: {file_path}")

    content = path.read_text(encoding="utf-8").strip()

    if not content:
        raise ValueError(f"Reference answer file is empty: {file_path}")

    return content
