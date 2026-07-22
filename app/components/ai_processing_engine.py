import time

import streamlit as st


INITIAL_STEP = {
    "task": "Initializing AI engine",
    "console": "Initializing AI engine...",
}


ENGINE_STEPS = [
    {
        "task": "Loading trained Random Forest",
        "console": "Loading trained Random Forest model...",
        "progress": 10,
    },
    {
        "task": "Validating user input",
        "console": "Validating user input...",
        "progress": 25,
    },
    {
        "task": "Encoding Genre",
        "console": "Encoding categorical features...",
        "progress": 40,
    },
    {
        "task": "Preparing numerical features",
        "console": "Preparing numerical features...",
        "progress": 55,
    },
    {
        "task": "Running prediction",
        "console": "Running prediction model...",
        "progress": 70,
    },
    {
        "task": "Calculating probabilities",
        "console": "Calculating prediction probabilities...",
        "progress": 85,
    },
    {
        "task": "Building Explainable AI report",
        "console": "Building Explainable AI report...",
        "progress": 100,
    },
]


def build_engine_steps():
    return [dict(step) for step in ENGINE_STEPS]


def render_ai_processing_engine(stage_delay=0.34):
    steps = build_engine_steps()
    card = st.container()

    with card:
        st.markdown(
            """
            <style>
            .ai-engine-card {
                max-width: 1200px;
                margin: 0 auto 1.4rem;
                padding: 1.35rem;
                background: #1A1A1A;
                border: 1px solid rgba(212, 175, 55, 0.24);
                border-radius: 24px;
                box-shadow: 0 18px 42px rgba(0, 0, 0, 0.28);
            }
            .ai-engine-title {
                margin: 0;
                color: #FFFFFF;
                font-size: 1.35rem;
                font-weight: 800;
            }
            .ai-engine-subtitle {
                margin: 0.35rem 0 1rem;
                color: #CFC9B7;
                line-height: 1.55;
            }
            .ai-engine-label {
                color: #D4AF37;
                font-size: 0.82rem;
                font-weight: 800;
                letter-spacing: 0.12em;
                text-transform: uppercase;
                margin-bottom: 0.25rem;
            }
            .ai-engine-value {
                color: #FFFFFF;
                font-weight: 700;
                margin-bottom: 0.7rem;
            }
            .ai-engine-console {
                min-height: 250px;
                margin-top: 1rem;
                padding: 1rem;
                background: #0E0E0E;
                border: 1px solid rgba(212, 175, 55, 0.16);
                border-radius: 16px;
                color: #F7E7B0;
                font-family: Consolas, "Courier New", monospace;
                line-height: 1.7;
                white-space: pre-wrap;
            }
            .ai-engine-info {
                margin-top: 1rem;
                padding: 1rem;
                background: rgba(255, 255, 255, 0.04);
                border-left: 4px solid #D4AF37;
                border-radius: 14px;
                color: #CFC9B7;
                line-height: 1.65;
            }
            .ai-engine-info strong {
                color: #FFFFFF;
            }
            </style>
            <div class="ai-engine-card">
                <h2 class="ai-engine-title">🧠 CineMind AI Engine</h2>
                <p class="ai-engine-subtitle">Analyzing movie characteristics using machine learning...</p>
            """,
            unsafe_allow_html=True,
        )

        progress = st.progress(0, text="Progress 0%")
        status_placeholder = st.empty()
        console_placeholder = st.empty()

        console_lines = []
        status_placeholder.markdown(
            f"""
            <div class="ai-engine-label">Current Task</div>
            <div class="ai-engine-value">{INITIAL_STEP["task"]}</div>
            """,
            unsafe_allow_html=True,
        )
        console_lines.append(f"⏳ {INITIAL_STEP['console']}")
        console_placeholder.markdown(
            f"<div class='ai-engine-console'>{'<br>'.join(console_lines)}</div>",
            unsafe_allow_html=True,
        )
        time.sleep(stage_delay)
        console_lines[-1] = f"✓ {INITIAL_STEP['console']} Complete"
        console_placeholder.markdown(
            f"<div class='ai-engine-console'>{'<br>'.join(console_lines)}</div>",
            unsafe_allow_html=True,
        )

        for step in steps:
            status_placeholder.markdown(
                f"""
                <div class="ai-engine-label">Current Task</div>
                <div class="ai-engine-value">{step["task"]}</div>
                """,
                unsafe_allow_html=True,
            )
            console_lines.append(f"⏳ {step['console']}")
            console_placeholder.markdown(
                f"<div class='ai-engine-console'>{'<br>'.join(console_lines)}</div>",
                unsafe_allow_html=True,
            )

            progress.progress(step["progress"], text=f"Progress {step['progress']}%")
            time.sleep(stage_delay)

            console_lines[-1] = f"✓ {step['console']} Complete"
            console_placeholder.markdown(
                f"<div class='ai-engine-console'>{'<br>'.join(console_lines)}</div>",
                unsafe_allow_html=True,
            )

        console_lines.append("🎉 Prediction Ready")
        status_placeholder.markdown(
            """
            <div class="ai-engine-label">Current Task</div>
            <div class="ai-engine-value">Prediction Ready</div>
            """,
            unsafe_allow_html=True,
        )
        console_placeholder.markdown(
            f"<div class='ai-engine-console'>{'<br>'.join(console_lines)}</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
                <div class="ai-engine-info">
                    <strong>🔍 What is happening?</strong><br>
                    The trained Random Forest model is loaded.<br>
                    Movie features are validated.<br>
                    Genre is encoded into numerical values.<br>
                    Numerical features are prepared.<br>
                    Machine learning prediction is performed.<br>
                    Probabilities are calculated.<br>
                    Explainable AI is generated.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
