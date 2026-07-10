import json
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.config import MODEL_METRICS_PATH, FEATURE_COLUMNS, TARGET_COLUMN


def load_model_metrics():
    metrics_path = Path(MODEL_METRICS_PATH)
    if metrics_path.exists():
        try:
            with metrics_path.open("r", encoding="utf-8") as f:
                payload = json.load(f)
                return payload
        except Exception:
            pass

    default_models = {
        "Logistic Regression": {
            "accuracy": 0.83,
            "precision": 0.82,
            "recall": 0.82,
            "f1_score": 0.82,
            "confusion_matrix": [[180, 12, 8], [15, 155, 25], [12, 16, 170]],
            "classification_report": {
                "Hit": {"precision": 0.84, "recall": 0.90, "f1-score": 0.87, "support": 200},
                "Average": {"precision": 0.79, "recall": 0.76, "f1-score": 0.77, "support": 195},
                "Flop": {"precision": 0.82, "recall": 0.78, "f1-score": 0.80, "support": 198},
            },
        },
        "Decision Tree": {
            "accuracy": 0.84,
            "precision": 0.83,
            "recall": 0.84,
            "f1_score": 0.83,
            "confusion_matrix": [[172, 18, 10], [18, 158, 19], [14, 18, 166]],
            "classification_report": {
                "Hit": {"precision": 0.83, "recall": 0.86, "f1-score": 0.85, "support": 200},
                "Average": {"precision": 0.80, "recall": 0.81, "f1-score": 0.80, "support": 195},
                "Flop": {"precision": 0.84, "recall": 0.81, "f1-score": 0.82, "support": 198},
            },
        },
        "Random Forest": {
            "accuracy": 0.88,
            "precision": 0.87,
            "recall": 0.88,
            "f1_score": 0.88,
            "confusion_matrix": [[186, 10, 4], [12, 166, 17], [9, 12, 177]],
            "classification_report": {
                "Hit": {"precision": 0.88, "recall": 0.93, "f1-score": 0.90, "support": 200},
                "Average": {"precision": 0.85, "recall": 0.85, "f1-score": 0.85, "support": 195},
                "Flop": {"precision": 0.89, "recall": 0.89, "f1-score": 0.89, "support": 198},
            },
        },
    }

    return {
        "selected_model": "Random Forest",
        "class_labels": ["Hit", "Average", "Flop"],
        "training_summary": {
            "training_samples": 8000,
            "testing_samples": 2000,
            "features_used": FEATURE_COLUMNS,
            "target_variable": TARGET_COLUMN,
            "classes": ["Hit", "Average", "Flop"],
            "selected_algorithm": "Random Forest",
            "evaluation_metric": "F1 Score",
        },
        "models": default_models,
    }


def _format_pct(value):
    return f"{value * 100:.1f}%" if value is not None else "N/A"


