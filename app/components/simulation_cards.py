import streamlit as st


def render_comparison_cards(orig_prob: float, new_prob: float):
    """Render three comparison cards: original, new, and difference.

    Probabilities are floats in [0,1]. The cards show percentage values.
    """
    diff = (new_prob - orig_prob) * 100.0
    cols = st.columns(3)
    orig_pct = orig_prob * 100.0
    new_pct = new_prob * 100.0

    cols[0].markdown(
        f"<div style='background:#1A1A1A;border-radius:12px;padding:12px;text-align:center;'>"
        f"<div style='color:#CFC9B7'>Original Probability</div>"
        f"<div style='font-size:1.6rem;font-weight:800;color:#FFFFFF'>{orig_pct:.1f}%</div>"
        "</div>", unsafe_allow_html=True
    )
    cols[1].markdown(
        f"<div style='background:#1A1A1A;border-radius:12px;padding:12px;text-align:center;border:1px solid rgba(212,175,55,0.06);'>"
        f"<div style='color:#CFC9B7'>New Probability</div>"
        f"<div style='font-size:1.6rem;font-weight:800;color:#D4AF37'>{new_pct:.1f}%</div>"
        "</div>", unsafe_allow_html=True
    )
    sign = "+" if diff >= 0 else ""
    cols[2].markdown(
        f"<div style='background:#1A1A1A;border-radius:12px;padding:12px;text-align:center;'>"
        f"<div style='color:#CFC9B7'>Difference</div>"
        f"<div style='font-size:1.4rem;font-weight:800;color:#FFFFFF'>{sign}{diff:.1f} pts</div>"
        "</div>", unsafe_allow_html=True
    )
