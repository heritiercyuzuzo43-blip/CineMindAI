import streamlit as st
import streamlit.components.v1 as components


def render_movie_poster_carousel():
    posters = [
        ("Avatar: The Way of Water", "2022", "https://image.tmdb.org/t/p/original/8rpDcsfLJypbO6vREc0547VKqEv.jpg"),
        ("Oppenheimer", "2023", "https://image.tmdb.org/t/p/original/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg"),
        ("Dune: Part Two", "2024", "https://image.tmdb.org/t/p/original/1pdfLvkbY9ohJlCjQH2CZjjYVvJ.jpg"),
        ("Interstellar", "2014", "https://image.tmdb.org/t/p/original/xJHokMbljvjADYdit5fK5VQsXEG.jpg"),
        ("House of the Dragon", "2022", "https://image.tmdb.org/t/p/original/7QMsOTMUswlwxJP0rTTZfmz2tX2.jpg"),
        ("Blade Runner 2049", "2017", "https://image.tmdb.org/t/p/original/gajva2L0rPYkEWjzgFlBXCAVBE5.jpg"),
        ("Mad Max: Fury Road", "2015", "https://image.tmdb.org/t/p/original/hA2ple9q4qnwxp3hKVNhroipsir.jpg"),
        ("Everything Everywhere All at Once", "2022", "https://image.tmdb.org/t/p/original/w3LxiVYdWWRvEVdn5RYq6jIqkb1.jpg"),
    ]

    poster_items = ""
    for title, year, image in posters:
        poster_items += f'''
            <div class="poster-item">
                <div class="poster-card">
                    <img src="{image}" alt="{title}" loading="lazy" />
                </div>
                <div class="poster-meta">
                    <div class="poster-title">{title}</div>
                    <div class="poster-year">{year}</div>
                </div>
            </div>
        '''

    html = f'''
    <style>
    .home-hero-shell {{
        width:100%;
        max-width:1360px;
        margin:0 auto;
        padding:28px 20px 0;
    }}
    .home-hero {{
        display:grid;
        grid-template-columns:1.05fr 0.95fr;
        gap:34px;
        align-items:center;
        min-height:720px;
    }}
    .hero-copy {{
        position:relative;
        z-index:1;
    }}
    .hero-eyebrow {{
        display:inline-block;
        text-transform:uppercase;
        letter-spacing:0.3em;
        font-size:0.82rem;
        color:#D4AF37;
        margin-bottom:18px;
    }}
    .hero-title {{
        font-size:4.8rem;
        line-height:0.94;
        margin:0;
        color:#FFFFFF;
        font-weight:800;
    }}
    .hero-title .highlight {{
        color:#D4AF37;
    }}
    .hero-description {{
        max-width:600px;
        color:#C9C9C9;
        font-size:1.05rem;
        line-height:1.72;
        margin:26px 0 36px;
    }}
    .hero-actions {{
        display:flex;
        flex-wrap:wrap;
        gap:18px;
        margin-bottom:24px;
    }}
    .hero-actions .btn {{
        border-radius:999px;
        padding:18px 34px;
        min-width:190px;
        text-align:center;
        font-size:0.98rem;
        font-weight:800;
        text-decoration:none;
        transition:transform 220ms ease, box-shadow 220ms ease, border-color 220ms ease, color 220ms ease, background 220ms ease;
        box-shadow:0 24px 54px rgba(0,0,0,0.24);
    }}
    .hero-actions .btn.primary {{
        background:linear-gradient(90deg, #D4AF37, #F6D365);
        color:#111111;
        border:1px solid rgba(212,175,55,0.22);
    }}
    .hero-actions .btn.primary:hover {{
        transform:translateY(-2px);
        box-shadow:0 30px 68px rgba(212,175,55,0.28);
    }}
    .hero-actions .btn.secondary {{
        background:transparent;
        color:#FFFFFF;
        border:1px solid rgba(212,175,55,0.75);
    }}
    .hero-actions .btn.secondary:hover {{
        transform:translateY(-2px);
        color:#D4AF37;
        background:rgba(212,175,55,0.08);
        border-color:#F6D365;
        box-shadow:0 22px 48px rgba(212,175,55,0.16);
    }}
    .hero-visual {{
        display:flex;
        justify-content:flex-end;
    }}
    .hero-visual-card {{
        position:relative;
        width:100%;
        max-width:600px;
        min-height:700px;
        border-radius:34px;
        background:#111111;
        border:1px solid rgba(212,175,55,0.18);
        box-shadow:0 44px 118px rgba(0,0,0,0.48);
        overflow:hidden;
    }}
    .hero-visual-image {{
        position:absolute;
        inset:0;
        width:100%;
        height:100%;
        object-fit:cover;
        object-position:center;
        filter:brightness(0.78) saturate(1.12);
    }}
    .hero-visual-overlay {{
        position:absolute;
        inset:0;
        background:linear-gradient(180deg, rgba(11,11,11,0.12), rgba(11,11,11,0.8));
        pointer-events:none;
    }}
    .hero-visual-frame {{
        position:absolute;
        inset:0;
        border-radius:34px;
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.05);
        pointer-events:none;
    }}
    .hero-visual-ring {{
        position:absolute;
        right:-36px;
        top:28px;
        width:230px;
        height:230px;
        border-radius:50%;
        border:1px solid rgba(212,175,55,0.18);
        box-shadow:0 0 86px rgba(212,175,55,0.18);
        opacity:0.9;
        pointer-events:none;
    }}
    .hero-visual-ribbon {{
        position:absolute;
        top:34px;
        left:34px;
        display:inline-flex;
        align-items:center;
        gap:10px;
        padding:12px 18px;
        border-radius:999px;
        background:rgba(0,0,0,0.5);
        border:1px solid rgba(255,255,255,0.08);
        color:#FFFFFF;
        font-size:0.82rem;
        letter-spacing:0.18em;
        text-transform:uppercase;
        z-index:2;
    }}
    .hero-visual-copy {{
        position:absolute;
        bottom:42px;
        left:42px;
        z-index:2;
        color:#FFFFFF;
        max-width:320px;
    }}
    .hero-visual-copy .label {{
        display:inline-block;
        margin-bottom:18px;
        padding:12px 18px;
        border-radius:999px;
        background:rgba(255,255,255,0.08);
        border:1px solid rgba(255,255,255,0.12);
        font-size:0.82rem;
        letter-spacing:0.18em;
        text-transform:uppercase;
    }}
    .hero-visual-copy h3 {{
        margin:0;
        font-size:2rem;
        line-height:1.04;
    }}
    .hero-visual-copy p {{
        margin:16px 0 0;
        color:#C9C9C9;
        line-height:1.78;
        font-size:0.98rem;
        max-width:320px;
    }}
    .carousel-section {{
        margin-top:66px;
    }}
    .carousel-headline {{
        display:flex;
        justify-content:space-between;
        gap:16px;
        align-items:flex-end;
        margin-bottom:24px;
    }}
    .carousel-title {{
        font-size:1.45rem;
        font-weight:800;
        color:#FFFFFF;
        margin:0;
    }}
    .carousel-caption {{
        color:#C9C9C9;
        font-size:0.95rem;
        text-align:right;
    }}
    .poster-row {{
        display:flex;
        gap:18px;
        overflow-x:auto;
        padding-bottom:10px;
        scroll-snap-type:x mandatory;
        -webkit-overflow-scrolling:touch;
    }}
    .poster-row::-webkit-scrollbar {{
        height:10px;
    }}
    .poster-row::-webkit-scrollbar-thumb {{
        background:rgba(255,255,255,0.16);
        border-radius:999px;
    }}
    .poster-item {{
        flex:0 0 auto;
        width:218px;
        scroll-snap-align:start;
    }}
    .poster-card {{
        width:100%;
        aspect-ratio:2/3;
        border-radius:22px;
        overflow:hidden;
        background:#161616;
        border:1px solid rgba(212,175,55,0.14);
        box-shadow:0 24px 60px rgba(0,0,0,0.42);
        transition:transform 260ms ease,box-shadow 260ms ease,border-color 260ms ease;
    }}
    .poster-card img {{
        width:100%;
        height:100%;
        object-fit:cover;
        display:block;
    }}
    .poster-card:hover {{
        transform:translateY(-10px);
        box-shadow:0 38px 88px rgba(212,175,55,0.22);
        border-color:rgba(212,175,55,0.35);
    }}
    .poster-card::after {{
        content:'';
        position:absolute;
        inset:0;
        border-radius:22px;
        box-shadow:0 0 0 1px rgba(255,255,255,0.02), 0 0 32px rgba(212,175,55,0.08);
        opacity:0;
        transition:opacity 260ms ease;
        pointer-events:none;
    }}
    .poster-card:hover::after {{
        opacity:1;
    }}
    .poster-meta {{
        margin-top:14px;
    }}
    .poster-title {{
        font-size:0.96rem;
        font-weight:700;
        color:#FFFFFF;
        margin:0 0 6px;
    }}
    .poster-year {{
        font-size:0.84rem;
        color:#C9C9C9;
        letter-spacing:0.02em;
        margin:0;
    }}
    @media (max-width:1080px) {{
        .home-hero {{ grid-template-columns:1fr; }}
        .hero-visual {{ justify-content:center; }}
        .hero-title {{ font-size:3.8rem; }}
        .hero-visual-card {{ max-width:100%; min-height:520px; }}
    }}
    @media (max-width:720px) {{
        .home-hero {{ gap:24px; }}
        .hero-title {{ font-size:3rem; }}
        .hero-description {{ font-size:1rem; }}
        .hero-actions .btn {{ width:100%; text-align:center; }}
        .carousel-headline {{ flex-direction:column; align-items:flex-start; }}
        .poster-item {{ width:170px; }}
    }}
    </style>

    <div class="home-hero-shell">
        <div class="home-hero">
            <div class="hero-copy">
                <span class="hero-eyebrow">CineMind AI</span>
                <h1 class="hero-title">Predict Movie<br><span class="highlight">Success</span><br>Before Release</h1>
                <p class="hero-description">High-end forecasting and cinematic intelligence for studios, producers, and premium release strategies.</p>
                <div class="hero-actions">
                    <a class="btn primary" href="#prediction-form">Start Prediction</a>
                    <a class="btn secondary" href="#how-it-works">Learn More</a>
                </div>
            </div>
            <div class="hero-visual">
                <div class="hero-visual-card">
                    <img class="hero-visual-image" src="https://images.unsplash.com/photo-1517604931442-7defb6f70fd4?auto=format&fit=crop&w=1200&q=80" alt="Cinematic illustration" />
                    <div class="hero-visual-overlay"></div>
                    <div class="hero-visual-ring"></div>
                    <div class="hero-visual-ribbon">Cinematic Intelligence</div>
                    <div class="hero-visual-copy">
                        <span class="label">Studio-grade insight</span>
                        <h3>Predictive intelligence styled for premium releases</h3>
                        <p>Capture the mood of a blockbuster campaign with elegant motion and gold highlights.</p>
                    </div>
                    <div class="hero-visual-frame"></div>
                </div>
            </div>
        </div>

        <div class="carousel-section">
            <div class="carousel-headline">
                <div class="carousel-title">Featured Movie Posters</div>
                <div class="carousel-caption">A curated selection of cinematic titles styled like Netflix and IMDb.</div>
            </div>
            <div class="poster-row">
                {poster_items}
            </div>
        </div>
    </div>
    '''

    components.html(html, height=930, scrolling=False)
