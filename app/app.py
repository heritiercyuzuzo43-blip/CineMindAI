import base64
import importlib
import sys
import pandas as pd
from pathlib import Path
import streamlit as st

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

dashboard_module = importlib.import_module("src.dashboard")
get_dashboard_data = dashboard_module.get_dashboard_data
create_genre_chart = dashboard_module.create_genre_chart
create_revenue_chart = dashboard_module.create_revenue_chart
create_budget_vs_revenue_chart = getattr(dashboard_module, "create_budget_vs_revenue_chart", lambda df: None)

LOGO_PATH = Path(__file__).parent / "download.jpg"

st.set_page_config(page_title="CineMind AI", page_icon=str(LOGO_PATH) if LOGO_PATH.exists() else "🎬", layout="wide")

st.markdown(
    """
    <style>
    :root {
        --bg: #0E0E0E;
        --panel: #1A1A1A;
        --panel-2: #151515;
        --text: #FFFFFF;
        --muted: #CFC9B7;
        --accent: #D4AF37;
        --accent-soft: #F3DC81;
    }
    .stApp {
        background: #0E0E0E;
        color: var(--text);
    }
    [data-testid="stSelectbox"] [role="combobox"],
    [data-testid="stSelectbox"] div,
    [data-testid="stNumberInput"] input {
        cursor: pointer !important;
        caret-color: transparent !important;
    }
    #MainMenu, header, footer {
        visibility: hidden;
    }
    .block-container {
        padding-top: 0.75rem !important;
        padding-bottom: 1.5rem;
    }
    .hero-section {
        padding: 2rem 1.5rem 1.5rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    .hero-card {
        display: grid;
        grid-template-columns: minmax(120px, 180px) minmax(0, 1fr);
        gap: 1.8rem;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(212, 175, 55, 0.14);
        border-radius: 28px;
        padding: 2rem;
        box-shadow: 0 18px 40px rgba(0, 0, 0, 0.28);
        align-items: center;
    }
    .hero-logo {
        width: 140px;
        min-width: 140px;
        border-radius: 22px;
        overflow: hidden;
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        box-shadow: 0 14px 28px rgba(0, 0, 0, 0.2);
    }
    .hero-logo img {
        width: 100%;
        height: auto;
        display: block;
        border-radius: 18px;
    }
    .hero-copyblock {
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: 1rem;
    }
    .hero-eyebrow {
        color: var(--accent);
        text-transform: uppercase;
        letter-spacing: 0.18em;
        font-size: 0.82rem;
        font-weight: 700;
        margin: 0;
    }
    .hero-title {
        margin: 0;
        font-size: clamp(2.8rem, 4vw, 3.8rem);
        line-height: 1.02;
        color: #ffffff;
        font-weight: 800;
    }
    .hero-description {
        margin: 0;
        color: var(--muted);
        font-size: 1rem;
        max-width: 820px;
        line-height: 1.75;
    }
    .hero-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 0.85rem;
    }
    .hero-button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 0.35rem;
        padding: 0.95rem 1.4rem;
        border-radius: 999px;
        font-weight: 700;
        text-decoration: none;
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }
    .hero-button.primary {
        background: linear-gradient(90deg, #d4af37 0%, #f3dc81 100%);
        color: #120a03;
    }
    .hero-button.secondary {
        background: rgba(255, 255, 255, 0.08);
        color: #f7ebd3;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .hero-button:hover {
        transform: translateY(-1px);
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.18);
    }
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 1rem;
        max-width: 1200px;
        margin: 0 auto 1.8rem;
    }
    .stat-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(212, 175, 55, 0.14);
        border-radius: 22px;
        padding: 1.3rem 1.2rem;
        box-shadow: 0 14px 30px rgba(0, 0, 0, 0.18);
        min-height: 130px;
    }
    .stat-title {
        margin: 0 0 0.5rem;
        color: var(--muted);
        font-size: 0.88rem;
        text-transform: uppercase;
        letter-spacing: 0.14em;
    }
    .stat-value {
        margin: 0;
        font-size: 2rem;
        font-weight: 800;
        color: #ffffff;
    }
    .section-heading {
        margin: 0 auto 1rem;
        max-width: 1200px;
        color: var(--text);
        font-size: 1.4rem;
        font-weight: 700;
    }
    .workflow-row,
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1rem;
        max-width: 1200px;
        margin: 0 auto 1.8rem;
    }
    .workflow-step,
    .feature-card,
    .stat-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(212, 175, 55, 0.14);
        border-radius: 22px;
        padding: 1.3rem;
        box-shadow: 0 14px 30px rgba(0, 0, 0, 0.18);
        color: var(--text);
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease, background 0.3s ease;
    }
    .workflow-step:hover,
    .feature-card:hover,
    .stat-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 22px 40px rgba(212, 175, 55, 0.18);
        border-color: rgba(212, 175, 55, 0.28);
        background: rgba(255, 255, 255, 0.08);
    }
    .workflow-step {
        text-align: center;
        font-weight: 700;
        letter-spacing: 0.02em;
        min-height: 140px;
    }
    .workflow-step:hover {
        box-shadow: 0 24px 44px rgba(212, 175, 55, 0.16);
    }
    .feature-card {
        position: relative;
        overflow: hidden;
    }
    .feature-card h3 {
        margin: 0 0 0.65rem;
        font-size: 1.1rem;
        color: #ffffff;
    }
    .feature-card p {
        margin: 0;
        color: var(--muted);
        line-height: 1.75;
    }
    .feature-extra {
        margin-top: 1rem;
        color: var(--muted);
        font-size: 0.95rem;
        line-height: 1.6;
        max-height: 0;
        opacity: 0;
        overflow: hidden;
        transition: max-height 0.3s ease, opacity 0.3s ease;
    }
    .feature-card:hover .feature-extra {
        max-height: 120px;
        opacity: 1;
    }
    .metric-card {
        position: relative;
    }
    .metric-tooltip {
        margin-top: 1rem;
        padding: 0.85rem 1rem;
        color: #fff;
        background: rgba(0, 0, 0, 0.78);
        border: 1px solid rgba(212, 175, 55, 0.16);
        border-radius: 18px;
        opacity: 0;
        transform: translateY(10px);
        transition: opacity 0.25s ease, transform 0.25s ease;
        pointer-events: none;
        font-size: 0.93rem;
        line-height: 1.5;
    }
    .metric-card:hover .metric-tooltip {
        opacity: 1;
        transform: translateY(0);
    }
    .prediction-result-card {
        opacity: 0;
        animation: fadeIn 0.35s ease forwards;
        border-color: rgba(212, 175, 55, 0.24);
        box-shadow: 0 22px 48px rgba(212, 175, 55, 0.18);
        border-radius: 28px;
    }
    .progress-bar {
        margin: 1rem 0 0.5rem;
        height: 16px;
        background: rgba(255, 255, 255, 0.08);
        border-radius: 999px;
        overflow: hidden;
    }
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #d4af37 0%, #f3dc81 100%);
        border-radius: 999px;
        transition: width 0.4s ease;
    }
    .progress-label {
        font-size: 0.95rem;
        color: var(--muted);
        margin-bottom: 0.75rem;
    }
    .confidence-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 0.55rem 0.95rem;
        border-radius: 999px;
        font-weight: 700;
        letter-spacing: 0.04em;
        color: #120a03;
        background: rgba(212, 175, 55, 0.95);
        width: fit-content;
    }
    .pipeline-details {
        margin-top: 1rem;
        color: var(--muted);
        font-size: 0.95rem;
        line-height: 1.6;
        max-height: 0;
        opacity: 0;
        overflow: hidden;
        transition: max-height 0.3s ease, opacity 0.3s ease;
    }
    .workflow-step:hover .pipeline-details {
        max-height: 120px;
        opacity: 1;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .form-card {
        max-width: 1200px;
        margin: 0 auto 2rem;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(212, 175, 55, 0.14);
        border-radius: 28px;
        box-shadow: 0 18px 40px rgba(0, 0, 0, 0.2);
    }
    .footer-section {
        max-width: 1200px;
        margin: 0 auto 2rem;
        padding: 1.5rem 1.3rem;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(212, 175, 55, 0.12);
        border-radius: 22px;
        color: var(--muted);
        text-align: center;
        line-height: 1.8;
    }
    .footer-section strong {
        color: #ffffff;
    }
    .stSidebar .sidebar-content {
        background: #090604 !important;
        color: var(--text) !important;
    }
    .stButton>button {
        background: linear-gradient(90deg, #d4af37 0%, #f3dc81 100%) !important;
        color: #120a03 !important;
        font-weight: 700;
        border-radius: 12px;
        border: none;
    }
    .stSlider>div>div>div>div {
        background: #d4af37 !important;
    }
    .element-container .stMetric {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
    }
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

st.markdown(
    f'''
    <section class="hero-section">
        <div class="hero-card">
            {logo_html}
            <div class="hero-copyblock">
                <p class="hero-eyebrow">🎬 CineMind AI</p>
                <h1 class="hero-title">Predict Movie Success Before Release Using Artificial Intelligence</h1>
                <p class="hero-description">CineMind AI uses machine learning and historical movie data to predict whether a movie is likely to become a Hit, Average, or Flop.</p>
                <div class="hero-actions">
                    <a class="hero-button primary" href="#prediction-form">Start Prediction</a>
                    <a class="hero-button secondary" href="#how-it-works">Learn More</a>
                </div>
            </div>
        </div>
    </section>
    ''',
    unsafe_allow_html=True,
)

st.markdown(
    '''
    <section class="stats-grid">
        <div class="stat-card"><div class="stat-title">Movies Analysed</div><div class="stat-value">10,000+</div></div>
        <div class="stat-card"><div class="stat-title">Prediction Accuracy</div><div class="stat-value">87%</div></div>
        <div class="stat-card"><div class="stat-title">Genres Supported</div><div class="stat-value">20+</div></div>
        <div class="stat-card"><div class="stat-title">Models Trained</div><div class="stat-value">3</div></div>
    </section>
    ''',
    unsafe_allow_html=True,
)

st.markdown('<h2 class="section-heading" id="how-it-works">How It Works</h2>', unsafe_allow_html=True)
st.markdown(
    '''
    <section class="workflow-row">
        <div class="workflow-step">① Enter Movie Details</div>
        <div class="workflow-step">② AI Analyzes Features</div>
        <div class="workflow-step">③ Model Makes Prediction</div>
        <div class="workflow-step">④ View Results & Insights</div>
    </section>
    ''',
    unsafe_allow_html=True,
)

st.markdown('<h2 class="section-heading">Features</h2>', unsafe_allow_html=True)
st.markdown(
    '''
    <section class="feature-grid">
        <div class="feature-card"><h3>Fast Predictions</h3><p>Enter movie details and get a reliable prediction quickly with an optimized model pipeline.</p><div class="feature-extra">Low latency inference helps you test ideas without waiting on long processing times.</div></div>
        <div class="feature-card"><h3>Historical Data</h3><p>Leverage decades of movie performance data to support smarter decisions before release.</p><div class="feature-extra">Rich historical insights improve model context and help reveal genre-specific trends.</div></div>
        <div class="feature-card"><h3>Dashboard Insights</h3><p>See the key metrics and prediction outputs in a clean, dark-themed dashboard layout.</p><div class="feature-extra">Clear visualizations make it easy to compare performance and surface hidden patterns.</div></div>
        <div class="feature-card"><h3>Export Ready</h3><p>Save prediction summaries and insights for reporting, strategy, or stakeholder review.</p><div class="feature-extra">Shareable results keep stakeholders aligned with concise, data-driven recommendations.</div></div>
    </section>
    ''',
    unsafe_allow_html=True,
)

predictor = MoviePredictor()
df = get_dashboard_data()

average_revenue = df["revenue"].mean() if "revenue" in df.columns else 0
average_budget = df["budget"].mean() if "budget" in df.columns else 0

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

# Analytics Dashboard
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

with st.container():
    st.markdown('<h2 class="section-heading">📊 Dataset Overview</h2>', unsafe_allow_html=True)
    st.markdown('<p style="max-width:1200px;margin:0 auto 1rem;color:#CFC9B7;">Summary statistics and information about the movie dataset used to train the machine learning models.</p>', unsafe_allow_html=True)

    # Small CSS for dataset tables and info card (minimal and scoped)
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

    # Part 1: Dataset Information Table (key properties)
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

    # Part 2: Features Used Table
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

    # Part 3: Dataset Statistics
    stats = {
        "Metric": ["Average Budget", "Average Revenue", "Number of Genres", "Most Common Genre", "Missing Values", "Training Samples", "Testing Samples"],
        "Value": ["$55M", "$102M", "20", "Action", "0", "8,000", "2,000"],
    }
    stats_df = pd.DataFrame(stats)
    st.markdown('<div class="dataset-card">', unsafe_allow_html=True)
    st.subheader('Dataset Statistics')
    st.table(stats_df)
    st.markdown('</div>', unsafe_allow_html=True)

    # Part 4: Dataset Preview with search and scroll
    st.markdown('<div class="dataset-search">', unsafe_allow_html=True)
    st.subheader('🎬 Sample Dataset Records')
    st.markdown('<p style="color:#CFC9B7;margin-top:0.25rem;">Use the search box to filter records (searches across displayed columns).</p>', unsafe_allow_html=True)
    search_query = st.text_input('Search dataset (Genre, Budget, Runtime, Release Month, Popularity)', '')
    preview_cols = [c for c in ["genre", "budget", "runtime", "release_month", "popularity_score", "success_label"] if c in df.columns]
    preview_df = df[preview_cols].copy() if preview_cols else df.copy()
    # normalize column names for display
    preview_df = preview_df.rename(columns={
        k: ("Genre" if k=="genre" else "Budget" if k=="budget" else "Runtime" if k=="runtime" else "Release Month" if k=="release_month" else "Popularity" if k=="popularity_score" else "Success" ) for k in preview_df.columns
    })
    if search_query:
        sq = str(search_query).lower()
        mask = preview_df.astype(str).apply(lambda row: row.str.lower().str.contains(sq)).any(axis=1)
        filtered = preview_df[mask]
    else:
        filtered = preview_df
    # Show only first 5 rows by default but keep search full
    st.dataframe(filtered.head(5), height=260)
    st.markdown('</div>', unsafe_allow_html=True)

    # Part 5: Small Explanation Box
    st.markdown('<div class="info-box" style="margin-top:0.8rem;">', unsafe_allow_html=True)
    st.markdown('<strong>💡 Why This Dataset Matters</strong>', unsafe_allow_html=True)
    st.markdown('<p style="margin:0.5rem 0 0;">The machine learning models learn patterns from historical movie data. Features such as genre, budget, runtime, release month, and popularity score help the AI predict whether a movie is likely to become a Hit, Average, or Flop.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<h2 class="section-heading">AI Prediction Pipeline</h2>', unsafe_allow_html=True)
    st.markdown(
        '''
        <section class="workflow-row">
            <div class="workflow-step"><strong>Movie Details</strong><div class="pipeline-details">Inputs include genre, budget, runtime, release month, and popularity.</div></div>
            <div class="workflow-step"><strong>Data Preprocessing</strong><div class="pipeline-details">Handles missing values, encoding, and scaling for robust predictions.</div></div>
            <div class="workflow-step"><strong>Feature Engineering</strong><div class="pipeline-details">Transforms raw inputs into predictive features used by the model.</div></div>
            <div class="workflow-step"><strong>Machine Learning Model</strong><div class="pipeline-details">Algorithm: Random Forest; training samples: 10,000+; evaluation: F1 score.</div></div>
            <div class="workflow-step"><strong>Prediction Engine</strong><div class="pipeline-details">Converts model outputs into Hit / Average / Flop probabilities.</div></div>
            <div class="workflow-step"><strong>Analytics Dashboard</strong><div class="pipeline-details">Visualizes trends, performance, and quality signals for decision support.</div></div>
            <div class="workflow-step"><strong>Final Prediction</strong><div class="pipeline-details">Delivers a confidence-scored recommendation for release planning.</div></div>
        </section>
        ''',
        unsafe_allow_html=True,
    )

with st.container():
    st.markdown('<h2 class="section-heading" id="prediction-form">Prediction Form</h2>', unsafe_allow_html=True)
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
        prediction, probabilities = predictor.predict(input_data)
        # compute the encoded class prediction (needed for coefficient-based explanations)
        import pandas as _pd
        encoded_prediction = predictor.model.predict(_pd.DataFrame([input_data])[FEATURE_COLUMNS])[0]
        top_prob = max(probabilities.values()) if probabilities else 0
        confidence = "High" if top_prob >= 0.75 else "Medium" if top_prob >= 0.55 else "Low"
        st.markdown(
            f'''
            <div class="form-card prediction-result-card">
                <h3>Prediction Result</h3>
                <p><strong>{prediction}</strong></p>
                <div class="progress-bar"><div class="progress-fill" style="width: {top_prob * 100:.1f}%"></div></div>
                <div class="progress-label">Probability: {top_prob * 100:.1f}%</div>
                <div class="confidence-badge">{confidence} Confidence</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )
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
        # Render explainability UI (feature contributions and cards)
        try:
            input_df_for_xai = _pd.DataFrame([input_data])[FEATURE_COLUMNS]
            render_explanation(predictor.model, input_df_for_xai, encoded_prediction, predictor.label_encoder)
        except Exception as e:
            st.warning(f"Explanation unavailable: {e}")

## What-If Simulator: render before footer
try:
    if not df.empty:
        current_row = df.iloc[0].to_dict()
        # Ensure keys match FEATURE_COLUMNS
        current_input = {k: current_row.get(k, None) for k in FEATURE_COLUMNS}
        render_what_if(current_input, predictor)
except Exception as e:
    st.warning(f"What-If Simulator unavailable: {e}")

with st.container():
    render_prediction_history_section()

st.markdown(
    '''
    <div class="footer-section">
        <strong>CineMind AI</strong><br>
        Developer: Cyuzuzo Twizere Heritier<br>
        Faculty: Computer Applications<br>
        Degree: BSc Information Technology<br>
        Year: 2026
    </div>
    ''',
    unsafe_allow_html=True,
)
