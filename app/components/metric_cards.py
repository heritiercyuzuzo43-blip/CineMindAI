import re
import streamlit as st


def _to_number(v):
    try:
        if isinstance(v, (int, float)):
            return float(v)
        s = str(v)
        s2 = re.sub(r'[^0-9.]', '', s)
        return float(s2) if s2 else 0.0
    except Exception:
        return 0.0


def render_dataset_overview(metrics):
    """Render dataset overview cards for CineMind AI with subtle animations."""
    st.markdown('<h2 class="section-heading">Dataset Overview</h2>', unsafe_allow_html=True)

    # Component-scoped CSS for animation and small progress spark
    st.markdown(
        """
        <style>
        .stats-grid { display:flex; gap:16px; flex-wrap:wrap; justify-content:center; max-width:1100px; margin:0 auto 18px; }
        .metric-card { min-width:180px; max-width:260px; padding:14px; border-radius:12px; background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)); border:1px solid rgba(255,255,255,0.02); box-shadow: 0 8px 30px rgba(0,0,0,0.6); transition: transform 360ms cubic-bezier(.2,.9,.2,1), box-shadow 360ms; transform: translateY(6px); opacity:0; animation: pop 540ms forwards; }
        .metric-card:hover{ transform: translateY(-8px); box-shadow: 0 28px 60px rgba(0,0,0,0.6); }
        .metric-icon{ font-size:22px; }
        .stat-title{ color:var(--muted); font-size:13px; margin-top:8px; }
        .stat-value{ color:var(--white); font-size:20px; font-weight:800; }
        .metric-top{ display:flex; align-items:center; justify-content:space-between; gap:8px; }
        .metric-bar{ background: rgba(255,255,255,0.03); height:8px; border-radius:8px; margin-top:10px; overflow:hidden; }
        .metric-fill{ height:100%; background: linear-gradient(90deg,var(--gold), #f1c86b); width:0%; transition: width 900ms cubic-bezier(.2,.9,.2,1); }

        @keyframes pop { to { transform: translateY(0); opacity:1; } }
        .stats-grid .metric-card:nth-child(1){ animation-delay:80ms }
        .stats-grid .metric-card:nth-child(2){ animation-delay:160ms }
        .stats-grid .metric-card:nth-child(3){ animation-delay:240ms }
        .stats-grid .metric-card:nth-child(4){ animation-delay:320ms }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Normalize numeric values for tiny progress bars
    numeric_vals = []
    parsed = {}
    for k, v in metrics.items():
        num = _to_number(v)
        parsed[k] = {'raw': v, 'num': num}
        if num > 0:
            numeric_vals.append(num)

    max_num = max(numeric_vals) if numeric_vals else 1.0

    icon_map = {
        "Movies Analysed": "🎬",
        "Genres Supported": "🎭",
        "Average Budget": "💰",
        "Average Revenue": "📈",
    }

    card_html = []
    for idx, (title, meta) in enumerate(parsed.items(), start=1):
        value = meta['raw']
        num = meta['num']
        pct = int((num / max_num) * 100) if max_num > 0 else 0
        pct = max(6, min(pct, 96))
        icon = icon_map.get(title, '⭐')

        card_html.append(
            f'<div class="stat-card metric-card">'
            f'  <div class="metric-top">'
            f'    <div style="display:flex;align-items:center;gap:10px;"><div class="metric-icon">{icon}</div><div class="stat-value">{value}</div></div>'
            f'  </div>'
            f'  <div class="stat-title">{title}</div>'
            f'  <div class="metric-bar"><div class="metric-fill" style="width:{pct}%;"></div></div>'
            f'</div>'
        )

    cards = "\n".join(card_html)
    st.markdown(f'<section class="stats-grid">{cards}</section>', unsafe_allow_html=True)
