import streamlit as st
from utils.helpers import inject_global_css
from utils.load_data import CARD_CLASS_DETAILS, CARD_ARO_GENES
from pathlib import Path
import base64
import streamlit.components.v1 as components


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
        "show_img_modal": False,
        "show_esm2_detail": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ─────────────────────────────────────────────
#  HELPER : Convertir image en Base64
# ─────────────────────────────────────────────
def img_to_base64(path: str) -> str | None:
    try:
        full_path = Path(path)
        if not full_path.exists():
            return None
        with open(full_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None


# ─────────────────────────────────────────────
#  CSS HOME  — uniquement les styles NON définis dans helpers.py
#  Les classes suivantes sont déjà dans helpers.py et ne sont PAS redéfinies ici :
#    .section-card, .obj-card, .obj-num, .obj-title, .obj-desc
#    .comp-chip, .chip-ico, .chip-title, .chip-desc
#    .hbanner, .hdiv, .sh-title, .sh-eyebrow, .info-card, .success-card, .warning-card
#    .hero-wrap, .hero-orb, .hero-left, .hero-title, .hero-subtitle
#    .hero-imgs, .img-card, .img-ico, .img-txt, .img-sub
#    .stat-badge, .stat-val, .stat-lbl
#    .badge-validated, .badge-bactericide
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
    /* ── Section wrapper (animation d'entrée) ── */
    .section-wrap { animation: fadeUp .35s ease both; }
    @keyframes fadeUp {
        from { opacity:0; transform:translateY(14px); }
        to   { opacity:1; transform:translateY(0); }
    }

    /* ── Pipeline wrap ── */
    .pipeline-wrap {
        background: linear-gradient(135deg,#C9D2DA, #D3DCE3);
        border: 1px solid var(--border); border-radius: 20px;
        padding: 32px 24px; margin-top: 16px;
        animation: fadeUp .3s ease both;
    }

    /* ── Pipeline steps ── */
    .pipeline-steps {
        display: flex; flex-wrap: wrap; gap: 0;
        align-items: stretch; justify-content: center; margin: 24px 0;
    }
    .pip-step {
        background: linear-gradient(135deg,var(--navy),var(--ocean));
        color: #fff; border-radius: 16px; padding: 16px 14px;
        text-align: center; min-width: 110px; max-width: 130px; flex: 1;
        box-shadow: 0 4px 14px rgba(2,62,138,.2);
        transition: transform .2s, box-shadow .2s;
    }
    .pip-step:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 24px rgba(2,62,138,.3); z-index: 2;
    }
    .pip-step.light { background: linear-gradient(135deg,var(--sky),var(--cerulean)); }
    .pip-step.accent {
        background: linear-gradient(135deg,#0a2463,var(--navy));
        box-shadow: 0 6px 20px rgba(2,62,138,.35);
    }
    .pip-step .step-num {
        font-size: .6rem; font-weight: 900; letter-spacing: 1.5px;
        opacity: .75; margin-bottom: 4px; text-transform: uppercase;
    }
    .pip-step .step-ico  { font-size: 1.5rem; margin-bottom: 6px; display: block; }
    .pip-step .step-title { font-size: .75rem; font-weight: 800; line-height: 1.3; margin-bottom: 4px; }
    .pip-step .step-tools { font-size: .72rem; opacity: .72; line-height: 1.4; }
    .pip-arrow-h {
        display: flex; align-items: center; color: var(--ocean);
        font-size: 1.1rem; font-weight: 900; padding: 0 4px; flex-shrink: 0;
    }

    /* ── IO Box ── */
    .io-box-wrap { animation: fadeUp .3s ease both; margin-top: 16px; }
    .io-container {
        background: linear-gradient(135deg, #C9D2DA, #D3DCE3);
        border: 1px solid var(--border); border-radius: 20px; padding: 28px; overflow: hidden;
    }
    .io-row {
        display: flex; align-items: center; gap: 16px; flex-wrap: wrap; justify-content: center;
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
        font-size: 1rem; font-weight: 800; letter-spacing: 2px;
        text-transform: uppercase; opacity: .8; margin-bottom: 10px;
    }
    .io-card .io-title { font-size: 1rem; font-weight: 800; margin-bottom: 8px; }
    .io-card .io-desc  { font-size: .78rem; opacity: .85; line-height: 1.5; }
    .io-arrow-big {
        font-size: 2rem; color: var(--ocean); flex-shrink: 0;
        display: flex; flex-direction: column; align-items: center; gap: 6px;
    }
    .io-arrow-big .io-arrow-label {
        font-size: 1rem; font-weight: 700; color: var(--navy);
        text-transform: uppercase; letter-spacing: 1px;
    }
    .binary-vector {
        display: flex; gap: 4px; flex-wrap: wrap; justify-content: center; margin-top: 10px;
    }
    .bit {
        width: 26px; height: 26px; border-radius: 6px;
        display: flex; align-items: center; justify-content: center;
        font-size: .78rem; font-weight: 800;
    }
    .bit.one     { background: rgba(255,255,255,.3); color: #0096c7; }
    .bit.zero    { background: rgba(255,255,255,.1); color: #000000; }
    .bit.special { background: rgba(255,200,50,.25); color: #ffe066; border: 1px solid rgba(255,200,50,.4); }

    /* ── CARD link box ── */
    .card-link-box {
        background: linear-gradient(135deg,var(--navy),var(--ocean));
        border-radius: 20px; padding: 24px 28px;
        display: flex; align-items: center; justify-content: space-between;
        flex-wrap: wrap; gap: 16px;
        box-shadow: 0 8px 28px rgba(2,62,138,.25); margin-bottom: 24px;
        animation: fadeUp .3s ease both;
    }
    .card-link-box .clb-title { font-size: 1.1rem; font-weight: 800; color: #fff; margin-bottom: 4px; }
    .card-link-box .clb-desc  { font-size: .82rem; color: rgba(202,240,248,.85); line-height: 1.5; }
    .card-link-btn {
        display: inline-flex; align-items: center; gap: 10px;
        background: #fff; color: var(--navy); border-radius: 40px; padding: 12px 24px;
        font-size: .88rem; font-weight: 800; text-decoration: none;
        box-shadow: 0 4px 16px rgba(0,0,0,.15); transition: transform .2s, box-shadow .2s;
        white-space: nowrap;
    }
    .card-link-btn:hover {
        transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,.2);
        color: var(--navy); text-decoration: none;
    }

    /* ── Galerie d'images verticale ── */
    .img-gallery-wrap { animation: fadeUp .35s ease both; margin-top: 16px; }
    .img-gallery-container {
        background: linear-gradient(135deg, #0d2137, var(--navy));
        border-radius: 20px; padding: 28px 24px;
        box-shadow: 0 12px 40px rgba(2,62,138,.25);
        display: flex; flex-direction: column; gap: 24px;
    }
    .img-gallery-item {
        background: rgba(255,255,255,.05);
        border: 1px solid rgba(255,255,255,.12);
        border-radius: 16px; overflow: hidden;
        transition: transform .2s, box-shadow .2s;
    }
    .img-gallery-item:hover {
        transform: translateY(-3px); box-shadow: 0 10px 30px rgba(0,0,0,.3);
    }
    .img-gallery-item img {
        width: 100%; max-height: 340px; object-fit: contain;
        display: block; background: #0d2137; padding: 16px;
    }
    .img-gallery-caption { padding: 14px 18px; background: rgba(0,0,0,.25); }
    .img-gallery-caption .cap-num {
        font-size: .62rem; font-weight: 700; color: var(--sky);
        letter-spacing: 1px; text-transform: uppercase; margin-bottom: 4px;
    }
    .img-gallery-caption .cap-title { font-size: .88rem; font-weight: 700; color: #0096c7; }
    .img-placeholder {
        display: flex; flex-direction: column; align-items: center;
        justify-content: center; height: 200px;
        background: linear-gradient(135deg, #0d2137, var(--navy));
        color: rgba(202,240,248,.6); gap: 10px; font-size: .88rem;
    }
    .img-placeholder .ph-icon { font-size: 2.5rem; }

    /* ── Drug panel ── */
    .drug-panel {
        background: #0096c7; border-radius: 20px; border: 1px solid var(--border);
        box-shadow: 0 8px 32px rgba(0,100,180,.1); padding: 24px;
        margin-top: 16px; animation: fadeUp .3s ease both;
    }
    .drug-card {
        background: #f8faff; border: 1px solid var(--border);
        border-radius: 14px; padding: 14px 16px;
        transition: box-shadow .2s; margin-bottom: 4px;
    }
    .drug-card:hover { box-shadow: 0 4px 16px rgba(0,100,180,.12); }
    .drug-name { font-size: .8rem; font-weight: 700; color: var(--navy); margin-bottom: 8px; line-height: 1.4; }
    .drug-detail {
        margin-top: 10px; padding: 10px 12px;
        background: linear-gradient(135deg,#f0f8ff,#e8f4fc);
        border-radius: 10px; font-size: .78rem; color: var(--text);
        line-height: 1.65; border-left: 3px solid var(--sky);
        animation: fadeUp .2s ease both;
    }
    .drug-occ-badge {
        display: inline-flex; align-items: center; gap: 6px;
        background: linear-gradient(135deg, #C9D2DA, #D3DCE3)
        color: #0096c7; border-radius: 20px; padding: 6px 14px;
        font-size: .82rem; font-weight: 800;
    }

    /* ── Result badges (locaux à home) ── */
    .res-badge {
        display: inline-flex; align-items: center; gap: 7px;
        padding: 8px 16px; border-radius: 20px; font-size: .82rem; font-weight: 700;
    }
    .res-badge.green { background:#f0fdf4; color:#16a34a; border:1px solid #86efac; }
    .res-badge.blue  { background:#eff6ff; color:var(--navy); border:1px solid #bfdbfe; }
    .res-badge.amber { background:#0096c77ed; color:#c2410c; border:1px solid #fdba74; }

    /* ── ARO diagram ── */
    .aro-wrap {
        background: linear-gradient(135deg,#f0f8ff,#e8f4fc);
        border: 1px solid var(--border); border-radius: 20px; padding: 28px; margin-top: 16px;
    }
    .aro-center { display: flex; justify-content: center; margin-bottom: 18px; }
    .aro-root {
        background: linear-gradient(135deg,var(--navy),var(--ocean));
        color: #fff; border-radius: 50%; width: 90px; height: 90px;
        display: flex; align-items: center; justify-content: center;
        font-size: .72rem; font-weight: 800; text-align: center;
        box-shadow: 0 6px 24px rgba(2,62,138,.3); line-height: 1.3;
    }
    .aro-branches { display: flex; justify-content: center; gap: 12px; flex-wrap: wrap; }
    .aro-node {
        border-radius: 12px; padding: 12px 16px; text-align: center;
        font-size: .75rem; font-weight: 700; box-shadow: 0 3px 12px rgba(0,100,180,.1);
        cursor: default; transition: transform .2s, box-shadow .2s; min-width: 100px;
    }
    .aro-node:hover { transform: translateY(-3px); box-shadow: 0 8px 22px rgba(0,100,180,.18); }
    @keyframes pulse-drug {
        0%,100% { box-shadow:0 3px 12px rgba(0,180,216,.25); }
        50%      { box-shadow:0 3px 24px rgba(0,180,216,.55); }
    }

    /* ── ESM-2 detail box ── */
    .esm2-detail-box {
        margin-top: 16px;
        background: linear-gradient(135deg, #f0f8ff, #e4f3fb);
        border: 1px solid var(--border); border-radius: 16px;
        padding: 22px 24px; animation: fadeUp .25s ease both;
        border-left: 4px solid var(--ocean);
    }
    .esm2-detail-box .esm2-title {
        font-size: .95rem; font-weight: 800; color: var(--navy); margin-bottom: 14px;
    }
    .esm2-feature-grid { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 12px; }
    .esm2-feature {
        background: linear-gradient(135deg, var(--navy), var(--ocean));
        color: #fff; border-radius: 10px; padding: 10px 14px;
        font-size: .75rem; font-weight: 700; flex: 1; min-width: 140px;
        text-align: center; line-height: 1.5;
    }
    </style>
    """
    st.markdown(HOME_CSS, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SECTION 1 — PRÉSENTATION DU PROJET
# ─────────────────────────────────────────────
def _section_presentation():
    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)

    # ── Hero — utilise les classes .hero-wrap, .hero-orb, .hero-title, .img-card de helpers.py ──
    st.markdown(
        """
        <div class="hero-wrap">
            <div class="hero-orb o1"></div>
            <div class="hero-orb o2"></div>
            <div class="hero-orb o3"></div>
            <div class="hero-left">
                <h1 class="hero-title">Résistance aux<br><span class="accent">Antibiotiques</span></h1>
                <p class="hero-subtitle">Prédiction computationnelle de la résistance aux antibiotiques par IA</p>
            </div>
            <div class="hero-imgs">
                <div class="img-card">
                    <div class="img-ico">🧬</div>
                    <div><div class="img-txt">CARD Database</div><div class="img-sub">46 classes · 4k+ ARGs</div></div>
                </div>
                <div class="img-card">
                    <div class="img-ico">🦠</div>
                    <div><div class="img-txt">Résistance MDR</div><div class="img-sub">Souches multirésistantes</div></div>
                </div>
                <div class="img-card">
                    <div class="img-ico">🤖</div>
                    <div><div class="img-txt">Modèles IA</div><div class="img-sub">Multi-label Classification</div></div>
                </div>
                <div class="img-card">
                    <div class="img-ico">📈</div>
                    <div><div class="img-txt">Interprétabilité XAI</div><div class="img-sub">SHAP · LIME</div></div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Contexte — utilise .hbanner de helpers.py ──
    st.markdown(
        """
        <strong style="color:var(--navy);">Contexte </strong>
        <div class="hbanner">
            La résistance aux antimicrobiens (RAM) est l'un des défis majeurs de la santé publique mondiale.
            L'émergence de souches multirésistantes (MDR) rend les traitements conventionnels inefficaces.
            Ce projet développe une alternative computationnelle basée sur l'IA pour prédire les profils
            de résistance <em>in silico</em> à partir de séquences protéiques bactériennes.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Objectifs + Travaux — utilise .obj-card, .comp-chip, .section-card de helpers.py ──
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown(
            '<p class="sh-eyebrow" style="color:var(--navy);">Objectifs du projet</p>',
            unsafe_allow_html=True,
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
                "Phase d’application sur souches réelles",
                "Sélection des souches, Extraction des protéines, Pipeline d’analyse, Analyse des résultats.",
            ),
            (
                "05",
                "Interprétation biologique",
                "La souche est-elle résistante ?, Quels types d’antibiotiques ?, Y a-t-il des homologues dangereux ?",
            ),
            (
                "06",
                "Interface sécurisée",
                "Soumission FASTA, probabilités et visualisation des explications.",
            ),
        ]:
            st.markdown(
                f"""
                <div class="obj-card">
                    <div class="obj-num">{num}</div>
                    <div>
                        <div class="obj-title">{title}</div>
                        <div class="obj-desc">{desc}</div>
                    </div>
                </div>""",
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Boutons d'action ──
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

    # ── IO Box ──
    if st.session_state.show_io_box:
        st.markdown(
            """
            <div class="io-box-wrap">
                <div class="io-container">
                    <p class="sh-eyebrow" style="text-align:center;margin-bottom:20px;">
                        Schéma Input → Output du modèle
                    </p>
                    <div class="io-row">
                        <div class="io-card input-card">
                            <div class="io-label">📥 INPUT</div>
                            <div class="io-title">Séquence ARG</div>
                            <div class="io-desc">
                                Séquence protéique d'un gène de résistance antimicrobienne (ARG) au format FASTA
                            </div>
                            <div style="margin-top:12px;background:rgba(255,255,255,.12);
                                        border-radius:10px;padding:10px;font-family:monospace;
                                        font-size:.7rem;color:#fff;text-align:left;line-height:1.6;">
                                &gt;ARO:3000004 | TEM-1<br>
                                MSIQHFRVALIPFFAAFCLPVFA<br>
                                HPETLVKVKDAEDQLGARVGYI...
                            </div>
                        </div>
                        <div class="io-arrow-big">
                            <div style="font-size:2.2rem;">➜</div>
                            <div class="io-arrow-label">Modèle IA<br>Multi-label</div>
                            <div style="font-size:2.2rem;">➜</div>
                        </div>
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
                            <div style="font-size:.65rem;color:rgba(255,255,255,.7);
                                        margin-top:8px;text-align:center;">
                                C1 | C2 | C3 | … | Cn | <span style="color:#ffe066;">MultiRésistance</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Pipeline (caché par défaut) ──
    if st.session_state.show_pipeline:
        st.markdown(
            """
            <div class="pipeline-wrap">
                <p class="sh-eyebrow" style="text-align:center;">Pipeline Complet — Prétraitement des données</p>
                <div style="text-align:center;font-size:1rem;font-weight:800;
                            color:var(--navy);margin-bottom:24px;">
                    Classification Multi-Label · Prédiction de la Résistance aux Antibiotiques
                </div>
                <!-- Ligne 1 : Étapes 1 → 4 -->
                <div class="pipeline-steps">
                    <div class="pip-step">
                        <div class="step-num">Étape 01</div>
                        <span class="step-ico">📥</span>
                        <div class="step-title">Extraction CARD</div>
                        <div class="step-tools">card.json · <br>ARO </div>
                    </div>
                    <div class="pip-arrow-h">→</div>
                    <div class="pip-step light">
                        <div class="step-num">Étape 02</div>
                        <span class="step-ico">🔬</span>
                        <div class="step-title">Filtrage Bactéricide</div>
                        <div class="step-tools">Critère pharmacologique<br></div>
                    </div>
                    <div class="pip-arrow-h">→</div>
                    <div class="pip-step">
                        <div class="step-num">Étape 03</div>
                        <span class="step-ico">🏷️</span>
                        <div class="step-title">Identification des classes d'antibiotiques</div>
                        <div class="step-tools">Familles thérapeutiques<br>MultiRésistance ≥ 2<br></div>
                    </div>
                    <div class="pip-arrow-h">→</div>
                    <div class="pip-step light">
                        <div class="step-num">Étape 04</div>
                        <span class="step-ico">🧬</span>
                        <div class="step-title">Extraction des Séquences</div>
                        <div class="step-tools">Séquences protéiques<br>ARG homolog model<br></div>
                    </div>
                </div>
                <!-- Flèche vers bas -->
                <div style="display:flex;justify-content:center;margin:4px 0;">
                    <div style="font-size:1.4rem;color:var(--ocean);font-weight:900;">↓</div>
                </div>
                <!-- Ligne 2 : Étapes 5 → 8 -->
                <div class="pipeline-steps">
                    <div class="pip-step">
                        <div class="step-num">Étape 05</div>
                        <span class="step-ico">🧹</span>
                        <div class="step-title">Nettoyage Séquences</div>
                        <div class="step-tools">Suppression des caractères invalides<br></div>
                    </div>
                    <div class="pip-arrow-h">→</div>
                    <div class="pip-step light">
                        <div class="step-num">Étape 06</div>
                        <span class="step-ico">🗄️</span>
                        <div class="step-title">Dataset Négatif<br>(UniProt)</div>
                        <div class="step-tools">DIAMOND blastp<br>id≥30% · cov≥80%<br>CD-HIT 90–95%</div>
                    </div>
                    <div class="pip-arrow-h">→</div>
                    <div class="pip-step accent">
                        <div class="step-num">Étape 07</div>
                        <span class="step-ico">🔗</span>
                        <div class="step-title">Encodage / Embedding<br>ESM-2</div>
                        <div class="step-tools">ESM-2 · HuggingFace<br>Embeddings denses<br></div>
                    </div>
                    <div class="pip-arrow-h">→</div>
                    <div class="pip-step light">
                        <div class="step-num">Étape 08</div>
                        <span class="step-ico">🗃️</span>
                        <div class="step-title">Construction du Dataset Final & Gestion du Déséquilibre<br></div>
                        <div class="step-tools">
                            Matrice multi-label (0 = sensible à la classe, 1 = résistant à la classe) 
                        </div> 
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Bouton ESM-2 détail ──
        esm2_label = (
            "🔼 Masquer les détails ESM-2"
            if st.session_state.show_esm2_detail
            else "🔬 Voir détails ESM-2"
        )
        if st.button(
            esm2_label, key="btn_esm2", use_container_width=False, type="secondary"
        ):
            st.session_state.show_esm2_detail = not st.session_state.show_esm2_detail
            st.rerun()

        if st.session_state.show_esm2_detail:
            st.markdown(
                """
                <div class="esm2-detail-box">
                    <div class="esm2-title">🔗 ESM-2 — Evolutionary Scale Modeling (Meta AI)</div>
                    <p style="font-size:.82rem;color:var(--text);line-height:1.75;margin-bottom:14px;">
                        <strong style="color:var(--navy);">ESM-2</strong> est un modèle de langage protéique
                        (Protein Language Model) développé par Meta AI Research, pré-entraîné sur des centaines
                        de millions de séquences protéiques issues de UniRef. Il génère des
                        <strong>embeddings denses</strong> qui capturent le contexte évolutif, structural
                        et fonctionnel de chaque séquence, sans nécessiter d'alignement multiple ou
                        d'informations structurales explicites.
                    </p>
                    <div class="esm2-feature-grid">
                        <div class="esm2-feature">
                            🧠 Architecture<br>
                            <span style="font-weight:400;font-size:.68rem;opacity:.85;">
                                Transformer encoder<br>jusqu'à 15 milliards de paramètres
                            </span>
                        </div>
                        <div class="esm2-feature">
                            📐 Dimension<br>
                            <span style="font-weight:400;font-size:.68rem;opacity:.85;">
                                Embeddings de 480 à 5120 dimensions<br>selon la taille du modèle
                            </span>
                        </div>
                        <div class="esm2-feature">
                            🗃️ Pré-entraînement<br>
                            <span style="font-weight:400;font-size:.68rem;opacity:.85;">
                                250M séquences UniRef50<br>Masked Language Modeling
                            </span>
                        </div>
                        <div class="esm2-feature">
                            🎯 Avantage clé<br>
                            <span style="font-weight:400;font-size:.68rem;opacity:.85;">
                                Capture contexte évolutif<br>&amp; motifs de résistance locaux
                            </span>
                        </div>
                        <div class="esm2-feature">
                            ⚙️ Intégration<br>
                            <span style="font-weight:400;font-size:.68rem;opacity:.85;">
                                HuggingFace Transformers<br>Fine-tuning &amp; feature extraction
                            </span>
                        </div>
                        <div class="esm2-feature">
                            📊 Usage dans le pipeline<br>
                            <span style="font-weight:400;font-size:.68rem;opacity:.85;">
                                Vecteur par séquence ARG<br>→ entrée du classifieur multi-label
                            </span>
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
def _render_image_gallery():
    """Affichage vertical propre avec images + captions stylés"""
    st.image(
        "assets/card/top1_card.jpg",
        use_container_width=True,
    )
    st.image(
        "assets/card/top2_card.png",
        use_container_width=True,
    )
    st.image(
        "assets/card/top3_card.png",
        use_container_width=True,
    )
    st.image(
        "assets/card/top7_card.png",
        use_container_width=True,
    )


def _section_card():
    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)

    # .sh-title défini dans helpers.py
    st.markdown(
        '<div class="sh-title">Base de Données : CARD</div>', unsafe_allow_html=True
    )

    # ── Lien CARD box (spécifique home.py) ──
    st.markdown(
        """
        <div class="card-link-box">
            <div>
                <div class="clb-title">🌐 CARD — Comprehensive Antibiotic Resistance Database</div>
                <div class="clb-desc">Référence mondiale · Ontologie ARO · 4k+ gènes · McMaster University</div>
            </div>
            <a href="https://card.mcmaster.ca" target="_blank" class="card-link-btn">
                <i class="fa fa-external-link-alt"></i> card.mcmaster.ca
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # .section-card défini dans helpers.py
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

    # ── Bouton Composants CARD ──
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

    if st.session_state.show_card_components:
        # .pipeline-wrap (home.py) + .obj-card (helpers.py)
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
                    <div><div class="obj-title">Séquences &amp; Modèles de détection</div>
                    <div class="obj-desc">Séquences nucléotidiques/protéiques + BLAST, HMM, RGI.</div></div>
                </div>
                <div class="obj-card" style="border-left:4px solid var(--navy);">
                    <div class="obj-num">📋</div>
                    <div><div class="obj-title">Mécanismes &amp; Preuves expérimentales</div>
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

    # # .hdiv défini dans helpers.py
    # st.markdown('<div class="hdiv"></div>', unsafe_allow_html=True)

    # ── Diagramme ARO ──
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
                <div class="aro-node" style="background:#f0fdf4;color:var(--navy);">🧬 Gène ARG<br>résistance</div>
                <div class="aro-node" style="background:linear-gradient(135deg,var(--sky),var(--cerulean));
                                             color:var(--navy);animation:pulse-drug 2s infinite;">💊 Drug<br>Class</div>
                <div class="aro-node" style="background:#0096c77ed;color:var(--navy);">🦠 Organisme<br>pathogène</div>
                <div class="aro-node" style="background:#fdf4ff;color:var(--navy);">⚗️ Molécule<br>antibiotique</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Bouton Drug Class ──
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

    # # .hdiv défini dans helpers.py
    # st.markdown('<div class="hdiv"></div>', unsafe_allow_html=True)

    # ── Bouton galerie images ──
    img_label = (
        "🔼 Masquer les visualisations"
        if st.session_state.show_img_modal
        else "📊 Voir résultats →"
    )
    if st.button(
        img_label, key="btn_img_modal", use_container_width=True, type="primary"
    ):
        st.session_state.show_img_modal = not st.session_state.show_img_modal
        st.rerun()

    if st.session_state.show_img_modal:
        # .sh-eyebrow défini dans helpers.py
        st.markdown(
            '<p class="sh-eyebrow" style="margin:16px 0 8px;">'
            "Visualisation de la distribution des classes d'antibiotiques dans CARD"
            "</p>",
            unsafe_allow_html=True,
        )
        _render_image_gallery()

    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  DRUG PANEL (grille des 46 classes)
# ─────────────────────────────────────────────
def _render_drug_panel():
    # .sh-eyebrow, .res-badge (home.py) utilisés ici
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

            if st.session_state[state_key] == "occ":
                gene_count = info["genes"]

                st.markdown(
                    f"""
                    <div class="drug-detail">
                        <div class="drug-occ-badge">🧬 {gene_count:,} gènes ARO</div>
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

    # .sh-title défini dans helpers.py
    st.markdown(
        '<div class="sh-title">Filtrage des Classes Bactéricides dans CARD</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="background:linear-gradient(135deg,var(--navy) 0%,var(--ocean) 50%,var(--cerulean) 100%);
                    border-radius:24px;padding:40px 48px;margin-bottom:40px;
                    box-shadow:0 20px 40px -12px rgba(2,62,138,0.35);
                    position:relative;overflow:hidden;">
            <div style="position:absolute;top:-30%;right:-10%;width:280px;height:280px;
                        background:radial-gradient(circle,rgba(255,255,255,0.08) 0%,transparent 70%);"></div>
            <div style="position:absolute;bottom:-20%;left:-5%;width:200px;height:200px;
                        background:radial-gradient(circle,rgba(202,240,248,0.08) 0%,transparent 70%);"></div>
            <div style="position:relative;z-index:2;">
                <div style="display:inline-block;background:rgba(255,255,255,0.15);backdrop-filter:blur(4px);
                            padding:6px 16px;border-radius:40px;margin-bottom:24px;">
                    <span style="color:var(--ice);font-size:0.7rem;font-weight:600;letter-spacing:1px;">
                        🎯 MOTIVATION &amp; OBJECTIF
                    </span>
                </div>
                <div style="display:flex;flex-wrap:wrap;gap:32px;">
                    <div style="flex:1.5;min-width:280px;">
                        <h2 style="color:var(--ice);font-size:1.6rem;font-weight:700;margin-bottom:20px;line-height:1.3;">
                            Pourquoi distinguer les<br>
                            <span style="color:var(--ice);">classes bactéricides</span> ?
                        </h2>
                        <p style="color:#000000;font-size:0.95rem;line-height:1.7;margin-bottom:16px;">
                            L'ontologie ARO de la base CARD ne différencie pas actuellement les antibiotiques
                            selon leur activité bactéricide ou bactériostatique. Cette distinction est pourtant
                            essentielle pour :
                        </p>
                        <div style="display:flex;flex-wrap:wrap;gap:20px;margin-top:24px;">
                            <div style="display:flex;align-items:center;gap:12px;">
                                <div style="width:28px;height:28px;background:rgba(202,240,248,0.2);border-radius:8px;
                                            display:flex;align-items:center;justify-content:center;">🏥</div>
                                <span style="color:var(--ice);font-size:0.85rem;">Orientation thérapeutique</span>
                            </div>
                            <div style="display:flex;align-items:center;gap:12px;">
                                <div style="width:28px;height:28px;background:rgba(202,240,248,0.2);border-radius:8px;
                                            display:flex;align-items:center;justify-content:center;">⚕️</div>
                                <span style="color:var(--ice);font-size:0.85rem;">Optimisation des traitements</span>
                            </div>
                            <div style="display:flex;align-items:center;gap:12px;">
                                <div style="width:28px;height:28px;background:rgba(202,240,248,0.2);border-radius:8px;
                                            display:flex;align-items:center;justify-content:center;">🎯</div>
                                <span style="color:var(--ice);font-size:0.85rem;">Précision des modèles prédictifs</span>
                            </div>
                        </div>
                    </div>
                    <div style="flex:1;min-width:260px;background:rgba(255,255,255,0.08);backdrop-filter:blur(8px);
                                border-radius:20px;padding:24px;border:1px solid rgba(255,255,255,0.15);">
                        <div style="text-align:center;">
                            <div style="font-size:2rem;margin-bottom:12px;">💊</div>
                            <div style="color:var(--ice);font-size:1.25rem;font-weight:600;margin-bottom:12px;">
                                OBJECTIF PRINCIPAL
                            </div>
                            <div style="color:rgba(255,255,255,0.75);font-size:1rem;font-weight:600;margin-bottom:16px;">
                                Identifier les classes à activité<br>bactéricide parmi les 46 familles<br>
                                d'antibiotiques de CARD
                            </div>
                            <div style="color:rgba(255,255,255,0.75);font-size:0.8rem;line-height:1.5;">
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

    # .hbanner défini dans helpers.py
    st.markdown(
        """
        <div class="hbanner">
            <strong>Approche méthodologique :</strong>
            L'analyse combine l'exploration des descriptions ARO (Antibiotic Resistance Ontology)
            et une revue de la littérature biomédicale pour classer les 46 classes d'antibiotiques
            selon leur spectre d'activité : bactéricide strict, bactériostatique, double activité,
            ou non déterminé.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_a, col_b, col_c = st.columns(3, gap="large")
    for col, ico, color, title, desc in [
        (
            col_a,
            "🔍",
            "var(--ocean)",
            "Exploration CARD",
            "Analyse des descriptions ARO et des mécanismes d'action pour extraire les indices relatifs au caractère bactéricide.",
        ),
        (
            col_b,
            "📚",
            "var(--cerulean)",
            "Références Scientifiques",
            "Validation par croisement avec la littérature biomédicale (ratio CMB/CMI, mécanismes lytiques).",
        ),
        (
            col_c,
            "✅",
            "var(--navy)",
            "Classification Validée",
            "Établissement de la liste définitive des classes bactéricides strictes, intégrée comme label prioritaire dans les modèles AMR.",
        ),
    ]:
        with col:
            # .section-card défini dans helpers.py
            st.markdown(
                f"""
                <div class="section-card" style="height:100%;">
                    <div style="width:52px;height:52px;border-radius:16px;background:{color};
                                display:flex;align-items:center;justify-content:center;
                                font-size:1.6rem;margin-bottom:20px;
                                box-shadow:0 8px 16px rgba(0,119,182,0.15);">
                        {ico}
                    </div>
                    <div style="font-size:1rem;font-weight:700;color:{color};margin-bottom:12px;">{title}</div>
                    <p style="font-size:0.85rem;color:var(--muted);line-height:1.6;margin:0;">{desc}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    # # .hdiv défini dans helpers.py
    # st.markdown('<div class="hdiv"></div>', unsafe_allow_html=True)

    # .success-card défini dans helpers.py
    st.markdown(
        """
        <div class="success-card" style="margin-top:28px;">
            <strong>🔬 Validation scientifique :</strong> La classification s'appuie sur l'analyse
            des descriptions ARO et une revue systématique de la littérature biomédicale, garantissant
            la fiabilité des classes identifiées comme bactéricides.
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
    inject_global_css()  # helpers.py : palette, hero, obj-card, hbanner, hdiv, section-card…
    inject_home_css()  # home.py    : pipeline, io-box, gallery, drug-panel, aro, esm2…

    # ── Navigation 3 sections ──
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
                st.session_state.show_img_modal = False
                st.session_state.show_esm2_detail = False
                st.session_state.card_viz_idx = 0
                st.rerun()

    # # .hdiv défini dans helpers.py
    # st.markdown('<div class="hdiv"></div>', unsafe_allow_html=True)

    sec = st.session_state.home_section
    if sec == 1:
        _section_presentation()
    elif sec == 2:
        _section_card()
    elif sec == 3:
        _section_filtrage()
