import base64
import importlib
import sys
import textwrap
import time
import pandas as pd
from pathlib import Path
import streamlit as st
from styles import load_styles

PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_DIR = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

importlib.invalidate_caches()
for module_name in [
    "src.dashboard",
    "src.config",
    "src.utils",
    "src.predictor",
    "src.report_generator",
    "src.scenario_simulator",
]:
    sys.modules.pop(module_name, None)

from src.predictor import MoviePredictor
from src.report_generator import save_prediction_report
from src.scenario_simulator import create_scenario_input
from src.config import FEATURE_COLUMNS
from components.explainable_ai import render_explanation
from components.what_if_simulator import render_what_if
from components.prediction_history import add_prediction_to_history, render_prediction_history_section
from components.chatbot import render_cinemind_assistant
from components.ai_processing_panel import render_ai_processing_panel
from components.home_page import render_home_page

dashboard_module = importlib.import_module("src.dashboard")
get_dashboard_data = dashboard_module.get_dashboard_data
create_genre_chart = dashboard_module.create_genre_chart
create_revenue_chart = dashboard_module.create_revenue_chart
create_budget_vs_revenue_chart = getattr(dashboard_module, "create_budget_vs_revenue_chart", lambda df: None)

LOGO_PATH = Path(__file__).parent / "download.jpg"

