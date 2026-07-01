"""Concept understanding score computation."""


def score_concept_understanding(similarity: float) -> dict:
    """
    Convert a semantic similarity score into a user-friendly assessment.

    Args:
        similarity: Cosine similarity score between 0.0 and 1.0.

    Returns:
        Dictionary containing:
            - score
            - grade
            - feedback

    Raises:
        ValueError: If similarity is outside the range 0.0–1.0.
    """

    if not 0.0 <= similarity <= 1.0:
        raise ValueError("Similarity score must be between 0.0 and 1.0.")

    percentage = round(similarity * 100, 2)

    if percentage >= 90:
        grade = "Excellent"
        feedback = (
            "The explanation closely matches the reference answer and "
            "demonstrates excellent conceptual understanding."
        )

    elif percentage >= 75:
        grade = "Good"
        feedback = (
            "The explanation covers most important concepts with only minor omissions."
        )

    elif percentage >= 60:
        grade = "Fair"
        feedback = (
            "The explanation demonstrates partial understanding but misses several important concepts."
        )

    else:
        grade = "Needs Improvement"
        feedback = (
            "The explanation does not sufficiently cover the key concepts of the reference answer."
        )

    return {
        "score": percentage,
        "grade": grade,
        "feedback": feedback,
    }