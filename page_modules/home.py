import streamlit as st
from utils.helpers import inject_global_css
from utils.load_data import CARD_CLASS_DETAILS, CARD_ARO_GENES
from pathlib import Path
import base64


# ─────────────────────────────────────────────
#  Session state keys
# ─────────────────────────────────────────────
def _init():
    defaults = {
        "home_section": 1,
        "show_pipeline": False,
        "show_card_components": False,
        "show_drug_panel": False,
        "drug_expanded": {},
        "card_viz_idx": 0,
        "show_io_box": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ─────────────────────────────────────────────
#  HELPER : Convertir image en Base64
# ─────────────────────────────────────────────
def img_to_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None


# ─────────────────────────────────────────────
#  CSS HOME
# ─────────────────────────────────────────────
def inject_home_css():
    HOME_CSS = """
<!-- Bootstrap 5 -->
<link rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
      integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH"
      crossorigin="anonymous">
<link rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">

<style>
/* ── Nav pills ── */
.nav-pills-custom {
    display: flex; gap: 8px; margin-bottom: 32px; flex-wrap: wrap;
}
.nav-pill {
    padding: 10px 24px; border-radius: 40px; font-size: .85rem;
    font-weight: 600; cursor: pointer; border: 2px solid transparent;
    transition: all .22s; user-select: none;
}
.nav-pill.active {
    background: linear-gradient(135deg,var(--navy),var(--ocean));
    color: #fff; box-shadow: 0 4px 16px rgba(2,62,138,.25);
}
.nav-pill.inactive {
    background: #fff; color: var(--muted); border-color: #d8e8f4;
}
.nav-pill.inactive:hover { border-color: var(--ocean); color: var(--navy); }

/* ── Section wrapper ── */
.section-wrap { animation: fadeUp .35s ease both; }
@keyframes fadeUp {
    from { opacity:0; transform:translateY(14px); }
    to   { opacity:1; transform:translateY(0); }
}

/* ── Toggle buttons ── */
.toggle-btn {
    display: inline-flex; align-items: center; gap: 10px;
    background: linear-gradient(135deg,var(--ocean),var(--navy));
    color: #fff; border: none; border-radius: 40px;
    padding: 11px 26px; font-size: .87rem; font-weight: 700;
    cursor: pointer; box-shadow: 0 4px 16px rgba(0,119,182,.25);
    transition: transform .2s, box-shadow .2s; margin: 8px 4px;
}
.toggle-btn:hover {
    transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,119,182,.35);
}

/* ── Pipeline Bootstrap override ── */
.pipeline-wrap {
    background: linear-gradient(135deg,#f0f8ff,#e4f3fb);
    border: 1px solid var(--border); border-radius: 20px;
    padding: 32px 24px; margin-top: 16px;
    animation: fadeUp .3s ease both;
}

/* ── Pipeline steps (7 étapes) ── */
.pipeline-steps {
    display: flex;
    flex-wrap: wrap;
    gap: 0;
    align-items: stretch;
    justify-content: center;
    margin: 24px 0;
}
.pip-step {
    background: linear-gradient(135deg,var(--navy),var(--ocean));
    color: #fff;
    border-radius: 16px;
    padding: 16px 14px;
    text-align: center;
    min-width: 110px;
    max-width: 130px;
    flex: 1;
    box-shadow: 0 4px 14px rgba(2,62,138,.2);
    position: relative;
    transition: transform .2s, box-shadow .2s;
}
.pip-step:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 24px rgba(2,62,138,.3);
    z-index: 2;
}
.pip-step.light {
    background: linear-gradient(135deg,var(--sky),var(--cerulean));
}
.pip-step.accent {
    background: linear-gradient(135deg,#0a2463,var(--navy));
    box-shadow: 0 6px 20px rgba(2,62,138,.35);
}
.pip-step .step-num {
    font-size: .6rem; font-weight: 900; letter-spacing: 1.5px;
    opacity: .75; margin-bottom: 4px; text-transform: uppercase;
}
.pip-step .step-ico { font-size: 1.5rem; margin-bottom: 6px; display: block; }
.pip-step .step-title {
    font-size: .75rem; font-weight: 800; line-height: 1.3; margin-bottom: 4px;
}
.pip-step .step-tools {
    font-size: .62rem; opacity: .72; line-height: 1.4;
}
.pip-arrow-h {
    display: flex; align-items: center; color: var(--ocean);
    font-size: 1.1rem; font-weight: 900; padding: 0 4px;
    flex-shrink: 0;
}

/* ── IO Box ── */
.io-box-wrap {
    animation: fadeUp .3s ease both;
    margin-top: 16px;
}
.io-container {
    background: linear-gradient(135deg, #f0f8ff, #e4f3fb);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 28px;
    overflow: hidden;
}
.io-row {
    display: flex;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
    justify-content: center;
}
.io-card {
    flex: 1; min-width: 200px; max-width: 260px;
    border-radius: 16px; padding: 22px 18px; text-align: center;
    box-shadow: 0 4px 16px rgba(0,100,180,.1);
}
.io-card.input-card {
    background: linear-gradient(135deg, #023e8a, #0077b6);
    color: #fff;
}
.io-card.output-card {
    background: linear-gradient(135deg, #0096c7, #00b4d8);
    color: #fff;
}
.io-card .io-label {
    font-size: .65rem; font-weight: 800; letter-spacing: 2px;
    text-transform: uppercase; opacity: .8; margin-bottom: 10px;
}
.io-card .io-title { font-size: 1rem; font-weight: 800; margin-bottom: 8px; }
.io-card .io-desc { font-size: .78rem; opacity: .85; line-height: 1.5; }
.io-arrow-big {
    font-size: 2rem; color: var(--ocean); flex-shrink: 0;
    display: flex; flex-direction: column; align-items: center; gap: 6px;
}
.io-arrow-big .io-arrow-label {
    font-size: .65rem; font-weight: 700; color: var(--navy);
    text-transform: uppercase; letter-spacing: 1px;
}
.binary-vector {
    display: flex; gap: 4px; flex-wrap: wrap; justify-content: center;
    margin-top: 10px;
}
.bit {
    width: 26px; height: 26px; border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
    font-size: .78rem; font-weight: 800;
}
.bit.one { background: rgba(255,255,255,.3); color: #fff; }
.bit.zero { background: rgba(255,255,255,.1); color: rgba(255,255,255,.5); }
.bit.special { background: rgba(255,200,50,.25); color: #ffe066; border: 1px solid rgba(255,200,50,.4); }

/* ── CARD link box ── */
.card-link-box {
    background: linear-gradient(135deg, #023e8a, #0077b6);
    border-radius: 20px;
    padding: 24px 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 16px;
    box-shadow: 0 8px 28px rgba(2,62,138,.25);
    margin-bottom: 24px;
    animation: fadeUp .3s ease both;
}
.card-link-box .clb-title {
    font-size: 1.1rem; font-weight: 800; color: #fff; margin-bottom: 4px;
}
.card-link-box .clb-desc {
    font-size: .82rem; color: rgba(202,240,248,.85); line-height: 1.5;
}
.card-link-btn {
    display: inline-flex; align-items: center; gap: 10px;
    background: #fff; color: var(--navy);
    border-radius: 40px; padding: 12px 24px;
    font-size: .88rem; font-weight: 800;
    text-decoration: none;
    box-shadow: 0 4px 16px rgba(0,0,0,.15);
    transition: transform .2s, box-shadow .2s;
    white-space: nowrap;
}
.card-link-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,.2);
    color: var(--navy);
    text-decoration: none;
}

/* ── Image Carousel ── */
.carousel-outer {
    position: relative;
    border-radius: 20px;
    overflow: hidden;
    background: linear-gradient(135deg, #0d2137, #023e8a);
    box-shadow: 0 12px 40px rgba(2,62,138,.25);
    margin-top: 16px;
}
.carousel-track-wrap {
    overflow: hidden;
    width: 100%;
    position: relative;
}
.carousel-track {
    display: flex;
    transition: transform .45s cubic-bezier(.4,0,.2,1);
}
.carousel-slide {
    flex: 0 0 100%;
    width: 100%;
    min-height: 280px;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #0d2137;
}
.carousel-slide img {
    width: 100%;
    height: 320px;
    object-fit: cover;
    display: block;
}
.carousel-slide .slide-placeholder {
    width: 100%;
    height: 320px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #0d2137, #023e8a);
    color: rgba(202,240,248,.6);
    font-size: .9rem;
    gap: 12px;
}
.carousel-slide .slide-placeholder .ph-icon { font-size: 2.5rem; }
.carousel-btn {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(255,255,255,.18);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,.25);
    color: #fff;
    width: 46px; height: 46px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    cursor: pointer;
    transition: background .2s, transform .2s;
    z-index: 10;
}
.carousel-btn:hover {
    background: rgba(255,255,255,.35);
    transform: translateY(-50%) scale(1.08);
}
.carousel-btn.prev { left: 14px; }
.carousel-btn.next { right: 14px; }
.carousel-dots {
    display: flex; justify-content: center; gap: 8px;
    padding: 14px;
    background: rgba(0,0,0,.2);
}
.carousel-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: rgba(255,255,255,.3);
    cursor: pointer; transition: all .25s;
    border: none; padding: 0;
}
.carousel-dot.active {
    background: #fff;
    width: 22px;
    border-radius: 4px;
}
.carousel-caption {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    background: linear-gradient(transparent, rgba(2,30,70,.85));
    padding: 28px 20px 16px;
    color: #fff;
}
.carousel-caption .cap-num {
    font-size: .65rem; font-weight: 700; letter-spacing: 2px;
    color: var(--sky); text-transform: uppercase; margin-bottom: 4px;
}
.carousel-caption .cap-title {
    font-size: .92rem; font-weight: 700; color: #fff;
}

/* ── Drug classes panel ── */
.drug-panel {
    background: #fff; border-radius: 20px;
    border: 1px solid var(--border);
    box-shadow: 0 8px 32px rgba(0,100,180,.1);
    padding: 24px; margin-top: 16px;
    animation: fadeUp .3s ease both;
}
.drug-card {
    background: #f8faff; border: 1px solid var(--border);
    border-radius: 14px; padding: 14px 16px;
    transition: box-shadow .2s;
    margin-bottom: 4px;
}
.drug-card:hover { box-shadow: 0 4px 16px rgba(0,100,180,.12); }
.drug-name {
    font-size: .8rem; font-weight: 700; color: var(--navy);
    margin-bottom: 8px; line-height: 1.4;
}
.drug-detail {
    margin-top: 10px; padding: 10px 12px;
    background: linear-gradient(135deg,#f0f8ff,#e8f4fc);
    border-radius: 10px; font-size: .78rem; color: var(--text);
    line-height: 1.65; border-left: 3px solid var(--sky);
    animation: fadeUp .2s ease both;
}
.drug-occ-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: linear-gradient(135deg,var(--navy),var(--ocean));
    color: #fff; border-radius: 20px; padding: 6px 14px;
    font-size: .82rem; font-weight: 800;
}

/* ── Stat row ── */
.stat-row {
    display: flex; gap: 14px; flex-wrap: wrap; margin: 20px 0;
}
.stat-mini {
    background: linear-gradient(135deg,var(--navy),var(--ocean));
    border-radius: 16px; padding: 18px 22px; flex: 1; min-width: 100px;
    text-align: center; box-shadow: 0 4px 14px rgba(2,62,138,.18);
}
.stat-mini-val { font-size: 1.7rem; font-weight: 900; color: #fff; }
.stat-mini-lbl { font-size: .68rem; color: var(--ice); margin-top: 3px; }

/* ── Result badges ── */
.res-badge {
    display: inline-flex; align-items: center; gap: 7px;
    padding: 8px 16px; border-radius: 20px;
    font-size: .82rem; font-weight: 700;
}
.res-badge.green { background:#f0fdf4; color:#16a34a; border:1px solid #86efac; }
.res-badge.blue  { background:#eff6ff; color:var(--navy); border:1px solid #bfdbfe; }
.res-badge.amber { background:#fff7ed; color:#c2410c; border:1px solid #fdba74; }

/* ── ARO diagram ── */
.aro-wrap {
    background: linear-gradient(135deg,#f0f8ff,#e8f4fc);
    border: 1px solid var(--border); border-radius: 20px;
    padding: 28px; margin-top: 16px;
}
.aro-center { display: flex; justify-content: center; margin-bottom: 18px; }
.aro-root {
    background: linear-gradient(135deg,var(--navy),var(--ocean));
    color: #fff; border-radius: 50%; width: 90px; height: 90px;
    display: flex; align-items: center; justify-content: center;
    font-size: .72rem; font-weight: 800; text-align: center;
    box-shadow: 0 6px 24px rgba(2,62,138,.3); line-height: 1.3;
}
.aro-branches {
    display: flex; justify-content: center; gap: 12px; flex-wrap: wrap;
}
.aro-node {
    border-radius: 12px; padding: 12px 16px; text-align: center;
    font-size: .75rem; font-weight: 700;
    box-shadow: 0 3px 12px rgba(0,100,180,.1);
    cursor: default; transition: transform .2s, box-shadow .2s;
    min-width: 100px;
}
.aro-node:hover { transform: translateY(-3px); box-shadow: 0 8px 22px rgba(0,100,180,.18); }

/* ── hero imgs ── */
.hero-imgs {
    display: flex; flex-direction: column; gap: 12px;
    position: relative; z-index: 1;
}
.img-card {
    display: flex; align-items: center; gap: 12px;
    background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.18);
    border-radius: 14px; padding: 12px 18px; min-width: 220px;
    backdrop-filter: blur(8px);
}
</style>
"""
    st.markdown(HOME_CSS, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SECTION 1 — PRÉSENTATION DU PROJET
# ─────────────────────────────────────────────
def _section_presentation():
    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)

    # Hero
    st.markdown(
        """
        <div class="hero-wrap">
            <div class="hero-orb o1"></div><div class="hero-orb o2"></div><div class="hero-orb o3"></div>
            <div class="hero-left">
                <h1 class="hero-title">Résistance aux<br><span class="accent">Antibiotiques</span></h1>
                <p class="hero-subtitle">Prédiction computationnelle de la résistance aux antibiotiques par IA</p>
            </div>
            <div class="hero-imgs">
                <div class="img-card"><div class="img-ico">🧬</div><div>
                    <div class="img-txt">CARD Database</div>
                    <div class="img-sub">46 classes · 4k+ ARGs</div></div></div>
                <div class="img-card"><div class="img-ico">🦠</div><div>
                    <div class="img-txt">Résistance MDR</div>
                    <div class="img-sub">Souches multirésistantes</div></div></div>
                <div class="img-card"><div class="img-ico">🤖</div><div>
                    <div class="img-txt">Modèles IA</div>
                    <div class="img-sub">Multi-label Classification</div></div></div>
                <div class="img-card"><div class="img-ico">📈</div><div>
                    <div class="img-txt">Interprétabilité XAI</div>
                    <div class="img-sub">SHAP · LIME</div></div></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Contexte
    st.markdown(
        """
        <strong style="color:var(--navy);">Contexte :</strong>
        <div class="hbanner">
            La résistance aux antimicrobiens (RAM) est l'un des défis majeurs de la santé publique mondiale.
            L'émergence de souches multirésistantes (MDR) rend les traitements conventionnels inefficaces.
            Ce projet développe une alternative computationnelle basée sur l'IA pour prédire les profils
            de résistance <em>in silico</em> à partir de séquences protéiques bactériennes.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Objectifs + Travaux
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown(
            '<p class="sh-eyebrow">Objectifs du projet</p>', unsafe_allow_html=True
        )
        for num, title, desc in [
            (
                "01",
                "Pipeline de traitement",
                "Ingestion, nettoyage et annotation des séquences protéiques bactériennes.",
            ),
            (
                "02",
                "Module de prédiction",
                "Détection automatique des profils de résistance multi-label avec métriques F1 / AUC.",
            ),
            (
                "03",
                "Explicabilité IA (XAI)",
                "Visualisation des variables influentes pour des décisions interprétables.",
            ),
            (
                "04",
                "Interface sécurisée",
                "Soumission FASTA, probabilités et visualisation des explications.",
            ),
        ]:
            st.markdown(
                f"""
            <div class="obj-card">
                <div class="obj-num">{num}</div>
                <div><div class="obj-title">{title}</div><div class="obj-desc">{desc}</div></div>
            </div>""",
                unsafe_allow_html=True,
            )

    with col2:
        st.markdown(
            '<p class="sh-eyebrow">Travaux réalisés</p>', unsafe_allow_html=True
        )
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        for ico, title, desc in [
            (
                "🔗",
                "Embeddings protéiques",
                "Représentations numériques via ESM-2, ProtBERT…",
            ),
            (
                "⚖️",
                "Entraînement & Évaluation",
                "Classification multi-label : précision, rappel, F1-score, AUC.",
            ),
            (
                "💡",
                "Intégration XAI",
                "Analyse d'influence pour l'interprétabilité locale des prédictions.",
            ),
            (
                "🖥️",
                "Interface web FASTA",
                "Soumission de séquences et visualisation des explications.",
            ),
        ]:
            st.markdown(
                f"""
            <div class="comp-chip">
                <div class="chip-ico">{ico}</div>
                <div><div class="chip-title">{title}</div><div class="chip-desc">{desc}</div></div>
            </div>""",
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Boutons d'action ──────────────────────────────
    col_b1, col_b2, _ = st.columns([2, 2, 2])

    with col_b1:
        io_label = (
            "🔼 Masquer Input/Output"
            if st.session_state.show_io_box
            else "⬇️ Input / Output du modèle"
        )
        if st.button(io_label, key="btn_io", use_container_width=True, type="primary"):
            st.session_state.show_io_box = not st.session_state.show_io_box
            st.rerun()

    with col_b2:
        pip_label = (
            "🔼 Masquer le pipeline"
            if st.session_state.show_pipeline
            else "⚙️ Pipeline du projet →"
        )
        if st.button(
            pip_label, key="btn_pipeline", use_container_width=True, type="primary"
        ):
            st.session_state.show_pipeline = not st.session_state.show_pipeline
            st.rerun()

    # ── IO Box ───────────────────────────────────────
    if st.session_state.show_io_box:
        st.markdown(
            """
            <div class="io-box-wrap">
                <div class="io-container">
                    <p class="sh-eyebrow" style="text-align:center; margin-bottom:20px;">
                        Schéma Input → Output du modèle
                    </p>
                    <div class="io-row">
                        <!-- INPUT -->
                        <div class="io-card input-card">
                            <div class="io-label">📥 INPUT</div>
                            <div class="io-title">Séquence ARG</div>
                            <div class="io-desc">
                                Séquence protéique d'un gène de résistance antimicrobienne (ARG) au format FASTA
                            </div>
                            <div style="margin-top:12px; background:rgba(255,255,255,.12);
                                        border-radius:10px; padding:10px; font-family:monospace;
                                        font-size:.7rem; color:#caf0f8; text-align:left; line-height:1.6;">
                                &gt;ARO:3000004 | TEM-1<br>
                                MSIQHFRVALIPFFAAFCLPVFA<br>
                                HPETLVKVKDAEDQLGARVGYI...
                            </div>
                        </div>
                        <!-- ARROW -->
                        <div class="io-arrow-big">
                            <div style="font-size:2.2rem;">➜</div>
                            <div class="io-arrow-label">Modèle IA<br>Multi-label</div>
                            <div style="font-size:2.2rem;">➜</div>
                        </div>
                        <!-- OUTPUT -->
                        <div class="io-card output-card">
                            <div class="io-label">📤 OUTPUT</div>
                            <div class="io-title">Vecteur binaire de résistance</div>
                            <div class="io-desc">
                                Prédiction multi-label : 1 = résistance détectée, 0 = non résistant
                            </div>
                            <div class="binary-vector">
                                <div class="bit one">1</div>
                                <div class="bit zero">0</div>
                                <div class="bit one">1</div>
                                <div class="bit zero">0</div>
                                <div class="bit zero">0</div>
                                <div class="bit one">1</div>
                                <div class="bit zero">0</div>
                                <div class="bit special">M</div>
                            </div>
                            <div style="font-size:.65rem; color:rgba(255,255,255,.7);
                                        margin-top:8px; text-align:center;">
                                C1 | C2 | C3 | … | Cn | <span style="color:#ffe066;">MultiRésistance</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Pipeline 7 étapes ─────────────────────────────
    if st.session_state.show_pipeline:
        st.markdown(
            """
            <div class="pipeline-wrap">
                <p class="sh-eyebrow" style="text-align:center;">Pipeline Complet — 7 Étapes</p>
                <div style="text-align:center;font-size:1rem;font-weight:800;
                            color:var(--navy);margin-bottom:24px;">
                    Classification Multi-Label · Prédiction de la Résistance aux Antibiotiques
                </div>
                <!-- Ligne 1 : étapes 1-4 -->
                <div class="pipeline-steps">
                    <div class="pip-step">
                        <div class="step-num">Étape 01</div>
                        <span class="step-ico">📥</span>
                        <div class="step-title">Extraction CARD</div>
                    </div>
                    <div class="pip-arrow-h">→</div>
                    <div class="pip-step light">
                        <div class="step-num">Étape 02</div>
                        <span class="step-ico">🔬</span>
                        <div class="step-title">Filtrage Bactéricide</div>
                    </div>
                    <div class="pip-arrow-h">→</div>
                    <div class="pip-step">
                        <div class="step-num">Étape 03</div>
                        <span class="step-ico">🏷️</span>
                        <div class="step-title">Définition Labels</div>
                        <div class="step-tools">Familles thérapeutiques<br>MultiRésistance ≥ 2<br>MultiLabelBinarizer</div>
                    </div>
                    <div class="pip-arrow-h">→</div>
                    <div class="pip-step light">
                        <div class="step-num">Étape 04</div>
                        <span class="step-ico">🧫</span>
                        <div class="step-title">Validation Biologique</div>
                        <div class="step-tools">DIAMOND blastp<br>CD-HIT 90–95%<br>id≥30% · cov≥80%</div>
                    </div>
                </div>
                <!-- Flèche vers bas -->
                <div style="display:flex;justify-content:center;margin:4px 0;">
                    <div style="font-size:1.4rem;color:var(--ocean);font-weight:900;">↓</div>
                </div>
                <!-- Ligne 2 : étapes 5-7 (centrées) -->
                <div class="pipeline-steps" style="justify-content:center;">
                    <div class="pip-step light">
                        <div class="step-num">Étape 05</div>
                        <span class="step-ico">🧹</span>
                        <div class="step-title">Nettoyage Séquences</div>
                        <div class="step-tools">Suppr. X,B,Z,*,-<br>Padding / Truncation<br>BioPython · regex</div>
                    </div>
                    <div class="pip-arrow-h">→</div>
                    <div class="pip-step">
                        <div class="step-num">Étape 06</div>
                        <span class="step-ico">🔗</span>
                        <div class="step-title">Encodage / Embedding</div>
                        <div class="step-tools">K-mers (3–5)<br>ProtBERT / ESM-2<br>HuggingFace · sklearn</div>
                    </div>
                    <div class="pip-arrow-h">→</div>
                    <div class="pip-step accent">
                        <div class="step-num">Étape 07</div>
                        <span class="step-ico">📊</span>
                        <div class="step-title">Dataset Final</div>
                        <div class="step-tools">Matrice multi-label<br>Class weights · W-F1<br>scikit-learn · pandas</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SECTION 2 — BASE DE DONNÉES CARD
# ─────────────────────────────────────────────
def _render_image_carousel():
    """Carousel d'images moderne avec flèches et points JS."""
    img_paths = [
        ("assets/card/top1_card.jpg", "Top gènes de résistance — Vue 1"),
        ("assets/card/top2_card.png", "Distribution des classes ATB — Vue 2"),
        ("assets/card/top3_card.png", "Mécanismes de résistance — Vue 3"),
        ("assets/card/top7_card.png", "Analyse comparative — Vue 7"),
    ]

    n = len(img_paths)

    # Build slides HTML
    slides_html = ""
    dots_html = ""
    for i, (p, caption) in enumerate(img_paths):
        b64 = img_to_base64(p)
        active_dot = "active" if i == 0 else ""
        if b64:
            slides_html += f"""
            <div class="carousel-slide" id="slide-{i}">
                <img src="data:image/jpg;base64,{b64}" alt="{caption}">
                <div class="carousel-caption">
                    <div class="cap-num">Visualisation {i+1} / {n}</div>
                    <div class="cap-title">{caption}</div>
                </div>
            </div>"""
        else:
            slides_html += f"""
            <div class="carousel-slide" id="slide-{i}">
                <div class="slide-placeholder">
                    <div class="ph-icon">📊</div>
                    <div>{caption}</div>
                    <div style="font-size:.72rem;opacity:.6;">Image non disponible</div>
                </div>
            </div>"""
        dots_html += f'<button class="carousel-dot {active_dot}" onclick="goToSlide({i})" id="dot-{i}"></button>'

    html = f"""
    <div class="carousel-outer" id="main-carousel">
        <div class="carousel-track-wrap">
            <div class="carousel-track" id="carousel-track">
                {slides_html}
            </div>
        </div>
        <button class="carousel-btn prev" onclick="prevSlide()">&#8592;</button>
        <button class="carousel-btn next" onclick="nextSlide()">&#8594;</button>
        <div class="carousel-dots">{dots_html}</div>
    </div>

    <script>
    (function() {{
        var current = 0;
        var total = {n};
        var autoTimer = null;

        function updateCarousel(idx) {{
            current = (idx + total) % total;
            var track = document.getElementById('carousel-track');
            if (track) track.style.transform = 'translateX(-' + (current * 100) + '%)';
            for (var i = 0; i < total; i++) {{
                var dot = document.getElementById('dot-' + i);
                if (dot) dot.className = 'carousel-dot' + (i === current ? ' active' : '');
            }}
        }}

        window.prevSlide = function() {{ updateCarousel(current - 1); resetAuto(); }};
        window.nextSlide = function() {{ updateCarousel(current + 1); resetAuto(); }};
        window.goToSlide = function(i) {{ updateCarousel(i); resetAuto(); }};

        function resetAuto() {{
            if (autoTimer) clearInterval(autoTimer);
            autoTimer = setInterval(function() {{ updateCarousel(current + 1); }}, 5000);
        }}

        resetAuto();
    }})();
    </script>
    """
    st.markdown(html, unsafe_allow_html=True)


def _section_card():
    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
    st.markdown(
        '<div class="sh-title">Base de Données : CARD</div>', unsafe_allow_html=True
    )

    # ── Lien CARD box ──────────────────────────────────
    st.markdown(
        """
        <div class="card-link-box">
            <div>
                <div class="clb-title">🌐 CARD — Comprehensive Antibiotic Resistance Database</div>
                <div class="clb-desc">
                    Référence mondiale · Ontologie ARO · 4k+ gènes · McMaster University
                </div>
            </div>
            <a href="https://card.mcmaster.ca" target="_blank" class="card-link-btn">
                <i class="fa fa-external-link-alt"></i> card.mcmaster.ca
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-card">
            <p style="color:var(--text);line-height:1.85;font-size:.93rem;margin:0 0 16px;">
                <strong style="color:var(--navy);">CARD</strong>
                est la référence mondiale en bioinformatique pour l'analyse de la résistance aux antibiotiques.
                Elle compile les gènes ARGs, mutations associées et mécanismes moléculaires organisés autour
                d'une ontologie formelle : l'<strong>ARO (Antibiotic Resistance Ontology)</strong>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Bouton Composants CARD ───────────────────────
    label_comp = (
        "🔼 Masquer les composants"
        if st.session_state.show_card_components
        else "🧩 Composants CARD →"
    )
    if st.button(
        label_comp, key="btn_card_comp", use_container_width=True, type="primary"
    ):
        st.session_state.show_card_components = (
            not st.session_state.show_card_components
        )
        st.rerun()

    # Composants CARD (collapsible)
    if st.session_state.show_card_components:
        st.markdown(
            """
            <div class="pipeline-wrap" style="margin-top:0;">
                <p class="sh-eyebrow" style="text-align:center;margin-bottom:16px;">Composants de CARD</p>
                <div class="obj-card" style="border-left:4px solid var(--sky);">
                    <div class="obj-num">🧬</div>
                    <div><div class="obj-title">ARGs — Antibiotic Resistance Genes</div>
                    <div class="obj-desc">Catalogue des gènes de résistance connus et validés expérimentalement.</div></div>
                </div>
                <div class="obj-card" style="border-left:4px solid var(--cerulean);">
                    <div class="obj-num">🌐</div>
                    <div><div class="obj-title">ARO — Antibiotic Resistance Ontology</div>
                    <div class="obj-desc">Ontologie classant les gènes selon mécanismes et familles d'antibiotiques.</div></div>
                </div>
                <div class="obj-card" style="border-left:4px solid var(--ocean);">
                    <div class="obj-num">🔗</div>
                    <div><div class="obj-title">Séquences & Modèles de détection</div>
                    <div class="obj-desc">Séquences nucléotidiques/protéiques + BLAST, HMM, RGI.</div></div>
                </div>
                <div class="obj-card" style="border-left:4px solid var(--navy);">
                    <div class="obj-num">📋</div>
                    <div><div class="obj-title">Mécanismes & Preuves expérimentales</div>
                    <div class="obj-desc">Mode d'action des gènes avec validations issues de la littérature publiée.</div></div>
                </div>
                <div class="obj-card" style="border-left:4px solid var(--slate);">
                    <div class="obj-num">💊</div>
                    <div><div class="obj-title">Drug Classes — 46 familles</div>
                    <div class="obj-desc">Classification des antibiotiques en 46 familles structurales et fonctionnelles.</div></div>
                </div>
                <div class="obj-card" style="border-left:4px solid var(--cobalt);">
                    <div class="obj-num">⚙️</div>
                    <div><div class="obj-title">RGI — Resistance Gene Identifier</div>
                    <div class="obj-desc">Outil d'annotation automatique des gènes de résistance via BLAST et HMM.</div></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="hdiv"></div>', unsafe_allow_html=True)

    # ── Diagramme ARO ───────────────────────────────
    st.markdown(
        '<p class="sh-eyebrow">Architecture ARO dans CARD</p>', unsafe_allow_html=True
    )
    st.markdown(
        """
        <div class="aro-wrap">
            <div class="aro-center">
                <div class="aro-root">ARO<br>Ontologie</div>
            </div>
            <div class="aro-branches">
                <div class="aro-node" style="background:#eff6ff;color:var(--navy);">🛡️ Mécanisme<br>de résistance</div>
                <div class="aro-node" style="background:#f0fdf4;color:#16a34a;">🧬 Gène ARG<br>résistance</div>
                <div class="aro-node" style="background:linear-gradient(135deg,var(--sky),var(--cerulean));
                                           color:#fff;cursor:pointer;animation:pulse-drug 2s infinite;">💊 Drug<br>Class</div>
                <div class="aro-node" style="background:#fff7ed;color:#c2410c;">🦠 Organisme<br>pathogène</div>
                <div class="aro-node" style="background:#fdf4ff;color:#7e22ce;">⚗️ Molécule<br>antibiotique</div>
            </div>
        </div>
        <style>
        @keyframes pulse-drug {0%,100% {box-shadow:0 3px 12px rgba(0,180,216,.25);}50% {box-shadow:0 3px 24px rgba(0,180,216,.55);}}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ── Bouton Drug Class ────────────────────────────
    label_dc = (
        "🔼 Masquer les classes"
        if st.session_state.show_drug_panel
        else "💊 46 classes d'antibiotiques →"
    )
    if st.button(
        label_dc, key="btn_drug_panel", use_container_width=True, type="primary"
    ):
        st.session_state.show_drug_panel = not st.session_state.show_drug_panel
        st.rerun()

    if st.session_state.show_drug_panel:
        _render_drug_panel()

    st.markdown('<div class="hdiv"></div>', unsafe_allow_html=True)

    # ── Carousel d'images ───────────────────────────
    
    st.markdown(
        """
        <p style="font-size:.85rem;color:var(--muted);margin-bottom:12px;">
            Visualisation des top gènes de résistance dans CARD —
            <span style="color:var(--ocean);font-weight:600;">utilisez les flèches pour naviguer</span>
        </p>
        """,
        unsafe_allow_html=True,
    )

    _render_image_carousel()

    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  DRUG PANEL (grille des 46 classes)
# ─────────────────────────────────────────────
def _render_drug_panel():
    st.markdown(
        """
        <div class="drug-panel">
            <div style="display:flex;align-items:center;justify-content:space-between;
                        flex-wrap:wrap;gap:10px;margin-bottom:6px;">
                <div>
                    <span class="sh-eyebrow">Drug Classes CARD</span>
                    <div style="font-size:1rem;font-weight:800;color:var(--navy);">
                        46 Classes d'antibiotiques
                    </div>
                </div>
                <div class="res-badge blue">💊 46 classes · 4k+ gènes ARO</div>
            </div>
        """,
        unsafe_allow_html=True,
    )

    classes = list(CARD_CLASS_DETAILS.keys())
    cols = st.columns(3, gap="small")

    for i, cls_name in enumerate(classes):
        col = cols[i % 3]
        info = CARD_CLASS_DETAILS[cls_name]
        state_key = f"drug_{cls_name.replace(' ', '_').replace('-', '_')}"

        if state_key not in st.session_state:
            st.session_state[state_key] = None

        with col:
            st.markdown(
                f"""
                <div class="drug-card">
                    <div class="drug-name">💊 {cls_name.title()}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            c1, c2, c3 = st.columns(3)
            with c1:
                occ_active = st.session_state[state_key] == "occ"
                if st.button(
                    "📊 Occur." if not occ_active else "✕ Occur.",
                    key=f"occ_{state_key}",
                    use_container_width=True,
                ):
                    st.session_state[state_key] = None if occ_active else "occ"
                    st.rerun()
            with c2:
                desc_active = st.session_state[state_key] == "desc"
                if st.button(
                    "📖 Desc." if not desc_active else "✕ Desc.",
                    key=f"desc_{state_key}",
                    use_container_width=True,
                ):
                    st.session_state[state_key] = None if desc_active else "desc"
                    st.rerun()
            with c3:
                st.markdown(
                    f'<div style="font-size:.7rem;color:var(--muted);padding:6px 2px;'
                    f'text-align:center;">#{i+1}</div>',
                    unsafe_allow_html=True,
                )

            if st.session_state[state_key] == "occ":
                gene_count = info["genes"]
                max_genes = 3404
                pct = int(gene_count / max_genes * 100) if max_genes > 0 else 0
                st.markdown(
                    f"""
                    <div class="drug-detail">
                        <div class="drug-occ-badge">🧬 {gene_count:,} gènes ARO</div>
                        <div style="margin-top:8px;background:#e0f0fb;border-radius:6px;height:6px;">
                            <div style="background:var(--ocean);width:{pct}%;height:100%;border-radius:6px;"></div>
                        </div>
                        <div style="font-size:.7rem;color:var(--muted);margin-top:4px;">
                            {pct}% du maximum (Céphalosporine · 3404)
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            elif st.session_state[state_key] == "desc":
                st.markdown(
                    f'<div class="drug-detail">{info["desc"]}</div>',
                    unsafe_allow_html=True,
                )

            st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SECTION 3 — FILTRAGE BACTÉRICIDES
# ─────────────────────────────────────────────
def _section_filtrage():
    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
    st.markdown(
        '<div class="sh-title">Filtrage des Classes Bactéricides dans CARD</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #023e8a 0%, #0077b6 50%, #0096c7 100%);
                    border-radius: 24px;
                    padding: 40px 48px;
                    margin-bottom: 40px;
                    box-shadow: 0 20px 40px -12px rgba(2,62,138,0.35);
                    position: relative;
                    overflow: hidden;">
            <div style="position: absolute; top: -30%; right: -10%; width: 280px; height: 280px;
                        background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);">
            </div>
            <div style="position: absolute; bottom: -20%; left: -5%; width: 200px; height: 200px;
                        background: radial-gradient(circle, rgba(202,240,248,0.08) 0%, transparent 70%);">
            </div>
            <div style="position: relative; z-index: 2;">
                <div style="display: inline-block; background: rgba(255,255,255,0.15); backdrop-filter: blur(4px);
                            padding: 6px 16px; border-radius: 40px; margin-bottom: 24px;">
                    <span style="color: #caf0f8; font-size: 0.7rem; font-weight: 600; letter-spacing: 1px;">
                        🎯 MOTIVATION & OBJECTIF
                    </span>
                </div>
                <div style="display: flex; flex-wrap: wrap; gap: 32px;">
                    <div style="flex: 1.5; min-width: 280px;">
                        <h2 style="color: #fff; font-size: 1.6rem; font-weight: 700; margin-bottom: 20px; line-height: 1.3;">
                            Pourquoi distinguer les<br>
                            <span style="color: #caf0f8;">classes bactéricides</span> ?
                        </h2>
                        <p style="color: rgba(255,255,255,0.9); font-size: 0.95rem; line-height: 1.7; margin-bottom: 16px;">
                            L'ontologie ARO de la base CARD ne différencie pas actuellement les antibiotiques
                            selon leur activité bactéricide ou bactériostatique. Cette distinction est pourtant
                            essentielle pour :
                        </p>
                        <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-top: 24px;">
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <div style="width: 28px; height: 28px; background: rgba(202,240,248,0.2); border-radius: 8px;
                                            display: flex; align-items: center; justify-content: center;">
                                    <span style="font-size: 0.85rem;">🏥</span>
                                </div>
                                <span style="color: #fff; font-size: 0.85rem;">Orientation thérapeutique</span>
                            </div>
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <div style="width: 28px; height: 28px; background: rgba(202,240,248,0.2); border-radius: 8px;
                                            display: flex; align-items: center; justify-content: center;">
                                    <span style="font-size: 0.85rem;">⚕️</span>
                                </div>
                                <span style="color: #fff; font-size: 0.85rem;">Optimisation des traitements</span>
                            </div>
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <div style="width: 28px; height: 28px; background: rgba(202,240,248,0.2); border-radius: 8px;
                                            display: flex; align-items: center; justify-content: center;">
                                    <span style="font-size: 0.85rem;">🎯</span>
                                </div>
                                <span style="color: #fff; font-size: 0.85rem;">Précision des modèles prédictifs</span>
                            </div>
                        </div>
                    </div>
                    <div style="flex: 1; min-width: 260px; background: rgba(255,255,255,0.08); backdrop-filter: blur(8px);
                                border-radius: 20px; padding: 24px; border: 1px solid rgba(255,255,255,0.15);">
                        <div style="text-align: center;">
                            <div style="font-size: 2rem; margin-bottom: 12px;">💊</div>
                            <div style="color: #caf0f8; font-size: 0.75rem; font-weight: 600; margin-bottom: 12px;">
                                OBJECTIF PRINCIPAL
                            </div>
                            <div style="color: #fff; font-size: 1rem; font-weight: 600; margin-bottom: 16px;">
                                Identifier les classes à activité<br>
                                bactéricide parmi les 46 familles<br>
                                d'antibiotiques de CARD
                            </div>
                            <div style="color: rgba(255,255,255,0.75); font-size: 0.8rem; line-height: 1.5;">
                                Une information clé absente de l'ontologie ARO actuelle
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="margin-bottom: 32px;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px;">
                <div style="width: 4px; height: 28px; background: linear-gradient(135deg, #0077b6, #0096c7); border-radius: 4px;"></div>
                <div style="font-size: 1rem; font-weight: 700; color: #023e8a;">Approche méthodologique</div>
            </div>
            <p style="font-size: 0.9rem; color: #2d3e50; line-height: 1.7;">
                L'analyse combine l'exploration des descriptions ARO (Antibiotic Resistance Ontology)
                et une revue de la littérature biomédicale pour classer les 46 classes d'antibiotiques
                selon leur spectre d'activité : bactéricide strict, bactériostatique, double activité,
                ou non déterminé.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_a, col_b, col_c = st.columns(3, gap="large")
    for col, ico, color, title, desc in [
        (
            col_a,
            "🔍",
            "#0077b6",
            "Exploration CARD",
            "Analyse des descriptions ARO et des mécanismes d'action pour extraire les indices relatifs au caractère bactéricide.",
        ),
        (
            col_b,
            "📚",
            "#0096c7",
            "Références Scientifiques",
            "Validation par croisement avec la littérature biomédicale (ratio CMB/CMI, mécanismes lytiques).",
        ),
        (
            col_c,
            "✅",
            "#023e8a",
            "Classification Validée",
            "Établissement de la liste définitive des classes bactéricides strictes, intégrée comme label prioritaire dans les modèles AMR.",
        ),
    ]:
        with col:
            st.markdown(
                f"""
            <div style="background: #fff; border-radius: 20px; padding: 28px 24px;
                        border: 1px solid rgba(0,119,182,0.12);
                        box-shadow: 0 8px 24px rgba(0,0,0,0.04); height: 100%;">
                <div style="width: 52px; height: 52px; border-radius: 16px;
                            background: {color};
                            display: flex; align-items: center; justify-content: center;
                            font-size: 1.6rem; margin-bottom: 20px;
                            box-shadow: 0 8px 16px rgba(0,119,182,0.15);">
                    {ico}
                </div>
                <div style="font-size: 1rem; font-weight: 700; color: {color}; margin-bottom: 12px;">
                    {title}
                </div>
                <p style="font-size: 0.85rem; color: #4a627a; line-height: 1.6; margin: 0;">
                    {desc}
                </p>
            </div>
            """,
                unsafe_allow_html=True,
            )

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style="margin-top: 16px;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
                <div style="width: 4px; height: 28px; background: linear-gradient(135deg, #0077b6, #0096c7); border-radius: 4px;"></div>
                <div style="font-size: 1rem; font-weight: 700; color: #023e8a;">Résultat : Classification des 46 classes CARD</div>
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 16px; justify-content: space-between;">
                <div style="flex: 1; min-width: 180px; background: linear-gradient(135deg, #fef2f2, #fee2e2);
                            border-radius: 20px; padding: 24px 20px; text-align: center; border-left: 4px solid #dc2626;">
                    <div style="font-size: 2rem; font-weight: 800; color: #dc2626; margin-bottom: 8px;">8</div>
                    <div style="font-size: 0.8rem; font-weight: 600; color: #7f1a1a;">Bactéricide strict</div>
                </div>
                <div style="flex: 1; min-width: 180px; background: linear-gradient(135deg, #f0fdf4, #dcfce7);
                            border-radius: 20px; padding: 24px 20px; text-align: center; border-left: 4px solid #16a34a;">
                    <div style="font-size: 2rem; font-weight: 800; color: #16a34a; margin-bottom: 8px;">9</div>
                    <div style="font-size: 0.8rem; font-weight: 600; color: #14532d;">Bactériostatique</div>
                </div>
                <div style="flex: 1; min-width: 180px; background: linear-gradient(135deg, #fffbeb, #fef3c7);
                            border-radius: 20px; padding: 24px 20px; text-align: center; border-left: 4px solid #f59e0b;">
                    <div style="font-size: 2rem; font-weight: 800; color: #f59e0b; margin-bottom: 8px;">3</div>
                    <div style="font-size: 0.8rem; font-weight: 600; color: #78350f;">Double activité</div>
                </div>
                <div style="flex: 1; min-width: 180px; background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
                            border-radius: 20px; padding: 24px 20px; text-align: center; border-left: 4px solid #64748b;">
                    <div style="font-size: 2rem; font-weight: 800; color: #475569; margin-bottom: 8px;">26</div>
                    <div style="font-size: 0.8rem; font-weight: 600; color: #1e293b;">Non déterminées</div>
                </div>
            </div>
            <div style="font-size: 0.85rem; color: #4a627a; line-height: 1.6; margin-top: 28px; padding: 16px 20px;
                        background: #f8fafc; border-radius: 16px; border: 1px solid #e2e8f0;">
                <strong style="color: #023e8a;">🔬 Validation scientifique :</strong> La classification s'appuie sur l'analyse
                des descriptions ARO et une revue systématique de la littérature biomédicale, garantissant la fiabilité
                des 8 classes identifiées comme bactéricides strictes.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  RENDER PRINCIPAL
# ─────────────────────────────────────────────
def render():
    _init()
    inject_global_css()
    inject_home_css()

    # ── Navigation 3 sections ──────────────────
    c1, c2, c3 = st.columns(3)
    sections = [
        (1, "🏠 Présentation du Projet"),
        (2, "🗄️ Base de Données CARD"),
        (3, "🔬 Filtrage Bactéricides"),
    ]
    for col, (num, label) in zip([c1, c2, c3], sections):
        with col:
            is_active = st.session_state.home_section == num
            if st.button(
                label,
                key=f"sec_btn_{num}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state.home_section = num
                st.session_state.show_pipeline = False
                st.session_state.show_card_components = False
                st.session_state.show_drug_panel = False
                st.session_state.show_io_box = False
                st.session_state.card_viz_idx = 0
                st.rerun()

    st.markdown('<div class="hdiv"></div>', unsafe_allow_html=True)

    sec = st.session_state.home_section
    if sec == 1:
        _section_presentation()
    elif sec == 2:
        _section_card()
    elif sec == 3:
        _section_filtrage()
