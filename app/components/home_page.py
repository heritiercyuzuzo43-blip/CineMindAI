import streamlit as st


def navigate_to(page_name: str):
    st.session_state.page = page_name


def render_home_page_styles():
    st.markdown(
        """
        <style>
        .home-page-shell { max-width: 1280px; margin: 0 auto; padding: 24px 24px 40px; position: relative; }
        .hero-section { display: grid; grid-template-columns: 1.05fr 0.95fr; gap: 54px; align-items: center; max-width: 1200px; margin: 0 auto 48px; padding: 32px 0 12px; }
        .hero-brand { display: inline-flex; align-items: center; gap: 12px; font-size: 0.95rem; font-weight: 700; letter-spacing: 0.22em; text-transform: uppercase; color: #D4AF37; margin-bottom: 16px; }
        .hero-brand span { font-size: 1.1rem; }
        .hero-tagline { color: #E8E3DC; font-size: 1rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; margin: 0 0 26px; }
        .hero-title { font-family: 'Cinzel', 'Cormorant Garamond', 'Playfair Display', serif; font-size: clamp(3.8rem, 5.4vw, 5.8rem); line-height: 0.96; margin: 0 0 28px; letter-spacing: 0.22em; color: #FFFFFF; }
        .hero-title .title-highlight { display: block; background: linear-gradient(90deg, #D4AF37 0%, #F5D76E 100%); -webkit-background-clip: text; color: transparent; }
        .hero-description { color: #D8D8D8; font-size: 1.05rem; line-height: 1.95; max-width: 44rem; margin-bottom: 34px; }
        .hero-actions { display: flex; flex-wrap: wrap; gap: 16px; margin-bottom: 28px; }
        .hero-actions .stButton>button { border-radius: 999px; min-width: 188px; padding: 18px 34px; font-weight: 800; letter-spacing: 0.08em; transition: transform 300ms ease, box-shadow 300ms ease, background 300ms ease, border-color 300ms ease, color 300ms ease; }
        .hero-actions .stButton>button:first-child { background: linear-gradient(90deg, #D4AF37 0%, #F5D76E 100%); color: #111111; border: 1px solid rgba(212,175,55,0.32); box-shadow: 0 18px 42px rgba(212,175,55,0.22); }
        .hero-actions .stButton>button:first-child:hover { transform: translateY(-2px); box-shadow: 0 26px 58px rgba(212,175,55,0.22); }
        .hero-actions .stButton>button:last-child { background: transparent; color: #FFFFFF; border: 1px solid rgba(212,175,55,0.9); }
        .hero-actions .stButton>button:last-child:hover { background: rgba(212,175,55,0.16); color: #FFFFFF; border-color: rgba(255,223,120,0.95); box-shadow: 0 20px 44px rgba(212,175,55,0.16); }
        .hero-actions .stButton>button svg { margin-right: 10px; vertical-align: middle; }
        .hero-visual { display: flex; justify-content: flex-end; position: relative; }
        .hero-visual { margin-top: 10px; }
        .hero-visual-card { position: relative; width: 100%; max-width: 640px; min-height: 560px; border-radius: 34px; background: rgba(18,18,18,0.95); border: 1px solid rgba(212,175,55,0.14); box-shadow: 0 28px 86px rgba(0,0,0,0.5); overflow: hidden; }
        .hero-visual-card::before { content: ''; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(255,255,255,0.03), transparent 34%); pointer-events: none; }
        .hero-visual-poster { position: absolute; border-radius: 28px; overflow: hidden; background: #111; box-shadow: 0 30px 82px rgba(0,0,0,0.32); transition: transform 260ms ease, box-shadow 260ms ease; }
        .hero-visual-poster img { width: 100%; height: 100%; object-fit: cover; filter: saturate(1.1) brightness(0.9); }
        .hero-visual-poster:hover { transform: translateY(-6px) scale(1.02); }
        .hero-visual-poster--a { top: 28px; left: 24px; width: 210px; height: 320px; transform: rotate(-4deg); }
        .hero-visual-poster--b { top: 48px; right: 28px; width: 240px; height: 360px; transform: rotate(6deg); }
        .hero-visual-poster--c { bottom: 42px; left: 64px; width: 240px; height: 360px; transform: rotate(4deg); }
        .hero-visual-poster--d { bottom: 34px; right: 56px; width: 200px; height: 300px; transform: rotate(-7deg); }
        .hero-visual-glow { position: absolute; top: 20%; left: 18%; width: 220px; height: 220px; border-radius: 50%; background: radial-gradient(circle, rgba(212,175,55,0.16), transparent 65%); pointer-events: none; filter: blur(12px); }
        .hero-visual-glow--small { position: absolute; bottom: 18%; right: 12%; width: 150px; height: 150px; border-radius: 50%; background: radial-gradient(circle, rgba(212,175,55,0.14), transparent 68%); pointer-events: none; filter: blur(12px); }

        .poster-showcase-section { padding: 18px 0 40px; }
        .carousel-header { display: flex; justify-content: space-between; align-items: flex-end; gap: 16px; margin-bottom: 24px; }
        .carousel-title { font-size: 1.55rem; font-weight: 800; margin: 0; color: #FFFFFF; }
        .carousel-subtitle { color: #CFC9B7; font-size: 0.96rem; }
        .carousel-controls { display: inline-flex; gap: 12px; }
        .control-button { width: 48px; height: 48px; border-radius: 999px; display: inline-flex; align-items: center; justify-content: center; color: #FFFFFF; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.12); box-shadow: 0 14px 30px rgba(0,0,0,0.22); transition: transform 220ms ease, background 220ms ease, border-color 220ms ease; }
        .control-button:hover { transform: translateY(-2px); background: rgba(212,175,55,0.12); border-color: rgba(212,175,55,0.22); }
        .poster-row { display: flex; gap: 18px; overflow-x: auto; padding-bottom: 10px; scroll-snap-type: x mandatory; -webkit-overflow-scrolling: touch; }
        .poster-row::-webkit-scrollbar { height: 10px; }
        .poster-row::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.18); border-radius: 999px; }
        .poster-item { flex: 0 0 auto; width: 240px; scroll-snap-align: start; }
        .poster-card { background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.008)); border-radius: 24px; overflow: hidden; border: 1px solid rgba(212,175,55,0.18); box-shadow: 0 26px 70px rgba(0,0,0,0.33); transition: transform 260ms ease, border-color 260ms ease, box-shadow 260ms ease; }
        .poster-card:hover { transform: translateY(-6px); border-color: rgba(212,175,55,0.28); box-shadow: 0 38px 90px rgba(0,0,0,0.42); }
        .poster-card img { width: 100%; height: 360px; object-fit: cover; display: block; }
        .poster-meta { padding: 16px 16px 18px; color: #FFFFFF; }
        .poster-title { font-size: 1.02rem; font-weight: 700; margin-bottom: 6px; }
        .poster-year { color: #CFC9B7; font-size: 0.92rem; }

        .feature-section { padding: 8px 0 0; }
        .feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 18px; }
        .feature-card { background: rgba(255,255,255,0.02); border: 1px solid rgba(212,175,55,0.10); border-radius: 24px; padding: 26px 24px; box-shadow: 0 18px 50px rgba(0,0,0,0.2); transition: transform 260ms ease, box-shadow 260ms ease, border-color 260ms ease; }
        .feature-card:hover { transform: translateY(-6px); border-color: rgba(212,175,55,0.20); box-shadow: 0 30px 70px rgba(0,0,0,0.28); }
        .feature-title { font-family: 'Cinzel', 'Playfair Display', serif; font-size: 1.22rem; margin-bottom: 12px; font-weight: 800; color: #FFFFFF; }
        .feature-copy { color: #D8D2C2; line-height: 1.82; }
        .section-heading { font-size: 1.55rem; font-weight: 800; margin-bottom: 18px; color: #FFFFFF; }

        .hero-gradient-bg { position: absolute; inset: 0; pointer-events: none; z-index: -1; background: radial-gradient(circle at top left, rgba(212,175,55,0.09), transparent 24%), radial-gradient(circle at bottom right, rgba(255,255,255,0.04), transparent 18%), radial-gradient(circle at center, rgba(255,255,255,0.02), transparent 40%); }

        @media (max-width: 1080px) { .hero-section { flex-direction: column; align-items: center; } .hero-visual { justify-content: center; margin-top: 28px; } }
        @media (max-width: 760px) {
            .hero-title { font-size: 3.2rem; }
            .hero-section { gap: 32px; padding: 24px 0 12px; }
            .hero-copy { width: 100%; }
            .hero-actions { justify-content: flex-start; }
            .poster-item { width: 200px; }
            .hero-visual-card { min-height: 460px; }
        }
        """,
        unsafe_allow_html=True,
    )


