"""
Explainable AI helpers for CineMind AI.

This module computes per-feature contributions for a single prediction using a
scikit-learn Pipeline that contains a ColumnTransformer preprocessor and a
classifier (LogisticRegression in the current model). It aggregates transformed
features back to their original feature groups (Genre, Budget, Runtime,
Release Month, Popularity) and returns percentage contributions that are
rendered by the UI.

All important lines include comments so you can explain them during your viva.
"""
from typing import Dict, Any
import numpy as np
import pandas as pd
import streamlit as st

from src.config import FEATURE_COLUMNS
from components.feature_importance_chart import render_feature_importance_chart


def _group_transformed_name(name: str) -> str:
    """Map a transformed feature name back to a readable original feature group.

    The project's ColumnTransformer prefixes transformed names such as
    'cat__genre_Action' for one-hot encoded genres and 'num__budget' for
    numeric features. We map them to the user-facing groups.
    """
    if name.startswith("cat__genre_"):
        return "Genre"
    if name.startswith("num__"):
        # num__budget -> Budget
        return name.split("__", 1)[1].replace("_", " ").title()
    # fallback
    return name


def compute_contributions(pipeline, input_df: pd.DataFrame, encoded_prediction) -> Dict[str, Any]:
    """Compute signed and percentage contributions per original feature.

    Returns a dict keyed by original feature group with values containing:
      - pct: percentage of total absolute contribution
      - signed: signed contribution in log-odds units
      - raw_value: original input value (if available)
    """
    # Extract preprocessor and classifier from Pipeline
    preprocessor = pipeline.named_steps.get("preprocessor")
    # classifier might be named 'classifier' or be the last step
    classifier = pipeline.named_steps.get("classifier") if "classifier" in pipeline.named_steps else pipeline.steps[-1][1]

    # Get transformed feature names (ColumnTransformer provides this)
    transformed_names = preprocessor.get_feature_names_out(FEATURE_COLUMNS)

    # Transform the single input row to the model's numeric feature space
    X_trans = preprocessor.transform(input_df)
    # ensure 1-D vector for the single row
    x_vec = np.asarray(X_trans).reshape(-1)

    # For multiclass logistic regression, coef_ has shape (n_classes, n_features)
    # Find the index of the predicted encoded class
    class_list = list(classifier.classes_)
    cls_index = class_list.index(int(encoded_prediction)) if isinstance(encoded_prediction, (int, np.integer)) else class_list.index(encoded_prediction)

    coefs = classifier.coef_
    # Select class-specific coefficients
    coef_vec = np.asarray(coefs[cls_index]).reshape(-1)

    # Signed contribution in log-odds = coefficient * transformed feature value
    signed_contribs = coef_vec * x_vec
    abs_contribs = np.abs(signed_contribs)

    # Aggregate transformed features into original groups
    grouped = {}
    for name, s, a in zip(transformed_names, signed_contribs, abs_contribs):
        group = _group_transformed_name(name)
        if group not in grouped:
            grouped[group] = {"signed": 0.0, "abs": 0.0, "parts": []}
        grouped[group]["signed"] += float(s)
        grouped[group]["abs"] += float(a)
        grouped[group]["parts"].append({"name": name, "signed": float(s), "abs": float(a)})

    # Compute percentage contributions (relative magnitude)
    total_abs = sum(v["abs"] for v in grouped.values()) or 1.0
    contributions = {}
    for g, v in grouped.items():
        pct = (v["abs"] / total_abs) * 100.0
        # raw input value if available
        raw_val = None
        if g in input_df.columns:
            raw_val = input_df.iloc[0][g]
        contributions[g] = {"pct": float(pct), "signed": float(v["signed"]), "raw_value": raw_val, "parts": v["parts"]}

    return contributions


def render_explanation(pipeline, input_df: pd.DataFrame, encoded_prediction, label_encoder):
    """Compute contributions and render the XAI UI: chart + explanation cards.

    Important lines are commented to help you explain why we do each step
    during your viva.
    """
    st.subheader("🤖 Why Did the AI Predict This?")
    st.markdown("<p style='color:#CFC9B7'>Understand which movie features influenced the prediction.</p>", unsafe_allow_html=True)

    # Compute contributions per original feature group
    contributions = compute_contributions(pipeline, input_df, encoded_prediction)

    # Prepare sorted list of (feature, pct) for the chart
    sorted_items = sorted([(k, v["pct"]) for k, v in contributions.items()], key=lambda x: x[1], reverse=True)

    # Render Plotly horizontal bar chart
    fig = render_feature_importance_chart(sorted_items, title="Feature contribution (%)")
    st.plotly_chart(fig, use_container_width=True)

    # Render explanation cards beneath the chart
    cols = st.columns(len(sorted_items) if len(sorted_items) <= 4 else 4)
    # Iterate in decreasing contribution order for consistent UX
    for i, (feature, pct) in enumerate(sorted_items):
        col = cols[i % len(cols)]
        info = contributions[feature]
        # Simple positive/negative phrasing based on signed contribution
        sign = info["signed"]
        if sign > 0:
            verdict = "Contributed +{:.1f}% toward prediction".format(pct)
            reason = {
                "Budget": "High production budgets are historically associated with successful movies.",
                "Popularity": "Popular movies generally achieve better box office performance.",
                "Genre": "Certain genres perform better based on historical patterns.",
                "Release Month": "Movies released during peak seasons tend to perform better.",
                "Runtime": "Runtime had a smaller influence on this prediction.",
            }.get(feature, "This feature increased the model's confidence for the predicted class.")
        else:
            verdict = "Contributed -{:.1f}% against prediction".format(pct)
            reason = "This feature reduced the model's confidence for the predicted class."

        # Card layout — minimal HTML but styled using existing app CSS
        col.markdown(
            f"""
            <div style="background:#1A1A1A;border-radius:12px;padding:12px;margin:6px 0;border:1px solid rgba(212,175,55,0.06);box-shadow:0 10px 24px rgba(0,0,0,0.4);">
                <div style="font-weight:700;color:#D4AF37;margin-bottom:6px;">{feature}</div>
                <div style="font-size:1.05rem;color:#FFFFFF;margin-bottom:6px;"><strong>{pct:.1f}%</strong></div>
                <div style="color:#CFC9B7;font-size:0.95rem">{reason}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Insights summary: build simple bullet points from signed signs
    insights = []
    for feature, data in sorted_items:
        s = contributions[feature]["signed"]
        if s > 0:
            insights.append(f"✓ {feature} increased the probability of success.")
        else:
            insights.append(f"✓ {feature} decreased the probability of success.")

    st.markdown("<div style='max-width:1200px;margin-top:0.6rem;color:#CFC9B7'>" + "<br>".join(insights) + "</div>", unsafe_allow_html=True)
