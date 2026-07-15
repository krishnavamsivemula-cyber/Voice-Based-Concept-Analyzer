"""Streamlit application entry point for VBCUA."""

from pathlib import Path

import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from modules.concept_scorer import score_concept_understanding
from modules.report_generator import generate_report
from modules.semantic_analyzer import SemanticAnalysisError, calculate_similarity
from modules.transcriber import TranscriptionError, transcribe_audio
from ui.report_actions import render_report_actions
from ui.results_panel import render_results_panel
from ui.sidebar import render_sidebar
from ui.upload_section import render_upload_section
from utils.file_io import load_reference_answer

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
REFERENCE_ANSWER_PATH = PROJECT_ROOT / "data" / "reference_answers" / "sample_answer.txt"
REPORT_PATH = PROJECT_ROOT / "reports" / "concept_report.pdf"


def configure_page() -> None:
    """Configure Streamlit page layout and metadata."""
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout="wide",
    )
    st.markdown("""
        <style>
            section[data-testid="stSidebar"]{
                width:280px !important;
            }
        </style>
        """, unsafe_allow_html=True)
    
def apply_custom_theme() -> None:
    """Apply a modern corporate theme."""

    st.markdown(
        """
        <style>

        /* Main page */
        .main {
            background-color: #F7F9FC;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #EEF4FB;
        }

        /* Headers */
        h1 {
            color: #0F172A;
        }

        h2, h3 {
            color: #1E3A5F;
        }

        /* Metric cards */
        div[data-testid="stMetric"] {
            background: white;
            border: 1px solid #D9E4F5;
            border-radius: 14px;
            padding: 18px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.05);
        }

        /* Upload box */
        div[data-testid="stFileUploader"] {
            border: 2px dashed #2563EB;
            border-radius: 14px;
            background: #FFFFFF;
        }

        /* Alerts */
        div[data-testid="stAlert"] {
            border-radius: 12px;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    """Render the main page heading and project description."""

    st.title("🎙️ Voice-Based Concept Understanding Analyzer")

    st.caption(
        "AI-powered speech recognition and semantic analysis for evaluating "
        "conceptual understanding."
    )

    st.markdown(
        """
        Upload a student's spoken explanation and let the application:

        - 🎤 Convert speech into text using **OpenAI Whisper**
        - 🧠 Compare the response with a reference answer
        - 📊 Calculate a semantic similarity score
        - 🏆 Generate a concept understanding grade
        - 📄 Create a downloadable PDF assessment report
        """
    )

    st.divider()


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


def compute_similarity_score(transcript: str) -> float | None:
    """
    Load the reference answer and compute semantic similarity for a transcript.

    Args:
        transcript: Transcribed student answer text.

    Returns:
        Similarity score between 0.0 and 1.0, or None if computation fails.
    """
    try:
        reference_answer = load_reference_answer(str(REFERENCE_ANSWER_PATH))

        return calculate_similarity(transcript, reference_answer)
    except FileNotFoundError:
        st.warning("Reference answer file could not be found.")
        return None
    except ValueError as exc:
        st.warning(f"Reference answer could not be loaded: {exc}")
        return None
    except SemanticAnalysisError as exc:
        st.warning(f"Semantic similarity could not be computed: {exc}")
        return None
    except Exception:
        st.warning("An unexpected error occurred during semantic analysis.")
        return None


def compute_score_data(similarity_score: float | None) -> dict | None:
    """
    Compute concept understanding grade and feedback from a similarity score.

    Args:
        similarity_score: Semantic similarity score between 0.0 and 1.0.

    Returns:
        Scoring dictionary with score, grade, and feedback, or None if unavailable.
    """
    if similarity_score is None:
        return None

    try:
        return score_concept_understanding(similarity_score)
    except ValueError as exc:
        st.warning(f"Concept score could not be computed: {exc}")
        return None


def generate_analysis_report(
    transcript: str | None,
    similarity_score: float | None,
    score_data: dict | None,
) -> str | None:
    """
    Generate a PDF report when all analysis data is available.

    Args:
        transcript: Transcribed student answer text.
        similarity_score: Semantic similarity score between 0.0 and 1.0.
        score_data: Concept understanding assessment dictionary.

    Returns:
        Path to the generated report, or None if generation was skipped or failed.
    """
    if not transcript or similarity_score is None or score_data is None:
        st.session_state.pop("report_path", None)
        return None

    try:
        report_path = generate_report(
            transcript=transcript,
            similarity_score=similarity_score,
            score_data=score_data,
            output_path=str(REPORT_PATH),
        )
    except (ValueError, RuntimeError) as exc:
        st.warning(f"Report generation failed: {exc}")
        st.session_state.pop("report_path", None)
        return None
    except Exception:
        st.warning("An unexpected error occurred during report generation.")
        st.session_state.pop("report_path", None)
        return None

    st.session_state["report_path"] = report_path
    return report_path


def transcribe_uploaded_audio(
    uploaded_file: UploadedFile,
) -> tuple[str | None, float | None, dict | None]:
    """
    Save, transcribe, and analyze an uploaded audio file.

    Args:
        uploaded_file: Audio file uploaded through the Streamlit UI.

    Returns:
        A tuple of transcript, similarity score, and score data; any may be None.
    """
    file_key = f"{uploaded_file.name}:{uploaded_file.size}"

    if st.session_state.get("transcribed_file_key") == file_key:
        return (
            st.session_state.get("transcript"),
            st.session_state.get("similarity_score"),
            st.session_state.get("score_data"),
        )

    try:
        audio_path = save_uploaded_audio(uploaded_file)
        transcript = transcribe_audio(str(audio_path))
    except FileNotFoundError:
        st.error("The uploaded audio file could not be found. Please upload it again.")
        return None, None, None
    except TranscriptionError as exc:
        st.error(f"Transcription failed: {exc}")
        return None, None, None
    except Exception:
        st.error("An unexpected error occurred during transcription.")
        return None, None, None

    similarity_score = compute_similarity_score(transcript)
    score_data = compute_score_data(similarity_score)

    st.session_state["transcribed_file_key"] = file_key
    st.session_state["transcript"] = transcript
    st.session_state["similarity_score"] = similarity_score
    st.session_state["score_data"] = score_data

    generate_analysis_report(transcript, similarity_score, score_data)

    return transcript, similarity_score, score_data


def handle_analysis(
    uploaded_file: UploadedFile | None,
) -> tuple[str | None, float | None, dict | None]:
    """
    Run transcription and semantic analysis when an audio file is available.

    Args:
        uploaded_file: Audio file uploaded through the Streamlit UI.

    Returns:
        A tuple of transcript, similarity score, and score data; any may be None.
    """
    if uploaded_file is None:
        st.session_state.pop("transcript", None)
        st.session_state.pop("similarity_score", None)
        st.session_state.pop("score_data", None)
        st.session_state.pop("report_path", None)
        st.session_state.pop("transcribed_file_key", None)
        return None, None, None

    return transcribe_uploaded_audio(uploaded_file)


def main() -> None:
    """Run the Streamlit application."""
    configure_page()
    # apply_custom_theme()

    render_sidebar()
    render_header()

    uploaded_file = render_upload_section()
    transcript, similarity_score, score_data = handle_analysis(uploaded_file)

    render_results_panel(transcript, similarity_score, score_data)
    render_report_actions()


if __name__ == "__main__":
    main()