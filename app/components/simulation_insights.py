from typing import Dict
import streamlit as st

from components.explainable_ai import compute_contributions


def generate_simulation_insights(pipeline, orig_input: Dict, sim_input: Dict):
    """Generate simple human-readable insights comparing original and simulated inputs.

    We compute contributions before and after and then describe the direction
    of change for any feature that was modified by the user.
    """
    import pandas as pd

    orig_df = pd.DataFrame([orig_input])
    sim_df = pd.DataFrame([sim_input])

    encoded_orig = pipeline.predict(orig_df)[0]
    encoded_sim = pipeline.predict(sim_df)[0]

    contrib_before = compute_contributions(pipeline, orig_df, encoded_orig)
    contrib_after = compute_contributions(pipeline, sim_df, encoded_sim)

    insights = []
    for k in sim_input.keys():
        if k not in orig_input:
            continue
        if sim_input[k] == orig_input[k]:
            continue
        before = contrib_before.get(k, {})
        after = contrib_after.get(k, {})
        # Determine whether contribution increased for this feature
        before_signed = before.get('signed', 0.0)
        after_signed = after.get('signed', 0.0)
        if after_signed > before_signed:
            insights.append(f"✓ {k.title().replace('_',' ')} increased the predicted success probability.")
        else:
            insights.append(f"⚠ {k.title().replace('_',' ')} decreased the predicted success probability.")

    return insights


def render_insights(insights):
    if not insights:
        st.markdown('<div style="color:#CFC9B7">No significant changes detected.</div>', unsafe_allow_html=True)
        return
    html = '<div style="color:#CFC9B7">' + '<br>'.join(insights) + '</div>'
    st.markdown(html, unsafe_allow_html=True)
