"""PDF report generation using ReportLab."""

from datetime import datetime
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

REPORT_TITLE = "Voice-Based Concept Understanding Analyzer"
REQUIRED_SCORE_KEYS = ("score", "grade", "feedback")


def _validate_transcript(transcript: str) -> str:
    """
    Validate and normalize transcript text.

    Args:
        transcript: Transcribed student answer text.

    Returns:
        Stripped transcript text.

    Raises:
        ValueError: If the transcript is empty.
    """
    normalized_transcript = transcript.strip()

    if not normalized_transcript:
        raise ValueError("Transcript must not be empty.")

    return normalized_transcript


def _validate_similarity_score(similarity_score: float) -> float:
    """
    Validate the semantic similarity score.

    Args:
        similarity_score: Cosine similarity score between 0.0 and 1.0.

    Returns:
        The validated similarity score.

    Raises:
        ValueError: If the score is outside the range 0.0–1.0.
    """
    if not 0.0 <= similarity_score <= 1.0:
        raise ValueError("Similarity score must be between 0.0 and 1.0.")

    return similarity_score


def _validate_score_data(score_data: dict) -> dict:
    """
    Validate score data returned by the concept scorer.

    Args:
        score_data: Dictionary containing score, grade, and feedback.

    Returns:
        The validated score data dictionary.

    Raises:
        ValueError: If required fields are missing or invalid.
    """
    missing_keys = [key for key in REQUIRED_SCORE_KEYS if key not in score_data]

    if missing_keys:
        raise ValueError(
            f"Score data is missing required fields: {', '.join(missing_keys)}"
        )

    score = score_data["score"]
    grade = score_data["grade"]
    feedback = score_data["feedback"]

    if not isinstance(score, (int, float)):
        raise ValueError("Score data field 'score' must be numeric.")

    if not isinstance(grade, str) or not grade.strip():
        raise ValueError("Score data field 'grade' must be a non-empty string.")

    if not isinstance(feedback, str) or not feedback.strip():
        raise ValueError("Score data field 'feedback' must be a non-empty string.")

    return score_data


def _build_report_story(
    transcript: str,
    similarity_score: float,
    score_data: dict,
) -> list:
    """
    Build ReportLab story elements for the assessment report.

    Args:
        transcript: Transcribed student answer text.
        similarity_score: Cosine similarity score between 0.0 and 1.0.
        score_data: Dictionary containing score, grade, and feedback.

    Returns:
        List of ReportLab flowables for PDF generation.
    """
    styles = getSampleStyleSheet()
    similarity_percentage = similarity_score * 100

    return [
        Paragraph(REPORT_TITLE, styles["Title"]),
        Spacer(1, 0.3 * inch),
        Paragraph("Student Transcript", styles["Heading2"]),
        Spacer(1, 0.1 * inch),
        Paragraph(transcript.replace("\n", "<br/>"), styles["BodyText"]),
        Spacer(1, 0.3 * inch),
        Paragraph("Concept Understanding Score", styles["Heading2"]),
        Spacer(1, 0.1 * inch),
        Paragraph(
            f"Similarity Score: {similarity_percentage:.2f} %",
            styles["Normal"],
        ),
        Spacer(1, 0.05 * inch),
        Paragraph(f"Grade: {score_data['grade']}", styles["Normal"]),
        Spacer(1, 0.3 * inch),
        Paragraph("Feedback", styles["Heading2"]),
        Spacer(1, 0.1 * inch),
        Paragraph(score_data["feedback"], styles["BodyText"]),
        Spacer(1, 0.3 * inch),
        Paragraph("Generated On", styles["Heading2"]),
        Spacer(1, 0.1 * inch),
        Paragraph(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            styles["Normal"],
        ),
    ]


def generate_report(
    transcript: str,
    similarity_score: float,
    score_data: dict,
    output_path: str,
) -> str:
    """
    Generate a PDF assessment report for an analyzed student answer.

    Args:
        transcript: Transcribed student answer text.
        similarity_score: Cosine similarity score between 0.0 and 1.0.
        score_data: Dictionary containing score, grade, and feedback.
        output_path: Destination path for the generated PDF report.

    Returns:
        The output path after successful PDF generation.

    Raises:
        ValueError: If any input is invalid.
        RuntimeError: If PDF generation fails.
    """
    normalized_transcript = _validate_transcript(transcript)
    validated_similarity_score = _validate_similarity_score(similarity_score)
    validated_score_data = _validate_score_data(score_data)

    pdf_path = Path(output_path)
    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        document = SimpleDocTemplate(
            str(pdf_path),
            pagesize=letter,
            title=REPORT_TITLE,
        )
        story = _build_report_story(
            transcript=normalized_transcript,
            similarity_score=validated_similarity_score,
            score_data=validated_score_data,
        )
        document.build(story)
    except Exception as exc:
        raise RuntimeError(
            f"Failed to generate PDF report at '{output_path}'."
        ) from exc

    return output_path