import plotly.graph_objects as go
import streamlit as st


def render_probability_gauges(orig_prob: float, new_prob: float, height: int = 220):
    """Render two side-by-side Plotly gauge indicators for before/after probabilities.

    Probabilities expected in [0,1].
    """
    fig1 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=orig_prob * 100.0,
        number={'suffix': '%', 'font': {'color': '#FFFFFF'}},
        gauge={'axis': {'range': [0, 100], 'tickcolor': '#CFC9B7'}, 'bar': {'color': '#777777'}, 'bgcolor': 'rgba(0,0,0,0)'},
        title={'text': 'Before', 'font': {'color': '#CFC9B7'}}
    ))
    fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=height, margin=dict(l=10, r=10, t=24, b=10))

    fig2 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=new_prob * 100.0,
        number={'suffix': '%', 'font': {'color': '#FFFFFF'}},
        gauge={'axis': {'range': [0, 100], 'tickcolor': '#CFC9B7'}, 'bar': {'color': '#D4AF37'}, 'bgcolor': 'rgba(0,0,0,0)'},
        title={'text': 'After', 'font': {'color': '#CFC9B7'}}
    ))
    fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=height, margin=dict(l=10, r=10, t=24, b=10))

    col1, col2 = st.columns(2)
    col1.plotly_chart(fig1, use_container_width=True)
    col2.plotly_chart(fig2, use_container_width=True)
