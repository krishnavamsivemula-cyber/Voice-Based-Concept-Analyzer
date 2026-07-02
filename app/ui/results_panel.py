"""Analysis results display components."""

import streamlit as st


def render_results_panel(
    transcript: str | None,
    similarity_score: float | None,
    score_data: dict | None,
) -> None:
    """
    Render the analysis results section.

    Args:
        transcript: Transcribed text to display, or None to show a placeholder.
        similarity_score: Semantic similarity score between 0.0 and 1.0, or None.
        score_data: Concept understanding assessment with grade and feedback, or None.
    """

    st.subheader("📊 Analysis Results")

    if transcript is None:
        st.info("Upload an audio file to begin the analysis.")
        return

    # ---------------- Dashboard ---------------- #

    score_col, grade_col = st.columns(2)

    with score_col:
        if similarity_score is not None:
            st.metric(
                label="🎯 Similarity Score",
                value=f"{similarity_score * 100:.2f} %",
            )
        else:
            st.metric(
                label="🎯 Similarity Score",
                value="N/A",
            )

    with grade_col:
        if score_data is not None:
            grade = score_data["grade"]

            if grade == "Excellent":
                st.success(f"🏆 {grade}")

            elif grade == "Good":
                st.info(f"🥈 {grade}")

            elif grade == "Fair":
                st.warning(f"🥉 {grade}")

            else:
                st.error(f"⚠️ {grade}")

        else:
            st.info("Grade: N/A")

    st.divider()

    # ---------------- Transcript ---------------- #

    st.markdown("### 📝 Student Transcript")

    st.text_area(
        label="Transcript",
        value=transcript,
        height=220,
        disabled=True,
        label_visibility="collapsed",
    )

    # ---------------- Feedback ---------------- #

    if score_data is not None:
        st.divider()

        st.markdown("### 💡 Feedback")

        st.info(score_data["feedback"])
