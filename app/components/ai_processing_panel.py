import time
import streamlit as st


DEFAULT_STEPS = [
    {"title": "Loading trained Random Forest model", "detail": "The trained model is loaded from disk and prepared for inference."},
    {"title": "Validating user input", "detail": "The form values are checked to ensure the request is complete and valid."},
    {"title": "Encoding categorical variables", "detail": "Genre values are converted into the format expected by the model."},
    {"title": "Preparing numerical features", "detail": "Budget, runtime, release month, and popularity are normalized for prediction."},
    {"title": "Running machine learning prediction", "detail": "The model evaluates the prepared features and predicts the outcome."},
    {"title": "Calculating prediction probabilities", "detail": "The model estimates how likely each class is for the submitted movie."},
    {"title": "Generating Explainable AI insights", "detail": "Feature importance is computed to explain the prediction to the user."},
]


def build_processing_steps():
    return [dict(step) for step in DEFAULT_STEPS]


def render_ai_processing_panel():
    steps = build_processing_steps()
    panel_placeholder = st.empty()

    with panel_placeholder.container():
        st.markdown(
            """
            <div style="background:#1A1A1A;border:1px solid #D4AF37;border-radius:24px;padding:1.2rem 1.2rem 1rem;box-shadow:0 16px 36px rgba(0,0,0,0.25);margin-bottom:1rem;">
                <div style="display:flex;justify-content:space-between;align-items:center;gap:0.75rem;margin-bottom:0.65rem;">
                    <div style="font-size:1.05rem;font-weight:700;color:#FFFFFF;">🤖 AI Processing</div>
                    <div style="color:#D4AF37;font-weight:700;">Live workflow</div>
                </div>
            """,
            unsafe_allow_html=True,
        )

        st.progress(0.0)

        for index, step in enumerate(steps):
            step_text = f"⏳ {step['title']}..."
            st.markdown(
                f"<div style='color:#F3DC81;margin:0.35rem 0;font-size:0.98rem;'>{step_text}</div>",
                unsafe_allow_html=True,
            )
            progress_value = (index + 1) / len(steps)
            st.progress(progress_value)
            time.sleep(0.38)
            st.markdown(
                f"<div style='color:#D4AF37;margin:0.1rem 0 0.5rem;font-size:0.92rem;'>✅ Completed</div>",
                unsafe_allow_html=True,
            )

        st.markdown(
            "<div style='color:#FFFFFF;font-weight:700;margin-top:0.5rem;'>🎉 Prediction Ready!</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div style="margin-top:0.85rem;padding:0.9rem 1rem;border-radius:16px;background:rgba(255,255,255,0.04);border:1px solid rgba(212,175,55,0.14);color:#CFC9B7;">
                <div style="font-weight:700;color:#FFFFFF;margin-bottom:0.35rem;">What is happening?</div>
                <ul style="margin:0.2rem 0 0;padding-left:1.1rem;line-height:1.65;">
                    <li>The trained Random Forest model is loaded.</li>
                    <li>Your movie information is validated.</li>
                    <li>Categorical values such as Genre are encoded into numerical values.</li>
                    <li>Numerical features are prepared.</li>
                    <li>The AI model predicts the movie's success.</li>
                    <li>Prediction probabilities are calculated.</li>
                    <li>Explainable AI generates feature importance.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