st.set_page_config(page_title="CineMind AI", page_icon=str(LOGO_PATH) if LOGO_PATH.exists() else "🎬", layout="wide")
load_styles()
st.markdown(
    """
    <style>

    ...
    </style>
    """,
    unsafe_allow_html=True,
)
def get_base64_image(image_path: Path) -> str:
    with image_path.open("rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

logo_html = ""
if LOGO_PATH.exists():
    image_data = get_base64_image(LOGO_PATH)
    logo_html = f'<div class="hero-logo"><img src="data:image/jpeg;base64,{image_data}" alt="CineMind AI logo"></div>'

# --- Navigation (premium top nav; stateful) ---
nav_items = [
    ("Home", "🏠"),
    ("Prediction", "🎬"),
    ("Analytics", "📊"),
    ("Chatbot", "🤖"),
    ("Dataset Info", "🗂"),
    ("About", "ℹ"),
]

if "page" not in st.session_state:
    st.session_state.page = "Home"

with st.container():
    st.markdown('<div class="cnav">', unsafe_allow_html=True)
    cols = st.columns(len(nav_items), gap="small")
    for col, (label, icon) in zip(cols, nav_items):
        with col:
            if st.button(f"{icon} {label}", key=f"nav_{label}"):
                st.session_state.page = label
    st.markdown('</div>', unsafe_allow_html=True)

active_index = [label for label, _ in nav_items].index(st.session_state.page) + 1
st.markdown(
    f"""
    <style>
        .stButton:nth-of-type({active_index})>button {{
            background: linear-gradient(90deg, #D4AF37 0%, #F5D76E 100%) !important;
            color: #0B0B0B !important;
            border-color: rgba(255,255,255,0.22) !important;
            box-shadow: 0 20px 44px rgba(212,175,55,0.24) !important;
        }}
        .stButton:nth-of-type({active_index})>button::after {{
            content: '';
            position: absolute;
            inset: 0;
            border-radius: 16px;
            box-shadow: inset 0 0 0 1px rgba(255,255,255,0.18);
            pointer-events: none;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize model and dashboard data
predictor = MoviePredictor()
df = get_dashboard_data()

if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []
if "prediction_history_df" not in st.session_state:
    st.session_state.prediction_history_df = pd.DataFrame(columns=[
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
    ])
if "show_clear_confirm" not in st.session_state:
    st.session_state.show_clear_confirm = False

# Analytics data summaries
if "genre" in df.columns:
    genre_dist = df["genre"].value_counts().reset_index()
    genre_dist.columns = ["genre", "count"]
else:
    genre_dist = None

if "revenue" in df.columns and "genre" in df.columns:
    revenue_by_genre = df.groupby("genre")["revenue"].mean().reset_index()
else:
    revenue_by_genre = None

budget_vs_revenue_fig = create_budget_vs_revenue_chart(df)

if "success_label" in df.columns:
    success_dist = df["success_label"].value_counts().reset_index()
    success_dist.columns = ["success", "count"]
else:
    success_dist = None

if "release_month" in df.columns and "revenue" in df.columns:
    monthly_revenue = df.groupby("release_month")["revenue"].mean().reset_index()
else:
    monthly_revenue = None


def render_prediction_page():
    st.markdown('<h2 class="section-heading" id="prediction-form">Prediction Form</h2>', unsafe_allow_html=True)
    result_placeholder = st.empty()
    with st.form("prediction_form"):
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        form_col1, form_col2 = st.columns(2)
        with form_col1:
            genre = st.selectbox("Genre", ["Action", "Comedy", "Drama", "Horror", "Sci-Fi", "Romance", "Thriller"])
            budget = st.number_input("Budget", min_value=1000000, value=50000000, step=1000000)
            runtime = st.number_input("Runtime (minutes)", min_value=70, value=120, step=1)
        with form_col2:
            release_month = st.number_input("Release Month", min_value=1, max_value=12, value=6, step=1)
            popularity_score = st.number_input("Popularity Score", min_value=0.0, max_value=100.0, value=50.0, step=1.0)
        submit_prediction = st.form_submit_button("Predict Now")
        st.markdown('</div>', unsafe_allow_html=True)

    if submit_prediction:
        input_data = {
            "genre": genre,
            "budget": budget,
            "runtime": runtime,
            "release_month": release_month,
            "popularity_score": popularity_score,
        }

        with st.spinner("Analyzing production potential..."):
            progress_bar = st.progress(0)
            for pct in [12, 28, 52, 76, 100]:
                time.sleep(0.06)
                progress_bar.progress(pct)
            prediction, probabilities = predictor.predict(input_data)

        top_prob = max(probabilities.values()) if probabilities else 0
        confidence = "High" if top_prob >= 0.75 else "Medium" if top_prob >= 0.55 else "Low"
        prediction_html = f'''
        <div class="form-card prediction-result-card">
            <h3>Prediction Result</h3>
            <p><strong>{prediction}</strong></p>
            <div class="progress-bar"><div class="progress-fill" style="width: {top_prob * 100:.1f}%"></div></div>
            <div class="progress-label">Probability: {top_prob * 100:.1f}%</div>
            <div class="confidence-badge">{confidence} Confidence</div>
        </div>
        '''
        result_placeholder.markdown(prediction_html, unsafe_allow_html=True)

        add_prediction_to_history(
            genre=genre,
            budget=budget,
            runtime=runtime,
            release_month=release_month,
            popularity_score=popularity_score,
            prediction=prediction,
            probability=top_prob,
            confidence=confidence,
        )

        try:
            import pandas as _pd
            input_df_for_xai = _pd.DataFrame([input_data])[FEATURE_COLUMNS]
            encoded_prediction = predictor.model.predict(input_df_for_xai)[0]
            render_explanation(predictor.model, input_df_for_xai, encoded_prediction, predictor.label_encoder)
        except Exception as e:
            st.warning(f"Explanation unavailable: {e}")


def render_analytics_page():
    with st.container():
        st.markdown('<h2 class="section-heading">Analytics Dashboard</h2>', unsafe_allow_html=True)
        chart_col1, chart_col2 = st.columns(2)
        if genre_dist is not None:
            chart_col1.plotly_chart(create_genre_chart(df), use_container_width=True)
        if revenue_by_genre is not None:
            chart_col2.plotly_chart(create_revenue_chart(df), use_container_width=True)
        if budget_vs_revenue_fig is not None:
            chart_col1.plotly_chart(budget_vs_revenue_fig, use_container_width=True)
        if success_dist is not None:
            import plotly.express as px
            success_fig = px.pie(success_dist, names="success", values="count", title="Movie Success Distribution", hole=0.4, color_discrete_sequence=["#D4AF37", "#BBA657", "#867636"])
            chart_col2.plotly_chart(success_fig, use_container_width=True)
        if monthly_revenue is not None:
            import plotly.express as px
            monthly_fig = px.line(monthly_revenue, x="release_month", y="revenue", title="Monthly Revenue Trend", markers=True, template="plotly_dark")
            monthly_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#FFFFFF")
            st.plotly_chart(monthly_fig, use_container_width=True)


def render_dataset_page():
    with st.container():
        st.markdown('<h2 class="section-heading">📊 Dataset Info</h2>', unsafe_allow_html=True)
        st.markdown('<p style="max-width:1200px;margin:0 auto 1rem;color:#CFC9B7;">Summary statistics and dataset information used to train the machine learning models.</p>', unsafe_allow_html=True)

        st.markdown(
            '''
            <style>
            .dataset-card { background: rgba(255,255,255,0.02); border-radius: 18px; padding: 1rem; max-width:1200px; margin:0 auto 1rem; border: 1px solid rgba(212,175,55,0.08); box-shadow: 0 12px 28px rgba(0,0,0,0.4); }
            .dataset-card table { width:100%; border-collapse: collapse; }
            .dataset-card table th { color: #D4AF37; text-align:left; padding:0.6rem 0.8rem; font-weight:700; }
            .dataset-card table td { color: #FFFFFF; padding:0.6rem 0.8rem; }
            .dataset-card table tr:nth-child(even) td { background: rgba(255,255,255,0.02); }
            .dataset-card table tr:hover td { background: rgba(212,175,55,0.04); }
            .info-box { background: rgba(255,255,255,0.02); border-left: 4px solid #D4AF37; padding: 1rem; border-radius: 10px; color: #FFFFFF; max-width:1200px; margin:0 auto; }
            .dataset-search { max-width:1200px; margin:0 auto 0.75rem; }
            </style>
            ''',
            unsafe_allow_html=True,
        )

        dataset_info = {
            "Property": [
                "Dataset Type",
                "Learning Type",
                "Problem Type",
                "Total Movies",
                "Features Used",
                "Target Classes",
                "Algorithms Trained",
                "Best Model Selection Metric",
            ],
            "Value": [
                "Structured Tabular Dataset",
                "Supervised Learning",
                "Multi-Class Classification",
                "10,000+",
                "5",
                "Hit, Average, Flop",
                "Logistic Regression, Decision Tree, Random Forest",
                "F1 Score",
            ],
        }
        info_df = pd.DataFrame(dataset_info)
        st.markdown('<div class="dataset-card">', unsafe_allow_html=True)
        st.subheader('Dataset Information')
        st.table(info_df)
        st.markdown('</div>', unsafe_allow_html=True)

        features = {
            "Feature": ["Genre", "Budget", "Runtime", "Release Month", "Popularity Score"],
            "Data Type": ["Categorical", "Numerical", "Numerical", "Numerical", "Numerical"],
            "Description": [
                "Type of movie",
                "Production budget",
                "Movie duration in minutes",
                "Month of release",
                "Popularity indicator",
            ],
        }
        features_df = pd.DataFrame(features)
        st.markdown('<div class="dataset-card">', unsafe_allow_html=True)
        st.subheader('Features Used')
        st.table(features_df)
        st.markdown('<strong>Target Variable:</strong> Success<br><strong>Possible Classes:</strong><ul style="margin:0.25rem 0 0.75rem;padding-left:1.1rem;"><li>Hit</li><li>Average</li><li>Flop</li></ul>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        stats = {
            "Metric": ["Average Budget", "Average Revenue", "Number of Genres", "Most Common Genre", "Missing Values", "Training Samples", "Testing Samples"],
            "Value": ["$55M", "$102M", "20", "Action", "0", "8,000", "2,000"],
        }
        stats_df = pd.DataFrame(stats)
        st.markdown('<div class="dataset-card">', unsafe_allow_html=True)
        st.subheader('Dataset Statistics')
        st.table(stats_df)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="dataset-search">', unsafe_allow_html=True)
        st.subheader('🎬 Sample Dataset Records')
        st.markdown('<p style="color:#CFC9B7;margin-top:0.25rem;">Use the search box to filter records (searches across displayed columns).</p>', unsafe_allow_html=True)
        search_query = st.text_input('Search dataset (Genre, Budget, Runtime, Release Month, Popularity)', '')
        preview_cols = [c for c in ["genre", "budget", "runtime", "release_month", "popularity_score", "success_label"] if c in df.columns]
        preview_df = df[preview_cols].copy() if preview_cols else df.copy()
        preview_df = preview_df.rename(columns={
            k: ("Genre" if k=="genre" else "Budget" if k=="budget" else "Runtime" if k=="runtime" else "Release Month" if k=="release_month" else "Popularity" if k=="popularity_score" else "Success" ) for k in preview_df.columns
        })
        if search_query:
            sq = str(search_query).lower()
            mask = preview_df.astype(str).apply(lambda row: row.str.lower().str.contains(sq)).any(axis=1)
            filtered = preview_df[mask]
        else:
            filtered = preview_df
        st.dataframe(filtered.head(5), height=260)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="info-box" style="margin-top:0.8rem;">', unsafe_allow_html=True)
        st.markdown('<strong>💡 Why This Dataset Matters</strong>', unsafe_allow_html=True)
        st.markdown('<p style="margin:0.5rem 0 0;">The machine learning models learn patterns from historical movie data. Features such as genre, budget, runtime, release month, and popularity score help the AI predict whether a movie is likely to become a Hit, Average, or Flop.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


def render_about_page():
    st.header("About CineMind AI")
    st.write(
        "CineMind AI is a premium Streamlit application that predicts movie success and delivers executive-level analytics for movie development teams."
    )
    st.write(
        "This product offers an intuitive dashboard for exploring how genre, budget, runtime, release timing, and audience popularity influence commercial outcomes. It focuses on clear model explanation, scenario planning, and practical decision support."
    )

    st.markdown("---")
    st.subheader("Contact")
    st.markdown(
        """
        - **Email:** heritier@example.com
        - **Portfolio:** https://www.example.com
        - **LinkedIn:** https://www.linkedin.com/in/heritier
        """
    )
    st.write("CineMind AI — a concise product showcase for movie analytics and predictive storytelling.")

# Page dispatch
if st.session_state.page == "Home":
    render_home_page()
elif st.session_state.page == "Prediction":
    render_prediction_page()
elif st.session_state.page == "Analytics":
    render_analytics_page()
elif st.session_state.page == "Chatbot":
    with st.container():
        render_cinemind_assistant()
elif st.session_state.page == "Dataset Info":
    render_dataset_page()
elif st.session_state.page == "About":
    render_about_page()
else:
    st.markdown(f'<div style="padding:18px 8px;"><h2 style="color:#FFFFFF;margin:0.2rem 0;">{st.session_state.page}</h2></div>', unsafe_allow_html=True)

# What-If Simulator: render before footer
try:
    if not df.empty:
        current_row = df.iloc[0].to_dict()
        current_input = {k: current_row.get(k, None) for k in FEATURE_COLUMNS}
        render_what_if(current_input, predictor)
except Exception as e:
    st.warning(f"What-If Simulator unavailable: {e}")

with st.container():
    render_ai_processing_panel()
