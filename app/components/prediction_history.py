from datetime import datetime

import pandas as pd
import streamlit as st


HISTORY_COLUMNS = [
    "Date",
    "Time",
    "Genre",
    "Budget",
    "Runtime",
    "Release Month",
    "Popularity",
    "Prediction",
    "Probability",
    "Confidence",
]


def _initialize_history() -> pd.DataFrame:
    if "prediction_history_df" not in st.session_state:
        st.session_state.prediction_history_df = pd.DataFrame(columns=HISTORY_COLUMNS)
    return st.session_state.prediction_history_df


def add_prediction_to_history(genre, budget, runtime, release_month, popularity_score, prediction, probability, confidence):
    history_df = _initialize_history()
    now = datetime.now()

    new_row = {
        "Date": now.strftime("%d %b %Y"),
        "Time": now.strftime("%I:%M %p"),
        "Genre": genre,
        "Budget": f"${budget / 1_000_000:.1f}M",
        "Runtime": int(runtime),
        "Release Month": int(release_month),
        "Popularity": float(popularity_score),
        "Prediction": prediction,
        "Probability": f"{probability * 100:.1f}%",
        "Confidence": confidence,
    }

    updated_history = pd.concat([history_df, pd.DataFrame([new_row])], ignore_index=True)
    st.session_state.prediction_history_df = updated_history
    return updated_history


def render_prediction_history_section():
    st.markdown('<h2 class="section-heading">📜 Prediction History</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#CFC9B7;max-width:1200px;margin-bottom:0.9rem;">View, manage, and export previous AI predictions.</p>', unsafe_allow_html=True)

    history_df = _initialize_history()

    button_col1, button_col2 = st.columns([1, 1])
    with button_col1:
        csv_bytes = history_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Prediction History",
            data=csv_bytes,
            file_name="prediction_history.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with button_col2:
        if st.button("🗑 Clear History", use_container_width=True):
            st.session_state.show_clear_confirm = True

    if st.session_state.get("show_clear_confirm", False):
        st.warning("This will remove all entries from the current session history. Continue?")
        confirm_col1, confirm_col2 = st.columns(2)
        with confirm_col1:
            if st.button("✅ Confirm Clear", use_container_width=True):
                st.session_state.prediction_history_df = pd.DataFrame(columns=HISTORY_COLUMNS)
                st.session_state.show_clear_confirm = False
                st.success("Prediction history cleared.")
        with confirm_col2:
            if st.button("Cancel", use_container_width=True):
                st.session_state.show_clear_confirm = False

    if history_df.empty:
        st.markdown(
            '<div style="background:#1A1A1A;border:1px solid rgba(212,175,55,0.16);border-radius:20px;padding:1rem;color:#CFC9B7;">No prediction history yet. Submit a prediction to see it appear here.</div>',
            unsafe_allow_html=True,
        )
    else:
        display_df = history_df.copy()
        display_df = display_df.reset_index(drop=True)
        st.dataframe(
            display_df,
            use_container_width=True,
            height=320,
            hide_index=True,
        )
