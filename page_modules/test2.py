import streamlit as st
from utils.helpers import inject_global_css


# ─────────────────────────────────────────────
#  Session state
# ─────────────────────────────────────────────
def _init():
    defaults = {
        "pipeline_step": None,
        "show_md5_detail": False,
        "show_cdhit_detail": False,
        "show_x_analysis": False,
        "show_data_leakage": False,
        "show_union_detail": False,
        "show_md5_vs_cdhit": False,
        "show_dedup_conclusion": False,
        "show_cdhit_algo": False,
        "show_cdhit_params": False,
        "show_clstr_format": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ─────────────────────────────────────────────
#  CSS local — Design moderne
# ─────────────────────────────────────────────
def _inject_pipeline_css():
    st.markdown(
        """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

    /* ── Animations ── */
    .pl-wrap { animation: plFadeUp .4s cubic-bezier(.16,1,.3,1) both; }
    @keyframes plFadeUp {
        from { opacity:0; transform:translateY(18px); }
        to   { opacity:1; transform:translateY(0); }
    }
    @keyframes shimmer {
        0%   { background-position: -200% center; }
        100% { background-position: 200% center; }
    }
    @keyframes pulse-ring {
        0%   { box-shadow: 0 0 0 0 rgba(0,180,216,.35); }
        70%  { box-shadow: 0 0 0 10px rgba(0,180,216,0); }
        100% { box-shadow: 0 0 0 0 rgba(0,180,216,0); }
    }

    /* ── Contenu étape — carte principale ── */
    .step-content {
        background: #ffffff;
        border: 1px solid rgba(0,180,216,.15);
        border-radius: 24px;
        padding: 32px 36px;
        margin-top: 10px;
        box-shadow: 0 8px 40px rgba(2,62,138,.08), 0 2px 8px rgba(0,0,0,.04);
        animation: plFadeUp .35s cubic-bezier(.16,1,.3,1) both;
        position: relative;
        overflow: hidden;
    }
    .step-content::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--navy), var(--ocean), var(--sky));
    }

    .step-header {
        display: flex; align-items: center; gap: 16px;
        margin-bottom: 24px;
    }
    .step-num-badge {
        background: linear-gradient(135deg, var(--navy), var(--ocean));
        color: #fff; border-radius: 10px;
        padding: 7px 14px; font-size: .65rem;
        font-weight: 800; letter-spacing: 2px; text-transform: uppercase;
        white-space: nowrap; font-family: 'monospace', sans-serif;
    }
    .step-title-big {
        font-size: 1.3rem; font-weight: 800; color: var(--navy);
        font-family: 'monospace', sans-serif; letter-spacing: -.3px;
    }

    /* ── Pipeline overview ── */
    .pipeline-overview {
        background: linear-gradient(135deg, #0a1628 0%, #023e8a 50%, #0077b6 100%);
        border-radius: 24px; padding: 32px 28px;
        margin-bottom: 24px;
        position: relative; overflow: hidden;
        box-shadow: 0 16px 50px rgba(2,62,138,.28);
    }
    .pipeline-overview::before {
        content: '';
        position: absolute; inset: 0;
        background: radial-gradient(ellipse at 70% 0%, rgba(0,180,216,.2) 0%, transparent 60%),
                    radial-gradient(ellipse at 10% 100%, rgba(202,240,248,.1) 0%, transparent 50%);
        pointer-events: none;
    }
    .po-eyebrow {
        text-align: center;
        font-size: .65rem; letter-spacing: 3px; text-transform: uppercase;
        color: rgba(202,240,248,.7); font-weight: 700;
        margin-bottom: 6px; font-family: 'Space Grotesk', sans-serif;
    }
    .po-title {
        text-align: center;
        font-size: 1.1rem; font-weight: 800;
        color: #fff; margin-bottom: 24px;
        font-family: 'monospace', sans-serif; letter-spacing: -.2px;
    }
    .pipeline-flow {
        display: flex; flex-wrap: wrap;
        align-items: stretch; gap: 0;
        justify-content: center;
    }
    .pf-step {
        background: rgba(255,255,255,.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,.18);
        color: #fff; border-radius: 16px;
        padding: 18px 16px; text-align: center;
        min-width: 120px; max-width: 155px; flex: 1;
        transition: transform .25s, background .25s;
        position: relative;
    }
    .pf-step:hover {
        transform: translateY(-5px);
        background: rgba(255,255,255,.18);
    }
    .pf-step.active-step {
        background: rgba(255,255,255,.2);
        border-color: rgba(0,180,216,.5);
        animation: pulse-ring 2s infinite;
    }
    .pf-step .pf-num  { font-size:.58rem; font-weight:700; letter-spacing:2px; opacity:.65; margin-bottom:6px; text-transform: uppercase; }
    .pf-step .pf-ico  { font-size:1.6rem; margin-bottom:8px; display:block; }
    .pf-step .pf-name { font-size:.75rem; font-weight:700; line-height:1.35; font-family: 'monospace', sans-serif; }
    .pf-step .pf-cnt  { font-size:.68rem; opacity:.65; margin-top:6px; font-family: 'monospace', sans-serif; }
    .pf-step .pf-status {
        display: inline-block; margin-top: 8px;
        font-size: .58rem; font-weight: 700; letter-spacing: 1px;
        background: rgba(255,255,255,.15); border-radius: 20px;
        padding: 2px 8px; color: rgba(202,240,248,.9);
    }
    .pf-arrow {
        display: flex; align-items: center; justify-content: center;
        color: rgba(202,240,248,.5); font-size:.9rem;
        padding: 0 8px; flex-shrink: 0;
    }
    .po-hint {
        text-align: center; font-size: .75rem;
        color: rgba(202,240,248,.5); margin-top: 14px;
        font-style: italic;
    }

    /* ── Boîte définition ── */
    .def-box {
        background: linear-gradient(135deg, #f0f8ff, #e4f3fb);
        border: 1px solid rgba(0,180,216,.2);
        border-left: 4px solid var(--ocean);
        border-radius: 16px;
        padding: 22px 26px;
        margin-top: 14px;
        animation: plFadeUp .25s cubic-bezier(.16,1,.3,1) both;
    }
    .def-box .def-title {
        font-size: .95rem; font-weight: 800;
        color: var(--navy); margin-bottom: 12px;
        font-family: 'monospace', sans-serif;
    }
    .def-box p { font-size: .85rem; color: var(--text); line-height: 1.9; margin: 0; }

    /* ── Data leakage box ── */
    .leakage-box {
        background: linear-gradient(135deg, #fff5f5, #ffe8e8);
        border: 1px solid #fca5a5;
        border-left: 4px solid #ef4444;
        border-radius: 16px;
        padding: 22px 26px;
        margin-top: 14px;
        animation: plFadeUp .25s cubic-bezier(.16,1,.3,1) both;
    }
    .leakage-box .lb-title {
        font-size: .95rem; font-weight: 800;
        color: #991b1b; margin-bottom: 14px;
        font-family: 'monospace', sans-serif;
    }
    .leakage-box p { font-size: .85rem; color: #7f1d1d; line-height: 1.9; margin: 0 0 12px; }
    .leakage-example {
        background: rgba(239,68,68,.07);
        border-radius: 12px; padding: 14px 18px;
        font-size: .82rem; color: #7f1d1d;
        line-height: 1.8; margin-top: 10px;
        border: 1px dashed #fca5a5;
    }

    /* ── Union strategy box ── */
    .union-box {
        background: linear-gradient(135deg, #f0fdf4, #dcfce7);
        border: 1px solid #86efac;
        border-left: 4px solid #16a34a;
        border-radius: 16px;
        padding: 22px 26px;
        margin-top: 14px;
        animation: plFadeUp .25s cubic-bezier(.16,1,.3,1) both;
    }
    .union-box .ub-title {
        font-size: .95rem; font-weight: 800;
        color: #14532d; margin-bottom: 12px;
        font-family: 'monospace', sans-serif;
    }
    .union-box p { font-size: .85rem; color: #166534; line-height: 1.9; margin: 0 0 10px; }

    /* ── Métriques ── */
    .metrics-row { display:flex; gap:14px; flex-wrap:wrap; margin:20px 0; }
    .metric-card {
        flex:1; min-width:115px;
        background: linear-gradient(135deg, var(--navy), var(--ocean));
        border-radius:18px; padding:20px 16px;
        text-align:center; color:#fff;
        box-shadow: 0 6px 20px rgba(2,62,138,.22);
        position: relative; overflow: hidden;
        transition: transform .2s;
    }
    .metric-card:hover { transform: translateY(-3px); }
    .metric-card::after {
        content: '';
        position: absolute; top: -30px; right: -20px;
        width: 80px; height: 80px; border-radius: 50%;
        background: rgba(255,255,255,.06);
    }
    .metric-card .mc-val { font-size:1.55rem; font-weight:900; margin-bottom:5px; font-family: 'monospace', sans-serif; }
    .metric-card .mc-lbl { font-size:.68rem; opacity:.78; letter-spacing:.5px; line-height:1.5; }
    .metric-card.light { background: linear-gradient(135deg, var(--sky), var(--cerulean)); }
    .metric-card.green { background: linear-gradient(135deg, #15803d, #22c55e); }
    .metric-card.amber { background: linear-gradient(135deg, #b45309, #f59e0b); }
    .metric-card.red   { background: linear-gradient(135deg, #991b1b, #ef4444); }

    /* ── Tag justification ── */
    .justif-tag {
        background: #fffbeb; border:1px solid #fcd34d;
        border-left: 3px solid #f59e0b;
        border-radius: 10px; padding: 12px 16px;
        font-size: .82rem; color: #78350f;
        margin-top: 12px; line-height: 1.8;
    }

    /* ── Analyse X ── */
    .x-seq-card {
        background: #fffbeb; border: 1px solid #fcd34d;
        border-left: 4px solid #f59e0b;
        border-radius: 14px; padding: 16px 20px;
        margin-bottom: 12px;
        transition: box-shadow .2s;
    }
    .x-seq-card:hover { box-shadow: 0 4px 16px rgba(245,158,11,.15); }
    .x-seq-card .xsc-header {
        font-size: .85rem; font-weight: 800;
        color: #78350f; margin-bottom: 8px;
        font-family: 'monospace', sans-serif;
    }
    .x-seq-card .xsc-seq {
        font-family: 'JetBrains Mono', 'Courier New', monospace; font-size: .78rem;
        background: rgba(0,0,0,.06); border-radius: 8px;
        padding: 8px 12px; color: #1a1a1a; margin-bottom: 10px;
        border: 1px solid rgba(0,0,0,.08); letter-spacing: .3px;
    }
    .x-seq-card .xsc-row { font-size: .8rem; color: #5d4037; line-height: 1.8; }

    /* ── Result highlight ── */
    .result-highlight {
        background: linear-gradient(135deg, var(--navy) 0%, var(--ocean) 100%);
        border-radius: 20px; padding: 24px 28px;
        color: #fff; margin: 18px 0;
        box-shadow: 0 8px 30px rgba(2,62,138,.25);
        position: relative; overflow: hidden;
    }
    .result-highlight::before {
        content: '';
        position: absolute; top: -40px; right: -20px;
        width: 140px; height: 140px; border-radius: 50%;
        background: rgba(255,255,255,.06);
    }
    .result-highlight .rh-title {
        font-size: .65rem; font-weight: 800;
        letter-spacing: 2.5px; text-transform: uppercase;
        opacity: .7; margin-bottom: 8px; font-family: 'Space Grotesk', sans-serif;
    }
    .result-highlight .rh-val {
        font-size: 1.7rem; font-weight: 900; margin-bottom: 6px;
        font-family: 'monospace', sans-serif;
    }
    .result-highlight .rh-desc {
        font-size: .83rem; opacity: .82; line-height: 1.65;
    }

    /* ── Sub-section title ── */
    .subsection-title {
        font-size: 1rem; font-weight: 800;
        color: var(--navy); margin: 22px 0 12px;
        padding-left: 14px;
        border-left: 3px solid var(--sky);
        font-family: 'monospace', sans-serif;
    }

    /* ── Approche card ── */
    .approche-card {
        background: #ffffff;
        border: 1px solid rgba(0,180,216,.15);
        border-radius: 18px; padding: 22px 26px;
        margin-bottom: 16px;
        box-shadow: 0 3px 14px rgba(2,62,138,.07);
        transition: box-shadow .2s, border-color .2s;
    }
    .approche-card:hover {
        box-shadow: 0 6px 24px rgba(2,62,138,.12);
        border-color: rgba(0,180,216,.3);
    }
    .approche-card .ac-header {
        display: flex; align-items: center; gap: 12px;
        margin-bottom: 14px;
    }
    .approche-badge {
        background: linear-gradient(135deg, var(--navy), var(--ocean));
        color: #fff; border-radius: 8px; padding: 5px 12px;
        font-size: .65rem; font-weight: 800; letter-spacing: 1.5px;
        text-transform: uppercase; font-family: 'monospace', sans-serif;
    }
    .approche-badge.b { background: linear-gradient(135deg, #0f766e, #14b8a6); }
    .approche-title {
        font-size: .95rem; font-weight: 700; color: var(--navy);
        font-family: 'monospace', sans-serif;
    }

    /* ── Code block ── */
    .code-block {
        background: #0d1117;
        border-radius: 12px; padding: 16px 20px;
        font-family: 'JetBrains Mono', 'Courier New', monospace;
        font-size: .78rem; line-height: 1.7;
        color: #e6edf3; margin: 12px 0;
        border: 1px solid rgba(255,255,255,.08);
        overflow-x: auto;
    }
    .code-block .c-kw  { color: #ff7b72; }
    .code-block .c-str { color: #a5d6ff; }
    .code-block .c-cmt { color: #8b949e; font-style: italic; }
    .code-block .c-num { color: #79c0ff; }
    .code-block .c-fn  { color: #d2a8ff; }
    .code-block .c-var { color: #ffa657; }

    /* ── Algo step ── */
    .algo-step {
        display: flex; gap: 16px; margin-bottom: 18px;
        align-items: flex-start;
    }
    .algo-num {
        min-width: 36px; height: 36px; border-radius: 10px;
        background: linear-gradient(135deg, var(--navy), var(--ocean));
        color: #fff; font-size: .78rem; font-weight: 800;
        display: flex; align-items: center; justify-content: center;
        flex-shrink: 0; font-family: 'monospace', sans-serif;
    }
    .algo-body { flex: 1; }
    .algo-body strong { color: var(--navy); font-weight: 700; }
    .algo-body p { font-size: .85rem; color: var(--text); line-height: 1.85; margin: 0; }

    /* ── Param row ── */
    .param-table { width: 100%; border-collapse: separate; border-spacing: 0 8px; }
    .param-row td { padding: 10px 14px; font-size: .83rem; }
    .param-row td:first-child {
        background: linear-gradient(135deg, #f0f8ff, #e4f3fb);
        border-radius: 10px 0 0 10px;
        font-family: 'JetBrains Mono', monospace; color: var(--navy);
        font-weight: 700; white-space: nowrap;
        border: 1px solid rgba(0,180,216,.12); border-right: none;
    }
    .param-row td:last-child {
        background: #fafcff;
        border-radius: 0 10px 10px 0;
        color: var(--text); line-height: 1.7;
        border: 1px solid rgba(0,180,216,.12); border-left: none;
    }

    /* ── Conclusion box ── */
    .conclusion-box {
        background: linear-gradient(135deg, #f0fdf4, #dcfce7);
        border: 1px solid #86efac;
        border-radius: 18px; padding: 22px 26px;
        margin-top: 16px;
    }
    .conclusion-box .cb-title {
        font-size: .95rem; font-weight: 800; color: #14532d;
        margin-bottom: 12px; font-family: 'monospace', sans-serif;
    }
    .conclusion-box p { font-size: .85rem; color: #166534; line-height: 1.9; margin: 0; }

    /* ── clstr format box ── */
    .clstr-box {
        background: #0d1117; border-radius: 14px;
        padding: 20px 24px; margin: 12px 0;
        border: 1px solid rgba(255,255,255,.08);
    }
    .clstr-line { font-family: 'JetBrains Mono', monospace; font-size: .78rem; line-height: 2; }
    .cl-cluster { color: #79c0ff; font-weight: 700; }
    .cl-rep     { color: #3fb950; font-weight: 600; }
    .cl-member  { color: #e6edf3; }
    .cl-pct     { color: #ffa657; }
    .cl-comment { color: #8b949e; font-style: italic; margin-left: 20px; }

    /* ── Bouton expand ── */
    div[data-testid="stButton"] button[kind="secondary"] {
        background: #f8fafc !important;
        border: 1.5px solid rgba(0,180,216,.25) !important;
        border-radius: 10px !important;
        color: var(--navy) !important;
        font-size: .82rem !important;
        font-weight: 600 !important;
        transition: all .2s !important;
    }
    div[data-testid="stButton"] button[kind="secondary"]:hover {
        background: linear-gradient(135deg, #f0f8ff, #e4f3fb) !important;
        border-color: var(--ocean) !important;
        transform: translateY(-1px) !important;
    }

    /* ── Step selector buttons ── */
    .step-selector div[data-testid="stButton"] button {
        border-radius: 16px !important;
        padding: 16px 12px !important;
        font-weight: 700 !important;
        font-family: 'monospace', sans-serif !important;
        transition: all .25s !important;
        min-height: 80px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
#  Vue d'ensemble pipeline
# ─────────────────────────────────────────────
def _pipeline_overview_block():
    active = st.session_state.pipeline_step

    steps = [
        ("01", "📥", "Parsing JSON\n+ Extraction", "~6 318 séq.", "✅ Complété"),
        ("02", "🔬", "Filtrage\nQualité", "6 313 séq.", "✅ Complété"),
        ("03", "🔑", "Déduplication\nMD5 & CD-HIT 100%", "6 285 séq.", "✅ Complété"),
        (
            "04",
            "🧩",
            "Clustering\nCD-HIT 80% | 90%",
            "1 319 | 1 497 clusters",
            "✅ Complété",
        ),
    ]

    flow_html = ""
    for i, (num, ico, name, cnt, status) in enumerate(steps):
        is_active = "active-step" if active == num else ""
        flow_html += f"""
        <div class="pf-step {is_active}">
            <div class="pf-num">Étape {num}</div>
            <span class="pf-ico">{ico}</span>
            <div class="pf-name">{name.replace(chr(10), '<br>')}</div>
            <div class="pf-cnt">{cnt}</div>
            <span class="pf-status">{status}</span>
        </div>
        """
        if i < len(steps) - 1:
            flow_html += '<div class="pf-arrow">→</div>'

    st.markdown(
        f"""
    <div class="pipeline-overview pl-wrap">
        <div class="po-eyebrow">Prétraitement des Séquences Protéiques — CARD → ESM-2</div>
        <div class="po-title">Pipeline Extraction &amp; Nettoyage — Dataset propre pour la classification multi-label</div>
        <div class="pipeline-flow">{flow_html}</div>
        <div class="po-hint">Cliquez sur une étape ci-dessous pour afficher son contenu détaillé</div>
    </div>
    """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
#  ÉTAPE 01
# ─────────────────────────────────────────────
def _step_01():
    st.markdown(
        """
    <div class="step-content pl-wrap">
        <div class="step-header">
            <span class="step-num-badge">Étape 01</span>
            <span class="step-title-big">Parsing JSON + Extraction des séquences</span>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class="hbanner">
    Le fichier <strong>card.json</strong> de la base CARD contient l'intégralité des modèles ARG 
    (Antibiotic Resistance Genes). Chaque modèle décrit un gène de résistance avec ses séquences 
    protéiques associées et ses annotations biologiques. Cette étape parcourt l'ensemble des modèles 
    pour en extraire les séquences et construire un dataset structuré.
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🎯 Champs extraits par séquence**")
        fields = {
            "`id`": "Identifiant unique interne",
            "`ARO_id`": "Identifiant ARO (Antibiotic Resistance Ontology)",
            "`ARO_name`": "Nom du gène de résistance",
            "`sequence_id`": "Identifiant de la séquence dans CARD",
            "`sequence`": "Séquence protéique en acides aminés",
            "`protein_accession`": "Accession GenBank / NCBI",
            "`drug_classes`": "Classes d'antibiotiques associées",
        }
        for f, desc in fields.items():
            st.markdown(f"- {f} — *{desc}*")
    with col2:
        st.markdown("**⚙️ Caractéristiques du module**")
        st.markdown(
            """
            - Compatible format **JSON CARD** (téléchargeable depuis card.mcmaster.ca)
            - Exportable en **FASTA** pour les outils bioinformatiques externes
            - Maintien des **annotations essentielles** à chaque séquence
            - Structure prête pour la **prédiction multi-label** (drug_classes = labels)
            - Préparation pour les encodeurs de type **ESM-2**
            """
        )

    st.markdown("**📄 Résultat attendu — Colonnes CSV :**")
    st.code(
        "id | ARO_id | ARO_name | sequence_id | sequence | protein_accession | drug_classes",
        language="text",
    )

    st.markdown(
        '<div class="metrics-row">'
        '<div class="metric-card"><div class="mc-val">~6 318</div><div class="mc-lbl">Séquences extraites</div></div>'
        '<div class="metric-card light"><div class="mc-val">7</div><div class="mc-lbl">Colonnes structurées</div></div>'
        '<div class="metric-card amber"><div class="mc-val">46</div><div class="mc-lbl">Classes d\'antibiotiques</div></div>'
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ÉTAPE 02
# ─────────────────────────────────────────────
def _step_02():
    st.markdown(
        """
    <div class="step-content pl-wrap">
        <div class="step-header">
            <span class="step-num-badge">Étape 02</span>
            <span class="step-title-big">Filtrage qualité des séquences</span>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class="hbanner">
    Les données brutes de CARD contiennent inévitablement des séquences incomplètes, fragmentées 
    ou ambiguës. Ces séquences, si elles sont conservées, <strong>dégradent la qualité des embeddings ESM-2</strong> 
    et introduisent du bruit dans le modèle de classification. Cette étape applique deux filtres indépendants 
    pour garantir l'intégrité du dataset.
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**❌ Filtre 1 — Longueur minimale**")
        st.markdown(
            """
            Suppression de toutes les séquences **< 50 acides aminés**.

            Ces fragments ne représentent pas des gènes fonctionnels complets. Ils génèrent des embeddings 
            non représentatifs et du bruit dans tout encodeur de séquences protéiques.
            """
        )
        st.markdown(
            '<div class="justif-tag">'
            "📚 <strong>Référence :</strong> Seuil standard établi par "
            "<em>DeepARG (Arango-Argoty et al., 2018)</em>, "
            "adopté comme standard dans les benchmarks AMR."
            "</div>",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown("**❌ Filtre 2 — Caractères non standard**")
        st.markdown(
            """
            Suppression des séquences contenant les caractères :

            | Caractère | Signification |
            |---|---|
            | `X` | Acide aminé **indéterminé** (codon ambigu) |
            | `B` | Asp **ou** Asn (ambiguïté) |
            | `Z` | Glu **ou** Gln (ambiguïté) |
            | `U` | Sélénocystéine (rare) |
            | `O` | Pyrrolysine (rare) |
            """
        )
        st.markdown(
            '<div class="justif-tag">'
            "⚙️ <strong>Compatibilité ESM-2 :</strong> Le vocabulaire d'ESM-2 est limité aux "
            "20 acides aminés standards. Tout caractère hors vocabulaire provoque une erreur "
            "d'encodage ou un embedding dégradé."
            "</div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="metrics-row">'
        '<div class="metric-card"><div class="mc-val">6 318</div><div class="mc-lbl">Séquences en entrée</div></div>'
        '<div class="metric-card green"><div class="mc-val">6 313</div><div class="mc-lbl">Séquences conservées</div></div>'
        '<div class="metric-card red"><div class="mc-val">5</div><div class="mc-lbl">Séquences supprimées</div></div>'
        '<div class="metric-card light"><div class="mc-val">50 aa</div><div class="mc-lbl">Seuil minimum</div></div>'
        "</div>",
        unsafe_allow_html=True,
    )

    # Bouton analyse séquences X
    btn_x = (
        "🔼 Masquer l'analyse"
        if st.session_state.show_x_analysis
        else "🔍 Voir le détail — Pourquoi ces 5 séquences ont été supprimées ?"
    )
    if st.button(btn_x, key="btn_x_analysis", type="secondary"):
        st.session_state.show_x_analysis = not st.session_state.show_x_analysis
        st.rerun()

    if st.session_state.show_x_analysis:
        st.markdown("---")
        st.markdown("#### 🔬 Analyse des 5 séquences supprimées — Caractères X")
        st.markdown(
            """
            <div class="hbanner">
            Ces 5 séquences sont <strong>biologiquement réelles et validées dans NCBI</strong>. 
            Le caractère X ne provient pas d'une erreur du pipeline — c'est une <strong>limite du séquençage original</strong> : 
            certaines bases de l'ADN étaient ambiguës lors du séquençage, rendant la traduction impossible pour ces codons. 
            Leur suppression est biologiquement justifiée pour ESM-2.
            </div>
            """,
            unsafe_allow_html=True,
        )

        sequences = [
            {
                "acc": "AIA08936.1",
                "gene": "rphA",
                "org": "Streptomyces sp. WAC4747",
                "seq": "...GEIDIT<span style='color:#ef4444;font-weight:700;'>X</span>PPVRERPS...",
                "nb_x": 1,
                "cause": "N dans l'ADN (ATCACG<strong>N</strong>GGCCC) — N = base indéterminée (A, T, C ou G). Le codon NGG ne peut pas être traduit avec certitude → X",
                "bio": "Ribonucléase PH réelle isolée de <em>Streptomyces sp.</em> WAC4747, bactérie du sol productrice d'antibiotiques.",
                "cultivable": "✅ Oui",
                "ncbi": "✅ Oui — séquence officielle avec X",
            },
            {
                "acc": "ACS83748.1",
                "gene": "tet(43)",
                "org": "uncultured bacterium AOTet43",
                "seq": "...GLVGAMPENRTSLGAALNDTAQEVGTSLGMAVIGTLIAVL<span style='color:#ef4444;font-weight:700;'>X</span>TTTLPNGD<span style='color:#ef4444;font-weight:700;'>X</span>SLDLATS...",
                "nb_x": 2,
                "cause": "Bases S (= C ou G) et Y (= C ou T) ambiguës → deux codons non résolvables → 2 X",
                "bio": "Séquence obtenue par <strong>métagénomique</strong> depuis l'environnement. La bactérie existe mais n'a jamais été cultivée.",
                "cultivable": "❌ Non cultivée (métagénomique)",
                "ncbi": "✅ Oui — 2 X dans la séquence officielle",
            },
            {
                "acc": "AAR96051.1",
                "gene": "otr(C)",
                "org": "Streptomyces rimosus",
                "seq": "...VGLGP<span style='color:#ef4444;font-weight:700;'>X</span>GAA<span style='color:#ef4444;font-weight:700;'>XX</span>RGALP...",
                "nb_x": 3,
                "cause": "N répété dans GGGCCGAN·CGGCGCGGCAAN·AN·AACGT — 3 zones indéterminées → 3 codons non traduits",
                "bio": "<em>Streptomyces rimosus</em> est la bactérie productrice de l'oxytétracycline. otr(C) est un gène de résistance réel et caractérisé.",
                "cultivable": "✅ Oui",
                "ncbi": "✅ Oui — séquençage 2004, jamais resoumis corrigé",
            },
            {
                "acc": "AHF82023.1",
                "gene": "AQU-2",
                "org": "Aeromonas hydrophila",
                "seq": "...AAP<span style='color:#ef4444;font-weight:700;'>X</span>EMGSQRLFNK...",
                "nb_x": 1,
                "cause": "K = G ou T (IUPAC) dans GCGCCGAA<strong>K</strong>GAGATG → codon AAK non résolvable → X",
                "bio": "Beta-lactamase réelle isolée d'<em>Aeromonas hydrophila</em>, pathogène aquatique courant, publiée en 2014.",
                "cultivable": "✅ Oui",
                "ncbi": "✅ Oui — séquence officielle telle que soumise",
            },
            {
                "acc": "AHF82024.1",
                "gene": "AQU-3",
                "org": "Aeromonas dhakensis",
                "seq": "...GAYVAFV<span style='color:#ef4444;font-weight:700;'>X</span>AKGVGI...",
                "nb_x": 1,
                "cause": "M = A ou C (IUPAC) dans GCGCCTTCGTGC<strong>M</strong>GGCC → codon non résolvable → X",
                "bio": "Paralogue d'AQU-2, publiée dans le même article 2014. <em>Aeromonas dhakensis</em> est un pathogène émergent.",
                "cultivable": "✅ Oui",
                "ncbi": "✅ Oui — même origine que AQU-2",
            },
        ]

        for s in sequences:
            st.markdown(
                f"""
            <div class="x-seq-card">
                <div class="xsc-header">🔑 {s['acc']} — {s['gene']} &nbsp;|&nbsp; <em>{s['org']}</em> &nbsp;|&nbsp; {s['nb_x']} × X</div>
                <div class="xsc-seq">{s['seq']}</div>
                <div class="xsc-row">
                    <strong>Cause ADN :</strong> {s['cause']}<br>
                    <strong>Contexte biologique :</strong> {s['bio']}<br>
                    <strong>Cultivable :</strong> {s['cultivable']} &nbsp;|&nbsp;
                    <strong>Présent dans NCBI :</strong> {s['ncbi']}
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        import pandas as pd

        df = pd.DataFrame(
            {
                "Accession": [
                    "AIA08936.1",
                    "ACS83748.1",
                    "AAR96051.1",
                    "AHF82023.1",
                    "AHF82024.1",
                ],
                "Gène": ["rphA", "tet(43)", "otr(C)", "AQU-2", "AQU-3"],
                "Organisme": [
                    "Streptomyces sp.",
                    "uncultured bacterium",
                    "S. rimosus",
                    "A. hydrophila",
                    "A. dhakensis",
                ],
                "Nb X": [1, 2, 3, 1, 1],
                "Cause ADN": ["N", "S, Y", "N répété", "K", "M"],
                "Cultivable": ["Oui", "Non", "Oui", "Oui", "Oui"],
                "X dans NCBI": ["✓", "✓", "✓", "✓", "✓"],
            }
        )
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.success(
            "**✅ Conclusion — Décision validée :** Toutes ces séquences sont biologiquement réelles et documentées dans NCBI avec leurs caractères X. "
            "Leur suppression est la **décision correcte et justifiée** : ESM-2 ne tolère pas les acides aminés ambigus, "
            "et ces 5 séquences auraient provoqué des erreurs d'encodage ou des vecteurs d'embedding non fiables."
        )

    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ÉTAPE 03
# ─────────────────────────────────────────────
def _step_03():
    st.markdown(
        """
    <div class="step-content pl-wrap">
        <div class="step-header">
            <span class="step-num-badge">Étape 03</span>
            <span class="step-title-big">Déduplication exacte — MD5 &amp; CD-HIT 100%</span>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class="hbanner">
    La base CARD référence fréquemment <strong>une même séquence protéique plusieurs fois</strong> 
    avec des annotations différentes : soit parce qu'une protéine confère une résistance à 
    <em>plusieurs antibiotiques</em> (plusieurs ARO distincts), soit parce qu'elle a été annotée 
    indépendamment dans différentes souches. Cette étape supprime ces redondances <strong>exactes</strong> 
    avant l'encodage par ESM-2 — encoder deux fois la même séquence serait un gaspillage de ressources 
    computationnelles et introduirait des doublons dans le dataset d'entraînement.
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="metrics-row">'
        '<div class="metric-card"><div class="mc-val">6 313</div><div class="mc-lbl">Séquences en entrée</div></div>'
        '<div class="metric-card green"><div class="mc-val">6 285</div><div class="mc-lbl">Séquences conservées</div></div>'
        '<div class="metric-card red"><div class="mc-val">28</div><div class="mc-lbl">Doublons supprimés</div></div>'
        '<div class="metric-card light"><div class="mc-val">0.4%</div><div class="mc-lbl">Taux de réduction</div></div>'
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div style="background:linear-gradient(135deg,#fff8e1,#fef3c7);border:1px solid #fcd34d;border-radius:14px;padding:16px 20px;margin-bottom:16px;font-size:.85rem;color:#78350f;line-height:1.85;">
    ⚠️ <strong>Deux approches indépendantes</strong> ont été testées sur ce dataset. 
    Elles produisent des résultats <strong>identiques</strong> (6 285 séquences conservées, 28 doublons supprimés), 
    ce qui valide la robustesse de la déduplication. Les différences de conception sont expliquées ci-dessous.
    </div>
    """,
        unsafe_allow_html=True,
    )

    # ── APPROCHE A : MD5
    st.markdown(
        '<div class="subsection-title">🔑 Approche A — Déduplication par hachage MD5</div>',
        unsafe_allow_html=True,
    )

    btn_md5 = (
        "🔼 Masquer la définition MD5"
        if st.session_state.show_md5_detail
        else "📖 Comprendre MD5 — Principe et fonctionnement ▼"
    )
    if st.button(btn_md5, key="btn_md5_def", type="secondary"):
        st.session_state.show_md5_detail = not st.session_state.show_md5_detail
        st.rerun()

    if st.session_state.show_md5_detail:
        st.markdown(
            """
        <div class="def-box">
            <div class="def-title">🔑 MD5 — Message Digest Algorithm 5</div>
            <p>
                MD5 est une <strong>fonction de hachage cryptographique</strong> qui transforme n'importe quelle 
                chaîne de caractères en une empreinte numérique fixe de <strong>128 bits (32 caractères hexadécimaux)</strong>.<br><br>
                <strong>Propriété fondamentale :</strong> Deux chaînes rigoureusement identiques produisent 
                <em>toujours</em> le même hash. Deux chaînes différentes (même d'un seul caractère) 
                produisent des hashs complètement différents.<br><br>
                <strong>Exemple :</strong><br>
                <code>MD5("MTKIIFVGAAA") = "a3f8c1e7..."</code><br>
                <code>MD5("MTKIIFVGAAB") = "d92f14aa..."</code> ← même 1 caractère différent → hash totalement différent<br><br>
                <strong>Dans ce pipeline :</strong> chaque séquence est normalisée (mise en majuscules, 
                suppression des espaces) puis hachée avec MD5. 
                La première occurrence d'un hash est conservée, les suivantes sont supprimées comme doublons.<br><br>
                <strong>Avantage computationnel :</strong> Complexité <strong>O(n)</strong> — une seule passe 
                sur toutes les séquences, sans comparaison pairwise. Nettement plus rapide que CD-HIT 
                pour la déduplication <em>exacte</em>, et complémentaire à lui pour la déduplication <em>approchée</em>.
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Analyse des 28 suppressions
    st.markdown("**📋 Analyse des 28 suppressions MD5 :**")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
        <div class="approche-card">
            <div class="ac-header">
                <span class="approche-badge">Cas 1 — Majoritaire</span>
            </div>
            <strong>Même séquence, ARO différents</strong><br><br>
            La même protéine (<code>NP_218312.1</code>, <code>NP_218371.1</code>, <code>NP_215774.1</code>) 
            est référencée plusieurs fois dans CARD car elle confère une résistance à 
            <em>plusieurs antibiotiques</em>. CARD lui associe un ARO distinct pour chaque résistance, 
            mais la séquence protéique est rigoureusement identique. MD5 détecte et supprime ces doublons.
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
        <div class="approche-card">
            <div class="ac-header">
                <span class="approche-badge b">Cas 2 — Minoritaire</span>
            </div>
            <strong>Accessions différentes, séquence identique</strong><br><br>
            Protéines annotées indépendamment dans différentes souches bactériennes.<br><br>
            Ex : <code>AAN43827.1</code> / <code>AAC75291.1</code> — deux accessions pour 
            le même gène <em>gyrA</em> dans <em>Shigella flexneri</em> et <em>E. coli</em>. 
            Séquence protéique rigoureusement identique. MD5 les détecte également.
        </div>
        """,
            unsafe_allow_html=True,
        )

    # ── APPROCHE B : CD-HIT 100%
    st.markdown(
        '<div class="subsection-title">🧩 Approche B — Déduplication CD-HIT à 100% d\'identité</div>',
        unsafe_allow_html=True,
    )

    btn_cd = (
        "🔼 Masquer la définition CD-HIT"
        if st.session_state.show_cdhit_detail
        else "📖 Comprendre CD-HIT — Principe et fonctionnement ▼"
    )
    if st.button(btn_cd, key="btn_cdhit_def_03", type="secondary"):
        st.session_state.show_cdhit_detail = not st.session_state.show_cdhit_detail
        st.rerun()

    if st.session_state.show_cdhit_detail:
        st.markdown(
            """
        <div class="def-box">
            <div class="def-title">🧩 CD-HIT — Cluster Database at High Identity with Tolerance</div>
            <p>
                CD-HIT est un programme de <strong>clustering de séquences biologiques</strong> par similarité.
                Il regroupe les séquences partageant un pourcentage d'identité ≥ au seuil défini 
                (paramètre <code>-c</code>). Pour chaque cluster, la séquence la plus longue est 
                désignée <em>représentante</em> et conservée.<br><br>
                <strong>À 100% d'identité (<code>-c 1.0</code>) :</strong> seules les séquences 
                rigoureusement identiques sont regroupées. Le paramètre <code>-aS 1.0</code> impose 
                une couverture totale de la séquence la plus courte, détectant également les cas de 
                <em>containment exact</em> (séquence A entièrement contenue dans B).<br><br>
                <strong>Résultat sur ce dataset :</strong> 6 285 clusters formés — chaque cluster 
                contient exactement 1 représentant conservé. <strong>Aucun cas de containment strict 
                (A ⊂ B) n'a été détecté</strong> dans ce dataset.
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
    <div class="approche-card">
        <div class="ac-header">
            <span class="approche-badge b">CD-HIT à 100%</span>
            <span class="approche-title">Résultats détaillés</span>
        </div>
        <ul style="font-size:.85rem;color:var(--text);line-height:2;margin:0;padding-left:20px;">
            <li>Les 28 séquences supprimées correspondent toutes à des <strong>duplications exactes</strong> de séquences</li>
            <li>Elles appartiennent à des clusters CD-HIT de taille > 1 (identité = 100%)</li>
            <li><strong>Aucun cas de containment strict</strong> (A ⊂ B avec A ≠ B) n'a été détecté dans ce dataset</li>
            <li>CD-HIT a formé <strong>6 285 clusters</strong> — chaque cluster contient exactement 1 représentant conservé</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # ── Comparaison MD5 vs CD-HIT
    btn_comp = (
        "🔼 Masquer la comparaison"
        if st.session_state.show_md5_vs_cdhit
        else "⚖️ Comparaison détaillée MD5 vs CD-HIT ▼"
    )
    if st.button(btn_comp, key="btn_md5_vs_cdhit", type="secondary"):
        st.session_state.show_md5_vs_cdhit = not st.session_state.show_md5_vs_cdhit
        st.rerun()

    if st.session_state.show_md5_vs_cdhit:
        st.markdown("---")
        st.markdown(
            "**Les deux approches donnent les mêmes résultats sur ce dataset :**"
        )
        import pandas as pd

        df_comp = pd.DataFrame(
            {
                "Critère": [
                    "Séquences identiques (string exact)",
                    "Même accession + ARO différents",
                    "Accessions différentes, séquence identique",
                    "Sous-séquence (A ⊂ B)",
                    "Complexité algorithmique",
                    "Dépendances externes",
                    "Gestion des annotations multiples",
                ],
                "MD5": [
                    "✅ Détecté",
                    "✅ Détecté",
                    "✅ Détecté",
                    "❌ Non détecté",
                    "O(n) — très rapide",
                    "Aucune (Python stdlib)",
                    "✅ Union explicite des drug classes",
                ],
                "CD-HIT 100%": [
                    "✅ Détecté",
                    "✅ Détecté",
                    "✅ Détecté",
                    "❌ Non observé ici",
                    "O(n log n)",
                    "CD-HIT installé",
                    "⚠️ Représentant unique (annotation principale)",
                ],
            }
        )
        st.dataframe(df_comp, use_container_width=True, hide_index=True)

        st.markdown(
            """
        <div class="hbanner">
        <strong>Pourquoi les deux approches donnent le même résultat ?</strong><br>
        La différence observée s'explique par des aspects liés à la gestion des entrées et des annotations 
        dans le pipeline, plutôt que par une différence réelle de capacité de déduplication. 
        MD5 opère directement sur la chaîne de caractères brute, indépendamment de l'accession ou de toute 
        annotation. CD-HIT traite les séquences au niveau FASTA et regroupe les entrées strictement identiques. 
        Dans ce dataset CARD, les deux cas de duplication observés (ARO multiples et accessions différentes) 
        sont détectés de façon identique par les deux méthodes.
        </div>
        """,
            unsafe_allow_html=True,
        )

    # ── Stratégie Union
    st.markdown("---")
    st.markdown(
        '<div class="subsection-title">🔗 Stratégie d\'annotation — Union des drug classes</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    Après déduplication, une même protéine peut avoir été annotée avec **plusieurs drug classes différentes** 
    selon les occurrences supprimées. La question est : quelles drug classes attribuer au représentant conservé ?
    """
    )

    btn_union = (
        "🔼 Masquer"
        if st.session_state.show_union_detail
        else "📖 Voir la stratégie Union expliquée ▼"
    )
    if st.button(btn_union, key="btn_union", type="secondary"):
        st.session_state.show_union_detail = not st.session_state.show_union_detail
        st.rerun()

    if st.session_state.show_union_detail:
        st.markdown(
            """
        <div class="union-box">
            <div class="ub-title">✅ Stratégie retenue : Union des classes</div>
            <p>
                Le pipeline agrège <strong>l'ensemble des drug classes</strong> présentes dans toutes 
                les occurrences d'une même séquence et les attribue au représentant conservé.
            </p>
            <p>
                <strong>Justification biologique :</strong> Les duplications détectées correspondent 
                à des séquences <em>strictement identiques</em>. Les différences d'annotation 
                proviennent de la multiplicité des ARO dans CARD ou d'annotations issues de sources 
                biologiques différentes. Or, une même protéine peut réellement conférer une 
                <strong>résistance multi-classe</strong>. À 100% d'identité, il s'agit du même 
                produit protéique — toutes ses fonctions biologiques connues doivent être conservées.
            </p>
            <p>
                <strong>Traçabilité :</strong> Une colonne <code>classes_added_by_union</code> est 
                ajoutée au dataset pour identifier les classes ajoutées par union, permettant 
                une vérification manuelle si nécessaire.
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        import pandas as pd

        df_strat = pd.DataFrame(
            {
                "Critère": [
                    "Complétude des labels",
                    "Apprentissage multi-label",
                    "Validité biologique",
                    "Traçabilité",
                ],
                "Représentant seul": [
                    "⚠️ Risque de perte d'info",
                    "⚠️ Sous-étiquetage possible",
                    "❌ Limitée",
                    "✅ Simple",
                ],
                "Union (choisie ✅)": [
                    "✅ Toutes les classes conservées",
                    "✅ Tous les labels transmis",
                    "✅ Biologiquement cohérente",
                    "✅ Via classes_added_by_union",
                ],
            }
        )
        st.dataframe(df_strat, use_container_width=True, hide_index=True)

    # ── Conclusion étape 03
    btn_conc = (
        "🔼 Masquer"
        if st.session_state.show_dedup_conclusion
        else "📋 Conclusion de l'étape 03 ▼"
    )
    if st.button(btn_conc, key="btn_dedup_conc", type="secondary"):
        st.session_state.show_dedup_conclusion = (
            not st.session_state.show_dedup_conclusion
        )
        st.rerun()

    if st.session_state.show_dedup_conclusion:
        st.markdown(
            """
        <div class="conclusion-box">
            <div class="cb-title">✅ Conclusion — Étape 03 validée</div>
            <p>
                Dans CARD, une même séquence protéique peut apparaître plusieurs fois avec des annotations 
                différentes, notamment lorsqu'elle est associée à plusieurs ARO ou plusieurs classes de résistance.<br><br>
                Les deux approches testées <strong>(MD5 et CD-HIT 100%)</strong> produisent des résultats 
                <strong>identiques</strong> sur ce dataset :<br>
                → <strong>6 285 séquences uniques</strong> conservées après suppression de <strong>28 doublons exacts</strong><br>
                → La stratégie <strong>Union</strong> garantit qu'aucune drug class n'est perdue lors de la fusion<br>
                → Le dataset est maintenant prêt pour le clustering CD-HIT (étape 04) et l'encodage ESM-2
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ÉTAPE 04
# ─────────────────────────────────────────────
def _step_04():
    st.markdown(
        """
    <div class="step-content pl-wrap">
        <div class="step-header">
            <span class="step-num-badge">Étape 04</span>
            <span class="step-title-big">Clustering CD-HIT — Prévention du Data Leakage</span>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class="hbanner">
    L'étape 03 a éliminé les doublons <em>exacts</em>. Mais il reste des séquences 
    <strong>très similaires</strong> (80–90% d'identité) qui représentent des variants proches 
    du même gène de résistance. Si ces séquences similaires se retrouvent dans des splits 
    train/test différents, le modèle <strong>mémorise au lieu d'apprendre</strong> — 
    c'est ce qu'on appelle le <em>data leakage</em>. Cette étape applique CD-HIT avec 
    deux seuils (80% et 90%) pour regrouper ces séquences et assurer une partition propre du dataset.
    </div>
    """,
        unsafe_allow_html=True,
    )

    # ── Data Leakage
    st.markdown(
        '<div class="subsection-title">⚠️ Data Leakage — Fuite d\'information</div>',
        unsafe_allow_html=True,
    )

    btn_leak = (
        "🔼 Masquer l'explication"
        if st.session_state.show_data_leakage
        else "📖 Comprendre le data leakage — avec exemple concret ▼"
    )
    if st.button(btn_leak, key="btn_leakage", type="secondary"):
        st.session_state.show_data_leakage = not st.session_state.show_data_leakage
        st.rerun()

    if st.session_state.show_data_leakage:
        st.markdown(
            """
        <div class="leakage-box">
            <div class="lb-title">⚠️ Data Leakage — Fuite d'information entre train et test</div>
            <p>
                Le <strong>data leakage</strong> survient quand des informations du jeu de test 
                "fuient" dans le jeu d'entraînement — ou quand les deux sets contiennent des données 
                trop similaires. Le modèle obtient alors des performances <em>artificiellement élevées</em> 
                qui ne reflètent pas sa capacité réelle de généralisation.
            </p>
            <p>
                <strong>Dans le contexte des séquences protéiques :</strong> si deux séquences 
                partageant 95% d'identité se retrouvent l'une dans le train set et l'autre dans 
                le test set, le modèle a déjà "vu" une protéine presque identique pendant 
                l'entraînement — la prédiction devient triviale.
            </p>
            <div class="leakage-example">
                <strong>🔬 Exemple concret — Famille TEM (beta-lactamases) :</strong><br><br>
                Supposons deux variants du gène <em>TEM-1</em> (beta-lactamase) :<br>
                — <code>TEM-1a</code> : séquence de 286 aa → <strong>Train set</strong><br>
                — <code>TEM-1b</code> : séquence de 286 aa, 95% identique à TEM-1a → <strong>Test set</strong><br><br>
                Le modèle ESM-2, ayant encodé TEM-1a pendant l'entraînement, va générer un embedding 
                presque identique pour TEM-1b au test. Il <strong>mémorise la famille</strong> 
                au lieu d'apprendre les caractéristiques généralisables de la résistance aux beta-lactamines.<br><br>
                <strong>Conséquence :</strong> F1-score et AUC-ROC artificiellement élevés → 
                le modèle semblera performant mais échouera sur de nouvelles séquences jamais vues.
            </div>
            <p style="margin-top:14px;">
                <strong>Solution :</strong> Toutes les séquences d'un même cluster CD-HIT doivent 
                rester dans le <em>même split</em>. Le split train/test se fait au niveau des 
                <strong>clusters</strong> et non des séquences individuelles.
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # ── L'algorithme CD-HIT en détail
    st.markdown(
        '<div class="subsection-title">⚙️ L\'algorithme CD-HIT — Fonctionnement pas à pas</div>',
        unsafe_allow_html=True,
    )

    btn_algo = (
        "🔼 Masquer l'algorithme"
        if st.session_state.show_cdhit_algo
        else "🔍 Voir le fonctionnement interne de CD-HIT ▼"
    )
    if st.button(btn_algo, key="btn_cdhit_algo", type="secondary"):
        st.session_state.show_cdhit_algo = not st.session_state.show_cdhit_algo
        st.rerun()

    if st.session_state.show_cdhit_algo:
        st.markdown(
            """
        <div class="def-box">
            <div class="def-title">🧩 CD-HIT — Fonctionnement interne en 5 étapes</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        algo_steps = [
            (
                "1",
                "Tri par longueur décroissante",
                """CD-HIT trie d'abord toutes les séquences de la plus longue à la plus courte. 
                Ce tri est fondamental : <strong>la séquence la plus longue devient toujours représentante</strong> car elle est 
                traitée en premier et n'a aucune représentante existante à rejoindre.
                <br><br>
                <code style="background:#f0f8ff;padding:4px 8px;border-radius:6px;font-size:.78rem;">
                seq_A : 520 aa  ← traitée en 1er → représentante automatique<br>
                seq_B : 412 aa<br>
                seq_D : 395 aa<br>
                seq_C : 280 aa
                </code>""",
            ),
            (
                "2",
                "Filtre par k-mers (mots courts)",
                """Avant tout alignement coûteux, CD-HIT applique un filtre rapide basé sur les k-mers. 
                Avec <code>-n 5</code>, il utilise des <strong>pentamères</strong> (mots de 5 acides aminés).<br><br>
                <strong>Théorème des k-mers :</strong> si deux séquences ont une identité ≥ 90%, 
                elles partagent nécessairement un nombre minimum de k-mers communs. Si ce nombre est inférieur 
                au seuil théorique, l'alignement complet est inutile — les séquences sont forcément < 90% identiques.<br><br>
                Ce filtre élimine la grande majorité des comparaisons inutiles, rendant CD-HIT 
                <strong>O(n) en pratique</strong> malgré un problème théoriquement O(n²).
                """,
            ),
            (
                "3",
                "Alignement Smith-Waterman (local)",
                """Pour les paires ayant passé le filtre k-mers, CD-HIT calcule l'identité de séquence :<br><br>
                <code style="background:#f0f8ff;padding:4px 8px;border-radius:6px;font-size:.78rem;">
                identité = nb_positions_identiques / longueur_séquence_courte
                </code><br><br>
                Si identité ≥ seuil (-c) → la séquence rejoint le cluster de la représentante.<br>
                Sinon → elle devient une nouvelle représentante (nouveau cluster).
                """,
            ),
            (
                "4",
                "Construction des clusters",
                """À la fin, chaque séquence appartient à exactement un cluster. 
                Le <strong>représentant</strong> (marqué <code>*</code> dans le fichier .clstr) est la séquence 
                conservée pour l'entraînement. Les autres membres sont des variants trop similaires qui seraient 
                source de data leakage s'ils étaient dans un split différent.<br><br>
                <code style="background:#f0f8ff;padding:4px 8px;border-radius:6px;font-size:.78rem;">
                Cluster 0 : seq_A (520 aa) ★  ← représentante<br>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;seq_D (395 aa) ← 93% avec A<br>
                Cluster 1 : seq_B (412 aa) ★  ← représentante<br>
                Cluster 2 : seq_C (280 aa) ★  ← séquence unique
                </code>""",
            ),
            (
                "5",
                "Assignation au cluster le plus similaire (mode -g 1)",
                """Avec le paramètre <code>-g 1</code>, CD-HIT utilise le mode <strong>précis</strong> : 
                chaque séquence est assignée au cluster dont le représentant est le <em>plus similaire</em> 
                (et non simplement le premier trouvé). Ce mode est plus lent mais produit des clusters 
                biologiquement plus cohérents. C'est le mode recommandé pour les analyses AMR.
                """,
            ),
        ]

        for num, title, body in algo_steps:
            st.markdown(
                f"""
            <div class="algo-step">
                <div class="algo-num">{num}</div>
                <div class="algo-body">
                    <strong>{title}</strong>
                    <p style="margin-top:8px;">{body}</p>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    # ── Paramètres d'exécution
    st.markdown(
        '<div class="subsection-title">⚙️ Paramètres d\'exécution CD-HIT</div>',
        unsafe_allow_html=True,
    )

    btn_params = (
        "🔼 Masquer les paramètres"
        if st.session_state.show_cdhit_params
        else "⚙️ Voir l'explication détaillée de chaque paramètre ▼"
    )
    if st.button(btn_params, key="btn_cdhit_params", type="secondary"):
        st.session_state.show_cdhit_params = not st.session_state.show_cdhit_params
        st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
**Communs aux deux seuils :**
- `-g 1` — mode précis : chaque séquence est assignée au cluster **le plus similaire**
- Mémoire : `4 000 MB`
- Threads : `4`
- `-d 0` — accession complète dans le fichier `.clstr`
        """
        )
    with col2:
        st.markdown(
            """
**Spécifique par seuil :**
- Seuil 80% → `-c 0.8 -n 4`
- Seuil 90% → `-c 0.9 -n 5`

Le **word size** (-n) est un pré-filtre basé sur des k-mers.
CD-HIT recommande n=5 pour ≥ 90% et n=4 pour 80–90%.
        """
        )

    if st.session_state.show_cdhit_params:
        st.markdown(
            """
        <table class="param-table">
            <tr class="param-row">
                <td>-c 0.90 / 0.80</td>
                <td><strong>Seuil d'identité central.</strong> Deux séquences partageant ≥ 90% de leurs acides aminés aux mêmes positions seront dans le même cluster. 
                À 90%, c'est le standard AMR pour prévenir le data leakage tout en préservant la diversité biologique.</td>
            </tr>
            <tr class="param-row">
                <td>-n 5 / 4</td>
                <td><strong>Taille des k-mers (word size).</strong> Règle établie empiriquement : -n 5 obligatoire pour -c ≥ 0.90, -n 4 pour 0.80–0.90. 
                Déroger à cette règle produit des clusters incorrects car le filtre k-mers serait mal calibré.</td>
            </tr>
            <tr class="param-row">
                <td>-g 1</td>
                <td><strong>Mode précis.</strong> Chaque séquence est assignée au cluster le plus similaire (pas seulement le premier trouvé). 
                Plus lent mais biologiquement correct — recommandé pour les analyses de résistance aux antibiotiques.</td>
            </tr>
            <tr class="param-row">
                <td>-M 4000</td>
                <td><strong>Mémoire allouée (MB).</strong> Pour 6 285 séquences de ~400 aa, la mémoire nécessaire est ≈ 5 MB. 
                4 000 MB est très largement suffisant et garantit qu'aucune séquence ne sera ignorée par manque de RAM.</td>
            </tr>
            <tr class="param-row">
                <td>-T 4</td>
                <td><strong>Threads (parallélisation).</strong> CD-HIT parallélise la phase de comparaison. 
                4 threads divisent le temps de calcul par ~4. -T 0 utilise automatiquement tous les cœurs disponibles.</td>
            </tr>
            <tr class="param-row">
                <td>-d 0</td>
                <td><strong>Longueur des descriptions dans .clstr.</strong> Par défaut, CD-HIT tronque les noms à 20 caractères. 
                -d 0 désactive toute troncature, garantissant les accessions complètes pour le parsing (ex : AHF82023.1 → non tronquée).</td>
            </tr>
        </table>
        """,
            unsafe_allow_html=True,
        )

    # ── Format du fichier .clstr
    st.markdown(
        '<div class="subsection-title">📄 Format du fichier de sortie .clstr</div>',
        unsafe_allow_html=True,
    )

    btn_clstr = (
        "🔼 Masquer"
        if st.session_state.show_clstr_format
        else "📄 Voir le format .clstr et son parsing ▼"
    )
    if st.button(btn_clstr, key="btn_clstr_format", type="secondary"):
        st.session_state.show_clstr_format = not st.session_state.show_clstr_format
        st.rerun()

    if st.session_state.show_clstr_format:
        st.markdown(
            """
        <div class="clstr-box">
            <div class="clstr-line"><span class="cl-cluster">&gt;Cluster 0</span><span class="cl-comment">← début du cluster 0</span></div>
            <div class="clstr-line"><span class="cl-rep">0   520aa, &gt;AIA08936.1... *</span><span class="cl-comment">← représentant (*), 520 aa</span></div>
            <div class="clstr-line"><span class="cl-member">1   412aa, &gt;AHF82023.1... </span><span class="cl-pct">at 93%</span><span class="cl-comment">← membre, 93% avec représentant</span></div>
            <div class="clstr-line"><span class="cl-member">2   401aa, &gt;AHF82024.1... </span><span class="cl-pct">at 91%</span><span class="cl-comment">← membre, 91% avec représentant</span></div>
            <div style="height:8px;"></div>
            <div class="clstr-line"><span class="cl-cluster">&gt;Cluster 1</span></div>
            <div class="clstr-line"><span class="cl-rep">0   395aa, &gt;ACS83748.1... *</span><span class="cl-comment">← représentant du cluster 1</span></div>
            <div class="clstr-line"><span class="cl-member">1   388aa, &gt;AAR96051.1... </span><span class="cl-pct">at 94%</span></div>
            <div style="height:8px;"></div>
            <div class="clstr-line"><span class="cl-cluster">&gt;Cluster 2</span></div>
            <div class="clstr-line"><span class="cl-rep">0   280aa, &gt;XXXX.1... *</span><span class="cl-comment">← séquence unique, cluster de taille 1</span></div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown("**Parsing Python du fichier .clstr :**")
        st.code(
            """def parse_cdhit_clusters(clstr_path: Path) -> set[str]:
    representatives = set()
    with open(clstr_path, "r", encoding="utf-8") as fh:
        for line in fh:
            if line.startswith(">"):
                # ">Cluster 0" → début d'un nouveau cluster → ignorer
                continue
            if "*" in line:
                # Ligne représentante : "0    520aa, >AIA08936.1... *"
                parts = line.split(">")
                # parts[1] = "AIA08936.1... *"
                acc = parts[1].split("...")[0].strip()
                representatives.add(acc)
    return representatives""",
            language="python",
        )

    # ── Résultats
    st.markdown(
        '<div class="subsection-title">📊 Résultats comparatifs 80% vs 90%</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="metrics-row">'
        '<div class="metric-card"><div class="mc-val">1 319</div><div class="mc-lbl">Clusters à 80%</div></div>'
        '<div class="metric-card green"><div class="mc-val">1 497</div><div class="mc-lbl">Clusters à 90% ✅</div></div>'
        '<div class="metric-card light"><div class="mc-val">+178</div><div class="mc-lbl">Séquences de différence</div></div>'
        '<div class="metric-card amber"><div class="mc-val">76.2%</div><div class="mc-lbl">Réduction à 90%</div></div>'
        "</div>",
        unsafe_allow_html=True,
    )

    import pandas as pd

    df_clust = pd.DataFrame(
        {
            "Métrique": [
                "Séquences en entrée",
                "Clusters formés",
                "Représentants conservés",
                "Séquences supprimées",
                "Taux de réduction",
                "Word size (-n)",
            ],
            "Seuil 80%": ["6 285", "1 319", "1 319", "4 966", "79.0 %", "4"],
            "Seuil 90% ✅": ["6 285", "1 497", "1 497", "4 788", "76.2 %", "5"],
            "Différence": ["—", "+178", "+178", "−178", "−2.8 pts", "—"],
        }
    )
    st.dataframe(df_clust, use_container_width=True, hide_index=True)

    st.markdown(
        """
    **Interprétation des 178 séquences de différence :**
    - À **80%** → elles sont absorbées dans des clusters existants (clustering plus agressif)
    - À **90%** → elles sont suffisamment différentes pour former leur **propre cluster** (plus de diversité conservée)
    - Ces 178 séquences seront testées : apportent-elles de l'information ou du bruit ?
    """
    )

    # ── Recommandations
    st.markdown(
        '<div class="subsection-title">🎯 Choix du seuil et recommandations</div>',
        unsafe_allow_html=True,
    )
    tab1, tab2, tab3 = st.tabs(
        [
            "✅ 90% — Dataset final",
            "🔍 80% — Analyse de robustesse",
            "⚠️ Règle split Train/Test",
        ]
    )

    with tab1:
        st.markdown(
            """
        <div class="result-highlight">
            <div class="rh-title">Dataset Final Recommandé</div>
            <div class="rh-val">1 497 séquences — Seuil 90%</div>
            <div class="rh-desc">
                Standard dans la littérature AMR · Conserve la diversité biologique · 
                Élimine les redondances évidentes · Adapté à l'encodage ESM-2
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
Le seuil **90%** est le standard établi dans les benchmarks AMR pour deux raisons :
1. **Diversité biologique préservée** : deux séquences à 89% d'identité peuvent avoir des profils de résistance différents
2. **Réduction suffisante** : 76.2% de réduction élimine les variants quasi-identiques sans sur-agréger
        """
        )
    with tab2:
        st.info(
            """
**Le seuil 80% sera utilisé pour une analyse de robustesse :**

- Tester si les **178 séquences supplémentaires** apportent de l'information ou du bruit
- Comparer les deux modèles entraînés (80% vs 90%) via **F1-score** et **AUC-ROC**
- Si performances similaires → les 178 séquences sont redondantes pour le modèle
- Si performances différentes → les 178 séquences capturent de la **diversité biologique réelle**
        """
        )
    with tab3:
        st.error(
            """
**Règle critique — prévention absolue du data leakage :**

Toutes les séquences d'un même cluster **doivent rester dans le même split**.

Le split train/test se fait **au niveau des clusters**, pas des séquences individuelles.

**Exemple correct :**
- Cluster C42 contient 5 variants TEM → toutes les 5 dans le train **ou** toutes dans le test
- Jamais 3 dans train et 2 dans test

**Conséquence si violée :** fuite d'information → F1-score artificiellement élevé → modèle qui mémorise.
        """
        )

    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Tableau état final
# ─────────────────────────────────────────────
def _pipeline_state_table():
    st.markdown("### 📁 État du pipeline — Récapitulatif complet")
    import pandas as pd

    df = pd.DataFrame(
        {
            "Étape": ["01", "02", "03", "04a", "04b", "05"],
            "Module": [
                "Extraction JSON",
                "Filtrage qualité",
                "Déduplication MD5 + CD-HIT 100%",
                "Clustering CD-HIT 80%",
                "Clustering CD-HIT 90%",
                "ESM-2 + entraînement",
            ],
            "Séquences": [
                "~6 318",
                "6 313",
                "6 285",
                "1 319 clusters",
                "1 497 clusters ✅",
                "—",
            ],
            "Fichier": [
                "sequences_extracted.csv",
                "sequences_clean.csv",
                "step03_md5/sequences_dedup_md5.csv",
                "threshold_80/sequences_clustered_80.csv",
                "threshold_90/sequences_clustered_90.csv",
                "(phase suivante)",
            ],
            "Statut": ["✅", "✅", "✅", "✅", "✅", "⏳"],
        }
    )
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown(
        """
    <div class="hbanner">
    ✅ <strong>Pipeline de prétraitement complété — Étapes 01 à 04.</strong><br>
    Le dataset de <strong>6 285 séquences</strong> est propre, dédupliqué et exempt de redondances. 
    Le dataset final de <strong>1 497 séquences</strong> (clustering 90%) est prêt pour l'encodage 
    par <strong>ESM-2</strong> et l'entraînement du modèle de prédiction multi-label de résistance aux antibiotiques.
    </div>
    """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
#  RENDER PRINCIPAL
# ─────────────────────────────────────────────
def render():
    _init()
    inject_global_css()
    _inject_pipeline_css()

    # ── En-tête ──
    st.markdown(
        '<div class="sh-title pl-wrap">🧬 Prétraitement des Séquences Protéiques</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
    <div class="hbanner">
    Ce pipeline décrit le processus complet de récupération et de préparation des séquences protéiques 
    des gènes de résistance aux antibiotiques (ARG) à partir de la base <strong>CARD</strong>. 
    Chaque étape est documentée avec ses justifications biologiques et computationnelles.
    L'objectif est de produire un dataset <em>fiable, propre et sans data leakage</em>, 
    prêt pour l'encodage par ESM-2 et la classification multi-label.
    </div>
    """,
        unsafe_allow_html=True,
    )

    # ── Vue d'ensemble ──
    _pipeline_overview_block()

    # ── Sélecteur d'étapes ──
    st.markdown("### 🔎 Sélectionnez une étape")
    cols = st.columns(4)
    steps = [
        ("01", "📥", "Parsing JSON\n+ Extraction"),
        ("02", "🔬", "Filtrage\nQualité"),
        ("03", "🔑", "Déduplication\nMD5 & CD-HIT"),
        ("04", "🧩", "Clustering\nCD-HIT"),
    ]
    for i, (num, emoji, title) in enumerate(steps):
        with cols[i]:
            is_active = st.session_state.pipeline_step == num
            if st.button(
                f"{emoji} Étape {num}\n{title}",
                key=f"step_btn_{num}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state.pipeline_step = None if is_active else num
                for k in [
                    "show_md5_detail",
                    "show_cdhit_detail",
                    "show_x_analysis",
                    "show_data_leakage",
                    "show_union_detail",
                    "show_md5_vs_cdhit",
                    "show_dedup_conclusion",
                    "show_cdhit_algo",
                    "show_cdhit_params",
                    "show_clstr_format",
                ]:
                    st.session_state[k] = False
                st.rerun()

    # ── Contenu de l'étape ──
    step = st.session_state.pipeline_step
    if step == "01":
        _step_01()
    elif step == "02":
        _step_02()
    elif step == "03":
        _step_03()
    elif step == "04":
        _step_04()
    else:
        st.markdown(
            '<div style="text-align:center;color:var(--muted);font-size:.84rem;margin:18px 0;padding:20px;'
            'background:#f8fafc;border-radius:14px;border:1px dashed rgba(0,180,216,.2);">'
            "☝️ Cliquez sur une étape ci-dessus pour afficher son contenu détaillé."
            "</div>",
            unsafe_allow_html=True,
        )

    # ── Tableau état final ──
    st.markdown("---")
    _pipeline_state_table()
