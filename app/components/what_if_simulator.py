import streamlit as st
import pandas as pd
from src.config import FEATURE_COLUMNS

from components.simulation_cards import render_comparison_cards
from components.probability_gauge import render_probability_gauges
from components.simulation_insights import generate_simulation_insights, render_insights


def render_what_if(current_input: dict, predictor):
    """Render the What-If Simulator UI.

    - current_input: dict with FEATURE_COLUMNS keys
    - predictor: MoviePredictor instance with `.model` and `.label_encoder`
    """
    st.markdown('<h2 class="section-heading">🔄 What-If Simulator</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#CFC9B7;max-width:1200px;margin-bottom:8px;">Experiment with movie parameters and see how the AI prediction changes in real time.</p>', unsafe_allow_html=True)

    left, right = st.columns([1, 1])

    # Left: show current movie
    with left:
        st.markdown('<div style="background:#1A1A1A;border-radius:12px;padding:12px;">', unsafe_allow_html=True)
        st.markdown('<strong style="color:#D4AF37">Current Movie</strong>', unsafe_allow_html=True)
        for k in FEATURE_COLUMNS:
            v = current_input.get(k, "—")
            st.markdown(f"<div style='color:#FFFFFF'>{k.replace('_',' ').title()}: <strong style='color:#CFC9B7'>{v}</strong></div>", unsafe_allow_html=True)
        # Compute and show original prediction
        orig_df = pd.DataFrame([current_input])[FEATURE_COLUMNS]
        encoded_orig = predictor.model.predict(orig_df)[0]
        pred_label = predictor.label_encoder.inverse_transform([encoded_orig])[0]
        probs = predictor.model.predict_proba(orig_df)[0]
        # pick top probability
        top_prob = float(probs.max())
        st.markdown(f"<div style='margin-top:8px;color:#CFC9B7'>Prediction: <strong style='color:#FFFFFF'>{pred_label}</strong></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='color:#CFC9B7'>Probability: <strong style='color:#D4AF37'>{top_prob*100:.1f}%</strong></div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Right: simulation controls
    with right:
        st.markdown('<div style="background:#1A1A1A;border-radius:12px;padding:12px;">', unsafe_allow_html=True)
        st.markdown('<strong style="color:#D4AF37">Simulation Inputs</strong>', unsafe_allow_html=True)
        # Editable inputs
        genre = st.selectbox('Genre', options=['Action','Comedy','Drama','Horror','Romance','Sci-Fi','Thriller'], index=max(0, ['Action','Comedy','Drama','Horror','Romance','Sci-Fi','Thriller'].index(current_input.get('genre','Action'))))
        budget = st.number_input('Budget', min_value=0, value=int(current_input.get('budget', 50000000)), step=1000000)
        runtime = st.number_input('Runtime (minutes)', min_value=50, value=int(current_input.get('runtime', 100)), step=1)
        release_month = st.number_input('Release Month', min_value=1, max_value=12, value=int(current_input.get('release_month', 6)), step=1)
        popularity_score = st.number_input('Popularity Score', min_value=0.0, max_value=100.0, value=float(current_input.get('popularity_score', 50.0)), step=0.1)

        run_sim = st.button('Run Simulation')
        reset = st.button('Reset Values')
        st.markdown('</div>', unsafe_allow_html=True)

    # reset behavior
    if reset:
        # simple page reload to reset controls
        st.experimental_rerun()

    # On run, compute new prediction and render results
    if run_sim:
        sim_input = {
            'genre': genre,
            'budget': budget,
            'runtime': runtime,
            'release_month': release_month,
            'popularity_score': popularity_score,
        }
        sim_df = pd.DataFrame([sim_input])[FEATURE_COLUMNS]

        # Original
        orig_df = pd.DataFrame([current_input])[FEATURE_COLUMNS]
        encoded_orig = predictor.model.predict(orig_df)[0]
        orig_probs = predictor.model.predict_proba(orig_df)[0]
        orig_top = float(orig_probs.max())

        # Simulated
        encoded_sim = predictor.model.predict(sim_df)[0]
        sim_probs = predictor.model.predict_proba(sim_df)[0]
        sim_top = float(sim_probs.max())

        # Render comparison cards
        render_comparison_cards(orig_top, sim_top)

        # Gauge charts
        render_probability_gauges(orig_top, sim_top)

        # Bar chart comparing numeric inputs
        # Use Plotly directly here for a grouped bar chart
        import plotly.graph_objects as go
        params = ['budget','popularity_score','release_month','runtime']
        orig_vals = [float(current_input.get(p, 0)) for p in params]
        sim_vals = [float(sim_input.get(p, 0)) for p in params]
        fig = go.Figure(data=[
            go.Bar(name='Original', x=params, y=orig_vals, marker_color='rgba(255,255,255,0.12)'),
            go.Bar(name='Simulated', x=params, y=sim_vals, marker_color='#D4AF37'),
        ])
        fig.update_layout(barmode='group', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#FFFFFF')
        st.plotly_chart(fig, use_container_width=True)

        # Insights using explainable AI contributions
        insights = generate_simulation_insights(predictor.model, current_input, sim_input)
        render_insights(insights)
