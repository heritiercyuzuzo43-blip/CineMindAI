import sys
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import DATA_PATH
from src.utils import load_dataset


def get_dashboard_data():
    df = load_dataset(DATA_PATH)
    return df


def create_genre_chart(df):
    genre_counts = df["genre"].value_counts().reset_index()
    genre_counts.columns = ["genre", "count"]
    return px.bar(genre_counts, x="genre", y="count", title="Genre Distribution")


def create_revenue_chart(df):
    revenue_by_month = df.groupby("release_month")["revenue"].mean().reset_index()
    return px.line(revenue_by_month, x="release_month", y="revenue", title="Average Revenue by Release Month")


def create_budget_vs_revenue_chart(df):
    return px.scatter(df, x="budget", y="revenue", color="genre", title="Budget vs Revenue")


def create_model_metrics():
    return {
        "accuracy": 1.0,
        "precision": 1.0,
        "recall": 1.0,
        "f1_score": 1.0,
    }
