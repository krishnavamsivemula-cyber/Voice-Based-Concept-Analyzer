"""Semantic similarity analysis using Sentence Transformers."""

from sentence_transformers import SentenceTransformer, util

MODEL_NAME = "all-MiniLM-L6-v2"

_sentence_transformer_model = None


class SemanticAnalysisError(Exception):
    """Raised when semantic model loading or similarity computation fails."""


def _load_sentence_transformer_model() -> SentenceTransformer:
    """
    Load and cache the Sentence Transformer model.

    Returns:
        The loaded SentenceTransformer instance.

    Raises:
        SemanticAnalysisError: If the model cannot be loaded.
    """
    global _sentence_transformer_model

    if _sentence_transformer_model is not None:
        return _sentence_transformer_model

    try:
        _sentence_transformer_model = SentenceTransformer(MODEL_NAME)
    except Exception as exc:
        raise SemanticAnalysisError(
            f"Failed to load Sentence Transformer model '{MODEL_NAME}'. "
            "Ensure dependencies are installed and sufficient memory is available."
        ) from exc

    return _sentence_transformer_model


def _validate_text(text: str, field_name: str) -> str:
    """
    Validate and normalize input text.

    Args:
        text: Input text to validate.
        field_name: Name of the field for error messages.

    Returns:
        Stripped text ready for embedding.

    Raises:
        SemanticAnalysisError: If the text is empty after stripping.
    """
    normalized_text = text.strip()

    if not normalized_text:
        raise SemanticAnalysisError(f"{field_name} must not be empty.")

    return normalized_text


def calculate_similarity(transcript: str, reference_answer: str) -> float:
    """
    Compute cosine similarity between a transcript and a reference answer.

    Args:
        transcript: Transcribed student answer text.
        reference_answer: Ground-truth reference answer text.

    Returns:
        Cosine similarity score between 0.0 and 1.0.

    Raises:
        SemanticAnalysisError: If inputs are empty or similarity computation fails.
    """
    normalized_transcript = _validate_text(transcript, "Transcript")
    normalized_reference = _validate_text(reference_answer, "Reference answer")

    try:
        model = _load_sentence_transformer_model()
    except SemanticAnalysisError:
        raise

    try:
        embeddings = model.encode(
            [normalized_transcript, normalized_reference],
            convert_to_tensor=True,
        )
        similarity = util.cos_sim(embeddings[0], embeddings[1]).item()
    except Exception as exc:
        raise SemanticAnalysisError(
            "Failed to generate embeddings or compute cosine similarity."
        ) from exc

    return max(0.0, min(1.0, float(similarity)))