def render_hero_section():
    with st.container():
        left, right = st.columns([1.05, 0.95], gap="large")
        with left:
            st.markdown(
                """
                <div class="hero-section">
                    <div class="hero-copy">
                        <div class="hero-brand">🎬 CINEMIND AI</div>
                        <p class="hero-tagline">AI That Predicts Movie Success</p>
                        <h1 class="hero-title">AI THAT PREDICTS<br /><span class="title-highlight">MOVIE SUCCESS</span><br />Before Release</h1>
                        <p class="hero-description">A premium cinematic platform for studios and executives. Forecast movie potential with luxury visuals, trusted AI, and executive-grade insight.</p>
                        <div class="hero-actions">
                """,
                unsafe_allow_html=True,
            )
            button_col1, button_col2 = st.columns([0.45, 0.45], gap="small")
            with button_col1:
                st.button("🚀 START PREDICTION", key="home_start_prediction", on_click=navigate_to, args=("Prediction",))
            with button_col2:
                st.button("➡ LEARN MORE", key="home_learn_more", on_click=navigate_to, args=("About",))
            st.markdown(
                """
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with right:
            st.markdown(
                """
                <div class="hero-visual">
                    <div class="hero-visual-card">
                        <div class="hero-visual-glow"></div>
                        <div class="hero-visual-glow--small"></div>
                        <div class="hero-visual-poster hero-visual-poster--a"><img src="https://image.tmdb.org/t/p/original/8rpDcsfLJypbO6vREc0547VKqEv.jpg" alt="Avatar poster" /></div>
                        <div class="hero-visual-poster hero-visual-poster--b"><img src="https://image.tmdb.org/t/p/original/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg" alt="Oppenheimer poster" /></div>
                        <div class="hero-visual-poster hero-visual-poster--c"><img src="https://image.tmdb.org/t/p/original/1pdfLvkbY9ohJlCjQH2CZjjYVvJ.jpg" alt="Dune poster" /></div>
                        <div class="hero-visual-poster hero-visual-poster--d"><img src="https://image.tmdb.org/t/p/original/xJHokMbljvjADYdit5fK5VQsXEG.jpg" alt="Interstellar poster" /></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_poster_showcase():
    with st.container():
        st.markdown(
            """
            <div class="poster-showcase-section">
                <div class="carousel-header">
                    <div>
                        <h2 class="carousel-title">Movie Poster Showcase</h2>
                        <div class="carousel-subtitle">Scroll through premium poster cards in a Netflix-style carousel.</div>
                    </div>
                    <div class="carousel-controls">
                        <div class="control-button">‹</div>
                        <div class="control-button">›</div>
                    </div>
                </div>
                <div class="poster-row">
                    <div class="poster-item"><div class="poster-card"><img src="https://image.tmdb.org/t/p/original/8rpDcsfLJypbO6vREc0547VKqEv.jpg" alt="Avatar" /></div><div class="poster-meta"><div class="poster-title">Avatar: The Way of Water</div><div class="poster-year">2022</div></div></div>
                    <div class="poster-item"><div class="poster-card"><img src="https://image.tmdb.org/t/p/original/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg" alt="Oppenheimer" /></div><div class="poster-meta"><div class="poster-title">Oppenheimer</div><div class="poster-year">2023</div></div></div>
                    <div class="poster-item"><div class="poster-card"><img src="https://image.tmdb.org/t/p/original/1pdfLvkbY9ohJlCjQH2CZjjYVvJ.jpg" alt="Dune" /></div><div class="poster-meta"><div class="poster-title">Dune: Part Two</div><div class="poster-year">2024</div></div></div>
                    <div class="poster-item"><div class="poster-card"><img src="https://image.tmdb.org/t/p/original/xJHokMbljvjADYdit5fK5VQsXEG.jpg" alt="Interstellar" /></div><div class="poster-meta"><div class="poster-title">Interstellar</div><div class="poster-year">2014</div></div></div>
                    <div class="poster-item"><div class="poster-card"><img src="https://image.tmdb.org/t/p/original/gajva2L0rPYkEWjzgFlBXCAVBE5.jpg" alt="Blade Runner 2049" /></div><div class="poster-meta"><div class="poster-title">Blade Runner 2049</div><div class="poster-year">2017</div></div></div>
                    <div class="poster-item"><div class="poster-card"><img src="https://image.tmdb.org/t/p/original/hA2ple9q4qnwxp3hKVNhroipsir.jpg" alt="Mad Max: Fury Road" /></div><div class="poster-meta"><div class="poster-title">Mad Max: Fury Road</div><div class="poster-year">2015</div></div></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_feature_cards():
    with st.container():
        st.markdown(
            """
            <div class="feature-section">
                <div class="section-heading">Premium Feature Cards</div>
                <div class="feature-grid">
                    <div class="feature-card">
                        <div class="feature-title">AI Powered</div>
                        <div class="feature-copy">Predict outcomes with industry-grade AI and cinematic presentation.</div>
                    </div>
                    <div class="feature-card">
                        <div class="feature-title">Data Driven</div>
                        <div class="feature-copy">Engineered around historical film performance and audience signals.</div>
                    </div>
                    <div class="feature-card">
                        <div class="feature-title">Reliable Results</div>
                        <div class="feature-copy">A premium experience built for confident studio decision-making.</div>
                    </div>
                    <div class="feature-card">
                        <div class="feature-title">What-if Simulator</div>
                        <div class="feature-copy">Visualize alternate release scenarios with polished scenario planning.</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_home_page():
    render_home_page_styles()
    render_hero_section()
    render_poster_showcase()
    render_feature_cards()
