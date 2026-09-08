import streamlit as st

def load_styles():
    st.markdown(
        """
        <style>

        :root{
            --bg:#0B0B0B;
            --bg-secondary:#111111;
            --card:#181818;
            --gold:#D4AF37;
            --gold-2:#C99A1A;
            --muted:#CFC9B7;
            --white:#FFFFFF;
            --glass: rgba(255,255,255,0.03);
            --glass-2: rgba(255,255,255,0.02);
            --radius:12px;
            --transition:220ms cubic-bezier(.2,.9,.2,1);
        }

        html, body {
            background: radial-gradient(circle at top left, rgba(212,175,55,0.08), transparent 18%), radial-gradient(circle at bottom right, rgba(255,255,255,0.05), transparent 20%), #0B0B0B !important;
            color: var(--white);
            font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
            min-height: 100%;
        }

                /* Top nav (used by app) */
        .cnav { display:flex; flex-wrap:nowrap; gap:40px; justify-content:center; align-items:center; margin:18px 0 28px 0; }
        .stButton:nth-of-type(-n+6)>button,
        .stButton:nth-of-type(-n+6)>button * {
            color: #D4AF37 !important;
        }
        .stButton:nth-of-type(-n+6)>button {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            border-radius: 0 !important;
            padding: 0 !important;
            min-width: 0 !important;
            margin: 0 !important;
            color: #D4AF37 !important;
            font-family: 'Poppins', 'Inter', 'Manrope', sans-serif !important;
            font-size: 1rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.05em !important;
            text-transform: uppercase !important;
            text-decoration: none !important;
            transition: color 0.3s ease !important;
            cursor: pointer !important;
            white-space: nowrap !important;
        }
        .stButton:nth-of-type(-n+6)>button:hover {
            color: #4DA3FF !important;
            background: transparent !important;
            transform: none !important;
            box-shadow: none !important;
        }
        .stButton:nth-of-type(-n+6)>button.active {
            border: none !important;
            background: transparent !important;
            box-shadow: none !important;
            border-bottom: 2px solid #D4AF37 !important;
        }

        .stButton:nth-of-type(-n+6)>button:focus,
        .stButton:nth-of-type(-n+6)>button:active {
            outline: none !important;
            box-shadow: 0 18px 42px rgba(212,175,55,0.24) !important;
        }
        .stButton:nth-of-type(-n+6)>button:focus,
        .stButton:nth-of-type(-n+6)>button:active {
            outline: none !important;
            box-shadow: 0 14px 34px rgba(212,175,55,0.18) !important;
        }

        /* Hero section */
        .hero-section { display:grid; grid-template-columns: 1.1fr 0.9fr; gap:48px; align-items:center; max-width:1200px; margin:0 auto 32px; padding:32px 0; }
        .hero-copy { max-width:560px; }
        .hero-eyebrow { display:inline-block; color:var(--gold); font-size:0.85rem; letter-spacing:0.16em; text-transform:uppercase; margin-bottom:18px; }
        .hero-title { font-size:4rem; line-height:1.02; margin:0 0 18px; letter-spacing:-0.04em; max-width:12ch; }
        .hero-subtitle { color:var(--muted); font-size:1.05rem; line-height:1.75; max-width:34rem; margin-bottom:28px; }
        .hero-actions { display:flex; flex-wrap:wrap; gap:14px; margin-bottom:22px; }
        .hero-highlights { display:flex; flex-wrap:wrap; gap:12px; color:var(--muted); font-size:0.95rem; }
        .hero-highlights span { background: rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.06); border-radius:999px; padding:12px 16px; }

        .hero-visual { display:flex; justify-content:flex-end; }
        .hero-visual-card { position:relative; width:100%; max-width:520px; min-height:420px; border-radius:28px; background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.008)); border:1px solid rgba(212,175,55,0.08); box-shadow: 0 40px 110px rgba(0,0,0,0.35); overflow:hidden; }
        .hero-visual-badge { position:absolute; top:22px; left:22px; z-index:2; padding:10px 14px; border-radius:999px; background:rgba(0,0,0,0.6); color:var(--gold); font-weight:700; letter-spacing:0.04em; }
        .hero-visual-grid { display:grid; grid-template-columns: 1fr 1fr; grid-auto-rows: 1fr; gap:16px; padding:22px; position:relative; top:0; }
        .hero-tile { border-radius:22px; background: linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0.02)); min-height:160px; box-shadow: inset 0 0 0 1px rgba(255,255,255,0.04); }
        .hero-tile.tile-a { grid-column:1 / span 2; min-height:240px; background-image: linear-gradient(135deg, rgba(255,255,255,0.06), rgba(212,175,55,0.1)), url('https://images.unsplash.com/photo-1524985069026-dd778a71c7b4?auto=format&fit=crop&w=900&q=80'); background-size:cover; background-position:center; }
        .hero-tile.tile-b { background-image: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01)), url('https://images.unsplash.com/photo-1517604931442-7defb6f70fd4?auto=format&fit=crop&w=900&q=80'); background-size:cover; background-position:center; }
        .hero-tile.tile-c { background-image: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01)), url('https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=80'); background-size:cover; background-position:center; }
        .hero-visual::before { content:''; position:absolute; inset:0; background: radial-gradient(circle at top right, rgba(212,175,55,0.16), transparent 22%), radial-gradient(circle at bottom left, rgba(255,255,255,0.08), transparent 18%); pointer-events:none; }
        .hero-visual-card { animation: fadeInUp 540ms ease both; }

        @media (max-width:1024px) {
            .hero-section { grid-template-columns:1fr; gap:28px; }
            .hero-visual { justify-content:center; }
        }
        @media (max-width:720px) {
            .hero-title { font-size:2.7rem; }
            .hero-actions { flex-direction:column; align-items:flex-start; }
        }

        /* Section headings */
        .section-heading{ color:var(--white); font-weight:800; margin:18px 0 12px; font-size:22px; }

        /* Stats grid */
        .stats-grid{ display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:16px; max-width:1200px; margin:0 auto 18px; }
        .stat-card{ background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.015)); border-radius:16px; padding:18px; border:1px solid rgba(212,175,55,0.04); box-shadow: 0 10px 30px rgba(0,0,0,0.6); }
        .stat-title{ color:var(--muted); font-size:13px; margin-bottom:8px; }
        .stat-value{ color:var(--white); font-size:20px; font-weight:800; }

        /* Workflow row */
        .workflow-row{ display:flex; gap:12px; flex-wrap:wrap; justify-content:center; max-width:1100px; margin:0 auto 18px; }
        .workflow-step{ background:var(--card); padding:12px 14px; border-radius:12px; color:var(--muted); border:1px solid rgba(255,255,255,0.02); min-width:160px; text-align:center; }

        /* Features */
        .feature-grid{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:16px; max-width:1200px; margin:0 auto 20px; }
        .feature-card{ background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)); padding:18px; border-radius:14px; border:1px solid rgba(212,175,55,0.03); transition: transform var(--transition), box-shadow var(--transition); }
        .feature-card:hover{ transform:translateY(-6px); box-shadow: 0 24px 60px rgba(0,0,0,0.6); }

        /* Forms and cards */
        .form-card{ background: linear-gradient(180deg, rgba(24,24,24,0.9), rgba(16,16,16,0.85)); border-radius:14px; padding:16px; border:1px solid rgba(255,255,255,0.02); box-shadow: 0 8px 30px rgba(0,0,0,0.6); }

        /* Buttons */
        .btn{ cursor:pointer; border-radius:999px; padding:14px 26px; font-weight:800; color:var(--white); text-decoration:none; display:inline-block; transition:transform 220ms ease, box-shadow 220ms ease, background 220ms ease, border-color 220ms ease, color 220ms ease; }
        .btn.primary{ background:linear-gradient(90deg,var(--gold),#F6D365); box-shadow: 0 10px 34px rgba(212,175,55,0.22); border: 1px solid rgba(212,175,55,0.22); color:#111111; }
        .btn.primary:hover{ transform:translateY(-2px); box-shadow: 0 18px 48px rgba(212,175,55,0.28); }
        .btn.secondary{ background:transparent; border:1px solid rgba(212,175,55,0.7); color:var(--white); }
        .btn.secondary:hover{ background:rgba(212,175,55,0.08); color:var(--gold); border-color:#F6D365; }

        /* Prediction result */
        .prediction-result-card{ padding:18px; border-radius:16px; background: linear-gradient(180deg, rgba(28,28,28,0.92), rgba(16,16,16,0.9)); border:1px solid rgba(212,175,55,0.1); box-shadow: 0 20px 45px rgba(0,0,0,0.4); animation: fadeInUp 500ms ease forwards; opacity:0; transform: translateY(18px); }
        .prediction-result-card h3{ margin-bottom:10px; color:var(--gold); }
        .prediction-result-card p{ color:#FFFFFF; font-size:1.1rem; margin:0 0 12px; }
        .progress-bar{ background: rgba(255,255,255,0.05); height:14px; border-radius:10px; overflow:hidden; margin-top:12px; }
        .progress-fill{ background: linear-gradient(90deg,var(--gold),#f1c86b); height:100%; width:0%; transition: width 900ms cubic-bezier(.25,.8,.25,1); }
        .progress-label{ color:var(--muted); font-size:13px; margin-top:8px; }
        .confidence-badge{ display:inline-block; background:rgba(212,175,55,0.1); color:var(--gold); padding:8px 14px; border-radius:999px; font-weight:700; margin-top:12px; }
        @keyframes fadeInUp { to { opacity:1; transform: translateY(0); } }

        /* Dataset */
        .dataset-card{ background: var(--glass); border-radius:14px; padding:12px; border:1px solid rgba(212,175,55,0.04); }

        /* Footer / About */
        .footer-section{ text-align:center; color:var(--muted); margin:26px 0 36px; }

        /* Responsive tweaks */
        @media (max-width:800px){
            .section-heading{ font-size:18px; }
            .stats-grid{ grid-template-columns:repeat(auto-fit,minmax(140px,1fr)); }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )