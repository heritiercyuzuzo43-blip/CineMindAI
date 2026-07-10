import plotly.graph_objects as go


def render_feature_importance_chart(contributions, title="Feature contributions", height=360):
    """Render a horizontal bar chart for feature contributions.

    contributions: list of tuples (feature_name, pct_value)
    Example: [("Budget", 38.2), ("Popularity", 27.1), ...]
    """
    # Unpack data
    features = [f for f, _ in contributions]
    values = [v for _, v in contributions]

    # Create horizontal bar chart using Plotly for smooth animation and styling
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=values[::-1],  # reverse for horizontal bar ordering
            y=features[::-1],
            orientation="h",
            marker=dict(color="#D4AF37", line=dict(color="rgba(212,175,55,0.2)", width=0)),
            hovertemplate="%{y}: %{x:.1f}%<extra></extra>",
        )
    )

    fig.update_layout(
        title=dict(text=title, font=dict(color="#FFFFFF", size=14), x=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF"),
        margin=dict(l=140, r=24, t=40, b=24),
        height=height,
    )

    # Soft animation on load
    fig.update_traces(marker_line_width=0)
    fig.update_layout(transition=dict(duration=400, easing="cubic-in-out"))

    return fig
