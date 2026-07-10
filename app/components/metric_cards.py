import streamlit as st


def render_dataset_overview(metrics):
    """Render dataset overview cards for CineMind AI."""
    st.markdown('<h2 class="section-heading">Dataset Overview</h2>', unsafe_allow_html=True)
    card_html = []
    icon_map = {
        "Movies Analysed": "🎬",
        "Genres Supported": "🎭",
        "Average Budget": "💰",
        "Average Revenue": "📈",
    }

    for title, value in metrics.items():
        icon = icon_map.get(title, "⭐")
        card_html.append(
            f'<div class="stat-card metric-card">'
            f'<div class="metric-icon">{icon}</div>'
            f'<div class="stat-title">{title}</div>'
            f'<div class="stat-value">{value}</div>'
            '</div>'
        )

    cards = "\n".join(card_html)
    st.markdown(f'<section class="stats-grid">{cards}</section>', unsafe_allow_html=True)