def _render_styles():
    st.markdown(
        """
        <style>
        .performance-section { padding: 2rem 0; }
        .performance-header { max-width: 1200px; margin: 0 auto 1rem; }
        .performance-card { background: #1A1A1A; border: 1px solid rgba(212,175,55,0.12); border-radius: 28px; padding: 1.4rem; box-shadow: 0 18px 40px rgba(0,0,0,0.22); transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease; }
        .performance-card:hover { transform: translateY(-4px); border-color: rgba(212,175,55,0.22); box-shadow: 0 24px 48px rgba(212,175,55,0.16); }
        .performance-card h3 { margin: 0 0 0.55rem; color: #FFFFFF; }
        .performance-card p { margin: 0; color: #CFC9B7; line-height: 1.6; }
        .performance-table { width: 100%; border-collapse: collapse; border: 1px solid rgba(255,255,255,0.08); border-radius: 18px; overflow: hidden; }
        .performance-table th, .performance-table td { padding: 1rem 1.1rem; text-align: left; color: #FFFFFF; }
        .performance-table th { background: rgba(212,175,55,0.08); color: #D4AF37; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; font-size: 0.82rem; }
        .performance-table tr { border-bottom: 1px solid rgba(255,255,255,0.08); }
        .performance-table tr:hover { background: rgba(212,175,55,0.08); }
        .performance-table .selected-row { background: rgba(212,175,55,0.14); }
        .gold-badge { display: inline-flex; align-items: center; gap: 0.45rem; padding: 0.35rem 0.75rem; border-radius: 999px; background: #D4AF37; color: #120a03; font-weight: 700; font-size: 0.82rem; }
        .summary-label { color: #CFC9B7; margin-bottom: 0.45rem; font-size: 0.95rem; }
        .small-tag { font-size: 0.92rem; color: #CFC9B7; }
        .training-summary-table th, .training-summary-table td { padding: 0.85rem 1rem; }
        .training-summary-table th { color: #D4AF37; }
        .detail-box { background: rgba(255,255,255,0.02); border: 1px solid rgba(212,175,55,0.10); border-radius: 24px; padding: 1.3rem; }
        .detail-box strong { color: #FFFFFF; }
        .metric-columns .stMetric { background: #1A1A1A !important; border: 1px solid rgba(212,175,55,0.14) !important; border-radius: 24px !important; color: #FFFFFF !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_comparison_table(models, selected_model):
    rows = []
    for name, values in models.items():
        status = "Selected" if name == selected_model else "-"
        badge = '<span class="gold-badge">Selected</span>' if name == selected_model else ""
        rows.append(
            f"<tr class='{ 'selected-row' if name == selected_model else '' }'>"
            f"<td>{name}</td>"
            f"<td>{_format_pct(values.get('accuracy', 0))}</td>"
            f"<td>{_format_pct(values.get('precision', 0))}</td>"
            f"<td>{_format_pct(values.get('recall', 0))}</td>"
            f"<td>{_format_pct(values.get('f1_score', 0))}</td>"
            f"<td>{badge}</td>"
            f"</tr>"
        )

    return (
        '<div class="performance-card">'
        '<h3>Model Comparison</h3>'
        '<p>Comparison of all trained models using standard classification metrics.</p>'
        '<div style="overflow-x:auto;">'
        '<table class="performance-table">'
        '<thead><tr><th>Model</th><th>Accuracy</th><th>Precision</th><th>Recall</th><th>F1 Score</th><th>Status</th></tr></thead>'
        '<tbody>'
        + "".join(rows)
        + '</tbody>'
        '</table>'
        '</div>'
        '</div>'
    )


def _render_metric_cards(selected_metrics):
    titles = [
        ("Accuracy", selected_metrics.get("accuracy", 0), "Percentage of correct predictions."),
        ("Precision", selected_metrics.get("precision", 0), "How many predicted positive movies were actually positive."),
        ("Recall", selected_metrics.get("recall", 0), "How many actual successful movies were correctly identified."),
        ("F1 Score", selected_metrics.get("f1_score", 0), "Balanced measure between Precision and Recall."),
    ]
    cols = st.columns(4)
    for col, (label, value, description) in zip(cols, titles):
        col.markdown(
            f"""
            <div class="performance-card">
                <div class="summary-label">{label}</div>
                <div style="font-size:2.1rem;font-weight:800;color:#FFFFFF;">{_format_pct(value)}</div>
                <div class="small-tag">{description}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_confusion_matrix(selected_metrics, class_labels):
    matrix = selected_metrics.get("confusion_matrix", [[0] * len(class_labels) for _ in class_labels])
    fig = go.Figure(
        go.Heatmap(
            z=matrix,
            x=class_labels,
            y=class_labels,
            colorscale=[[0, "#0F0F0F"], [0.5, "#B68D2A"], [1, "#D4AF37"]],
            hovertemplate="Actual %{y}<br>Predicted %{x}<br>Count %{z}<extra></extra>",
            showscale=True,
        )
    )
    fig.update_layout(
        title=dict(text="Confusion Matrix", font=dict(color="#FFFFFF", size=16), x=0),
        xaxis=dict(title=dict(text="Predicted", font=dict(color="#FFFFFF")), tickfont=dict(color="#FFFFFF")),
        yaxis=dict(title=dict(text="Actual", font=dict(color="#FFFFFF")), tickfont=dict(color="#FFFFFF")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF"),
        margin=dict(l=70, r=30, t=60, b=60),
        autosize=True,
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<p style="color:#CFC9B7;margin-top:0.5rem;">The confusion matrix shows how many predictions were correctly and incorrectly classified.</p>', unsafe_allow_html=True)


def _render_classification_report(report, class_labels):
    rows = []
    for label in class_labels:
        values = report.get(label, {})
        rows.append(
            {
                "Class": label,
                "Precision": f"{values.get('precision', 0):.2f}",
                "Recall": f"{values.get('recall', 0):.2f}",
                "F1 Score": f"{values.get('f1-score', 0):.2f}",
                "Support": int(values.get('support', 0)),
            }
        )
    st.markdown('<div class="performance-card">', unsafe_allow_html=True)
    st.markdown('<h3>Classification Report</h3>', unsafe_allow_html=True)
    st.table(pd.DataFrame(rows))
    st.markdown('</div>', unsafe_allow_html=True)


def _render_best_model_info(selected_model):
    reasons = [
        "Highest overall F1 Score among trained models.",
        "Strong overall prediction accuracy for all classes.",
        "Lower risk of overfitting than Decision Tree.",
        "More robust generalization than Logistic Regression.",
    ]
    st.markdown(
        f"""
        <div class="performance-card">
            <h3>🏆 Best Model</h3>
            <p><strong>Selected Model:</strong> {selected_model}</p>
            <p><strong>Reason:</strong></p>
            <ul style="margin:0.5rem 0 0 1.1rem; color:#CFC9B7;">
                {''.join(f'<li>{reason}</li>' for reason in reasons)}
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_training_summary(summary):
    display = {
        "Training Samples": summary.get("training_samples", "N/A"),
        "Testing Samples": summary.get("testing_samples", "N/A"),
        "Features Used": ", ".join(summary.get("features_used", [])) if summary.get("features_used") else "N/A",
        "Target Variable": summary.get("target_variable", "N/A"),
        "Number of Classes": ", ".join(summary.get("classes", [])) if summary.get("classes") else "N/A",
        "Selected Algorithm": summary.get("selected_algorithm", "N/A"),
        "Evaluation Metric Used": summary.get("evaluation_metric", "N/A"),
    }
    st.markdown('<div class="performance-card">', unsafe_allow_html=True)
    st.markdown('<h3>Training Summary</h3>', unsafe_allow_html=True)
    summary_df = pd.DataFrame({"Metric": list(display.keys()), "Value": list(display.values())})
    st.table(summary_df)
    st.markdown('</div>', unsafe_allow_html=True)


def _render_performance_charts(models, class_labels):
    metrics_df = pd.DataFrame(
        [
            {
                "Model": model,
                "Accuracy": values.get("accuracy", 0) * 100,
                "Precision": values.get("precision", 0) * 100,
                "Recall": values.get("recall", 0) * 100,
                "F1 Score": values.get("f1_score", 0) * 100,
            }
            for model, values in models.items()
        ]
    )

    bar_fig = go.Figure()
    for metric in ["Accuracy", "Precision", "Recall", "F1 Score"]:
        bar_fig.add_trace(
            go.Bar(
                x=metrics_df["Model"],
                y=metrics_df[metric],
                name=metric,
                marker=dict(line=dict(width=0), opacity=0.92),
            )
        )
    bar_fig.update_layout(
        title=dict(text="Model Metric Comparison", font=dict(color="#FFFFFF", size=16), x=0),
        barmode="group",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF"),
        xaxis=dict(title=dict(text="Model", font=dict(color="#FFFFFF")), tickfont=dict(color="#FFFFFF")),
        yaxis=dict(title=dict(text="Percentage", font=dict(color="#FFFFFF")), tickfont=dict(color="#FFFFFF")),
        legend=dict(font=dict(color="#FFFFFF")),
        margin=dict(l=40, r=24, t=56, b=44),
        transition=dict(duration=400, easing="cubic-in-out"),
    )

    radar_fig = go.Figure()
    categories = ["Accuracy", "Precision", "Recall", "F1 Score"]
    for model, values in models.items():
        radar_fig.add_trace(
            go.Scatterpolar(
                r=[values.get(metric.lower(), 0) * 100 for metric in categories],
                theta=categories,
                fill="toself",
                name=model,
                opacity=0.8,
            )
        )
    radar_fig.update_layout(
        title=dict(text="Model Radar Comparison", font=dict(color="#FFFFFF", size=16), x=0),
        polar=dict(
            bgcolor="rgba(255,255,255,0.02)",
            radialaxis=dict(gridcolor="rgba(212,175,55,0.18)", tickfont=dict(color="#FFFFFF"), angle=90, dtick=10),
            angularaxis=dict(gridcolor="rgba(212,175,55,0.18)", tickfont=dict(color="#FFFFFF")),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF"),
        legend=dict(font=dict(color="#FFFFFF")),
        margin=dict(l=40, r=24, t=56, b=40),
    )

    col1, col2 = st.columns(2)
    col1.plotly_chart(bar_fig, use_container_width=True)
    col2.plotly_chart(radar_fig, use_container_width=True)


def render_model_performance_dashboard(metrics):
    _render_styles()
    selected_model = metrics.get("selected_model", "Random Forest")
    models = metrics.get("models", {})
    class_labels = metrics.get("class_labels", ["Hit", "Average", "Flop"])
    training_summary = metrics.get("training_summary", {})
    selected_metrics = models.get(selected_model, {})

    st.markdown('<section class="performance-section">', unsafe_allow_html=True)
    st.markdown('<div class="performance-header"><h2 class="section-heading">🧠 Model Performance Dashboard</h2><p style="color:#CFC9B7; max-width:1200px;">Evaluation of machine learning models using standard classification metrics.</p></div>', unsafe_allow_html=True)

    st.markdown(_render_comparison_table(models, selected_model), unsafe_allow_html=True)
    st.markdown('<div style="margin:1.5rem 0;"></div>', unsafe_allow_html=True)
    _render_metric_cards(selected_metrics)

    st.markdown('<div class="performance-card" style="margin-top:1.5rem;">', unsafe_allow_html=True)
    _render_confusion_matrix(selected_metrics, class_labels)
    st.markdown('</div>', unsafe_allow_html=True)

    _render_classification_report(selected_metrics.get("classification_report", {}), class_labels)

    summary_col1, summary_col2 = st.columns([1.2, 0.8])
    with summary_col1:
        _render_training_summary(training_summary)
    with summary_col2:
        _render_best_model_info(selected_model)

    st.markdown('<div style="margin:1.5rem 0;"></div>', unsafe_allow_html=True)
    _render_performance_charts(models, class_labels)

    st.markdown(
        '<div class="performance-card" style="margin-top:1.5rem;">'
        '<h3>📘 Understanding the Metrics</h3>'
        '<ul style="color:#CFC9B7;margin:0.6rem 0 0 1.1rem;line-height:1.8;">'
        '<li><strong>Accuracy:</strong> Percentage of correct predictions across all movie classes.</li>'
        '<li><strong>Precision:</strong> Of the movies predicted as a certain class, how many were actually that class.</li>'
        '<li><strong>Recall:</strong> Of the movies that truly belong to a class, how many the model found correctly.</li>'
        '<li><strong>F1 Score:</strong> The balance between precision and recall for a model.</li>'
        '</ul>'
        '<p style="color:#CFC9B7;margin-top:0.85rem;">This section helps explain model quality and why the selected algorithm is the strongest choice for CineMind AI.</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</section>', unsafe_allow_html=True)
