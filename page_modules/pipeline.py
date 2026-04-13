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
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ─────────────────────────────────────────────
#  CSS local
# ─────────────────────────────────────────────
def _inject_pipeline_css():
    st.markdown(
        """
    <style>
    .pl-wrap { animation: plFadeUp .35s ease both; }
    @keyframes plFadeUp {
        from { opacity:0; transform:translateY(14px); }
        to   { opacity:1; transform:translateY(0); }
    }

    /* ── Contenu étape ── */
    .step-content {
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 28px 32px;
        margin-top: 8px;
        box-shadow: 0 4px 20px rgba(0,100,180,.07);
        animation: plFadeUp .3s ease both;
    }
    .step-header {
        display: flex; align-items: center; gap: 14px;
        margin-bottom: 20px;
    }
    .step-num-badge {
        background: linear-gradient(135deg, var(--navy), var(--ocean));
        color: #fff; border-radius: 12px;
        padding: 8px 14px; font-size: .72rem;
        font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase;
        white-space: nowrap;
    }
    .step-title-big {
        font-size: 1.25rem; font-weight: 800; color: var(--navy);
    }

    /* ── Pipeline flow ── */
    .pipeline-overview {
        background: linear-gradient(135deg, #C9D2DA, #D3DCE3);
        border: 1px solid var(--border);
        border-radius: 20px; padding: 28px 20px;
        margin-bottom: 20px;
    }
    .pipeline-flow {
        display: flex; flex-wrap: wrap;
        align-items: center; gap: 0;
        justify-content: center; margin: 16px 0 8px;
    }
    .pf-step {
        background: linear-gradient(135deg, var(--navy), var(--ocean));
        color: #fff; border-radius: 14px;
        padding: 14px 16px; text-align: center;
        min-width: 115px; max-width: 150px; flex: 1;
        box-shadow: 0 4px 14px rgba(2,62,138,.22);
        transition: transform .2s;
    }
    .pf-step:hover { transform: translateY(-4px); }
    .pf-step .pf-num  { font-size:.6rem; font-weight:800; letter-spacing:1.5px; opacity:.75; margin-bottom:4px; }
    .pf-step .pf-ico  { font-size:1.4rem; margin-bottom:6px; display:block; }
    .pf-step .pf-name { font-size:.75rem; font-weight:700; line-height:1.3; }
    .pf-step .pf-cnt  { font-size:.7rem; opacity:.75; margin-top:4px; }
    .pf-arrow { color: var(--ocean); font-size:1.1rem; padding:0 6px; flex-shrink:0; }

    /* ── Boîte définition ── */
    .def-box {
        background: linear-gradient(135deg, #f0f8ff, #e4f3fb);
        border: 1px solid var(--border);
        border-left: 4px solid var(--ocean);
        border-radius: 14px;
        padding: 20px 24px;
        margin-top: 12px;
        animation: plFadeUp .25s ease both;
    }
    .def-box .def-title {
        font-size: .95rem; font-weight: 800;
        color: var(--navy); margin-bottom: 10px;
    }
    .def-box p { font-size: .85rem; color: var(--text); line-height: 1.85; margin: 0; }

    /* ── Data leakage box ── */
    .leakage-box {
        background: linear-gradient(135deg, #fff5f5, #ffe8e8);
        border: 1px solid #fca5a5;
        border-left: 4px solid #ef4444;
        border-radius: 14px;
        padding: 20px 24px;
        margin-top: 12px;
        animation: plFadeUp .25s ease both;
    }
    .leakage-box .lb-title {
        font-size: .95rem; font-weight: 800;
        color: #991b1b; margin-bottom: 12px;
    }
    .leakage-box p { font-size: .85rem; color: #7f1d1d; line-height: 1.85; margin: 0 0 10px; }
    .leakage-example {
        background: rgba(239,68,68,.08);
        border-radius: 10px; padding: 12px 16px;
        font-size: .82rem; color: #7f1d1d;
        line-height: 1.75; margin-top: 8px;
        border: 1px dashed #fca5a5;
    }
    .leakage-example strong { color: #991b1b; }

    /* ── Union strategy box ── */
    .union-box {
        background: linear-gradient(135deg, #f0fdf4, #dcfce7);
        border: 1px solid #86efac;
        border-left: 4px solid #16a34a;
        border-radius: 14px;
        padding: 20px 24px;
        margin-top: 12px;
        animation: plFadeUp .25s ease both;
    }
    .union-box .ub-title {
        font-size: .95rem; font-weight: 800;
        color: #14532d; margin-bottom: 10px;
    }
    .union-box p { font-size: .85rem; color: #166534; line-height: 1.85; margin: 0 0 8px; }

    /* ── Métriques ── */
    .metrics-row { display:flex; gap:12px; flex-wrap:wrap; margin:16px 0; }
    .metric-card {
        flex:1; min-width:110px;
        background: linear-gradient(135deg, var(--navy), var(--ocean));
        border-radius:14px; padding:16px 14px;
        text-align:center; color:#fff;
        box-shadow:0 4px 14px rgba(2,62,138,.2);
    }
    .metric-card .mc-val { font-size:1.5rem; font-weight:900; margin-bottom:4px; }
    .metric-card .mc-lbl { font-size:.7rem; opacity:.8; letter-spacing:.5px; line-height:1.4; }
    .metric-card.light {
        background: linear-gradient(135deg, var(--sky), var(--cerulean));
    }
    .metric-card.green {
        background: linear-gradient(135deg, #16a34a, #22c55e);
    }

    /* ── Tag justification ── */
    .justif-tag {
        background: #fff8e1; border:1px solid #ffc107;
        border-radius:8px; padding:12px 16px;
        font-size:.83rem; color:#78350f;
        margin-top:10px; line-height:1.75;
    }

    /* ── Analyse X ── */
    .x-seq-card {
        background: #fff8e1; border:1px solid #ffc107;
        border-left:4px solid #f59e0b;
        border-radius:12px; padding:14px 18px;
        margin-bottom:10px;
    }
    .x-seq-card .xsc-header { font-size:.85rem; font-weight:800; color:#78350f; margin-bottom:6px; }
    .x-seq-card .xsc-seq {
        font-family:monospace; font-size:.78rem;
        background:rgba(0,0,0,.06); border-radius:6px;
        padding:6px 10px; color:#1a1a1a; margin-bottom:8px;
    }
    .x-seq-card .xsc-row { font-size:.78rem; color:#5d4037; line-height:1.75; }

    /* ── Result highlight ── */
    .result-highlight {
        background: linear-gradient(135deg, var(--navy), var(--ocean));
        border-radius: 16px; padding: 20px 24px;
        color: #fff; margin: 16px 0;
        box-shadow: 0 6px 20px rgba(2,62,138,.22);
    }
    .result-highlight .rh-title {
        font-size: .72rem; font-weight: 800;
        letter-spacing: 2px; text-transform: uppercase;
        opacity: .8; margin-bottom: 8px;
    }
    .result-highlight .rh-val {
        font-size: 1.6rem; font-weight: 900; margin-bottom: 4px;
    }
    .result-highlight .rh-desc {
        font-size: .82rem; opacity: .85; line-height: 1.6;
    }

    /* ── Sub-section title ── */
    .subsection-title {
        font-size: 1rem; font-weight: 800;
        color: var(--navy); margin: 18px 0 10px;
        padding-left: 10px;
        border-left: 3px solid var(--sky);
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
#  Vue d'ensemble pipeline
# ─────────────────────────────────────────────
def _pipeline_overview_block():
    st.markdown(
        """
    <div class="pipeline-overview pl-wrap">
        <p class="sh-eyebrow" style="text-align:center; margin-bottom:4px;">
            Prétraitement des Séquences Protéiques
        </p>
        <div style="text-align:center;font-size:1rem;font-weight:800;color:var(--navy);margin-bottom:16px;">
            Pipeline Extraction &amp; Nettoyage — CARD → Dataset propre pour ESM-2
        </div>
        <div class="pipeline-flow">
            <div class="pf-step">
                <div class="pf-num">Étape 01</div>
                <span class="pf-ico">📥</span>
                <div class="pf-name">Parsing JSON<br>+ Extraction</div>
                <div class="pf-cnt">6 318 séq.</div>
            </div>
            <div class="pf-arrow">→</div>
            <div class="pf-step">
                <div class="pf-num">Étape 02</div>
                <span class="pf-ico">🔬</span>
                <div class="pf-name">Filtrage<br>Qualité</div>
                <div class="pf-cnt">6 313 séq.</div>
            </div>
            <div class="pf-arrow">→</div>
            <div class="pf-step">
                <div class="pf-num">Étape 03</div>
                <span class="pf-ico">🔑</span>
                <div class="pf-name">Déduplication<br>MD5 &amp; CD-HIT</div>
                <div class="pf-cnt">6 285 séq.</div>
            </div>
            <div class="pf-arrow">→</div>
            <div class="pf-step" style="background:linear-gradient(135deg,#0a2463,var(--navy));">
                <div class="pf-num">Étape 04</div>
                <span class="pf-ico">🧩</span>
                <div class="pf-name">Clustering<br>CD-HIT 80% | 90%</div>
                <div class="pf-cnt">1 319 | 1 497 séq.</div>
            </div>
        </div>
        <div style="text-align:center;font-size:.82rem;color:var(--muted);margin-top:6px;">
            Cliquez sur une étape ci-dessous pour afficher son contenu détaillé
        </div>
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
        '<div class="metric-card"><div class="mc-val">~6 318</div><div class="mc-lbl">Séquences<br>extraites</div></div>'
        '<div class="metric-card light"><div class="mc-val">7</div><div class="mc-lbl">Colonnes<br>structurées</div></div>'
        '<div class="metric-card"><div class="mc-val">46</div><div class="mc-lbl">Classes<br>d\'antibiotiques</div></div>'
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
        '<div class="metric-card"><div class="mc-val">6 318</div><div class="mc-lbl">Séquences<br>en entrée</div></div>'
        '<div class="metric-card green"><div class="mc-val">6 313</div><div class="mc-lbl">Séquences<br>conservées</div></div>'
        '<div class="metric-card light"><div class="mc-val">5</div><div class="mc-lbl">Séquences<br>supprimées</div></div>'
        '<div class="metric-card"><div class="mc-val">50 aa</div><div class="mc-lbl">Seuil<br>minimum</div></div>'
        "</div>",
        unsafe_allow_html=True,
    )

    # Bouton analyse séquences X
    btn_x = (
        "🔼 Masquer l'analyse"
        if st.session_state.show_x_analysis
        else "🔍 Voir détail — Pourquoi ces 5 séquences ont été supprimées ?"
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
                "seq": "...GEIDITXPPVRERPS...",
                "nb_x": 1,
                "cause": "N dans l'ADN (ATCACGNGGCCC) — le N est une base indéterminée (A, T, C ou G). Le codon NGG ne peut pas être traduit avec certitude → X",
                "bio": "Ribonucléase PH réelle isolée de Streptomyces sp. WAC4747, bactérie du sol productrice d'antibiotiques.",
                "cultivable": "✅ Oui",
                "ncbi": "✅ Oui — séquence officielle avec X",
            },
            {
                "acc": "ACS83748.1",
                "gene": "tet(43)",
                "org": "uncultured bacterium AOTet43",
                "seq": "...GLVGAMPENRTSLGAALNDTAQEVGTSLGMAVIGTLIAVLXTTTLPNGDXSLDLATS...",
                "nb_x": 2,
                "cause": "Bases S (= C ou G) et Y (= C ou T) ambiguës → deux codons non résolvables → 2 X",
                "bio": "Séquence obtenue par métagénomique directement depuis l'environnement. La bactérie existe mais n'a jamais été cultivée en laboratoire.",
                "cultivable": "❌ Non cultivée (métagénomique)",
                "ncbi": "✅ Oui — 2 X dans la séquence officielle",
            },
            {
                "acc": "AAR96051.1",
                "gene": "otr(C)",
                "org": "Streptomyces rimosus",
                "seq": "...VGLGPXGAAXXRGALP...",
                "nb_x": 3,
                "cause": "N répété dans GGGCCGANCGGCGCGGCAANANAACGT — 3 zones indéterminées → 3 codons non traduits → 3 X",
                "bio": "Streptomyces rimosus est la bactérie productrice de l'oxytétracycline. otr(C) est un gène de résistance à la tétracycline réel et caractérisé.",
                "cultivable": "✅ Oui",
                "ncbi": "✅ Oui — séquençage original 2004, jamais resoumis corrigé",
            },
            {
                "acc": "AHF82023.1",
                "gene": "AQU-2",
                "org": "Aeromonas hydrophila",
                "seq": "...AAPXEMGSQRLFNK...",
                "nb_x": 1,
                "cause": "K = G ou T (code IUPAC ambigu) dans GCGCCGAAKGAGATG → codon AAK non résolvable → X",
                "bio": "Beta-lactamase réelle isolée d'Aeromonas hydrophila, pathogène aquatique courant, publiée en 2014.",
                "cultivable": "✅ Oui",
                "ncbi": "✅ Oui — séquence officielle telle que soumise",
            },
            {
                "acc": "AHF82024.1",
                "gene": "AQU-3",
                "org": "Aeromonas dhakensis",
                "seq": "...GAYVAFVXAKGVGI...",
                "nb_x": 1,
                "cause": "M = A ou C (IUPAC ambigu) dans GCGCCTTCGTGCMGGCC → codon non résolvable → X",
                "bio": "Paralogue d'AQU-2, publiée dans le même article 2014. Aeromonas dhakensis est un pathogène émergent.",
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
            """
**✅ Conclusion — Décision validée :**
Toutes ces séquences sont biologiquement réelles et documentées dans NCBI avec leurs caractères X.
Leur suppression est la **décision correcte et justifiée** : ESM-2 ne tolère pas les acides aminés ambigus,
et ces 5 séquences auraient provoqué des erreurs d'encodage ou des vecteurs d'embedding non fiables.
        """
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
    La base CARD référence fréquemment <strong>une même séquence protéique plusieurs fois</strong> avec des annotations différentes :
    soit parce qu'une protéine confère une résistance à <em>plusieurs antibiotiques</em> (plusieurs ARO distincts),
    soit parce qu'elle a été annotée indépendamment dans différentes souches. 
    Cette étape supprime ces redondances <strong>exactes</strong> avant l'encodage par ESM-2 — 
    encoder deux fois la même séquence serait un gaspillage de ressources computationnelles et introduirait
    des doublons dans le dataset d'entraînement.
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Résultats globaux
    st.markdown(
        '<div class="metrics-row">'
        '<div class="metric-card"><div class="mc-val">6 313</div><div class="mc-lbl">Séquences<br>en entrée</div></div>'
        '<div class="metric-card green"><div class="mc-val">6 285</div><div class="mc-lbl">Séquences<br>conservées</div></div>'
        '<div class="metric-card light"><div class="mc-val">28</div><div class="mc-lbl">Doublons<br>supprimés</div></div>'
        '<div class="metric-card"><div class="mc-val">0.4%</div><div class="mc-lbl">Taux de<br>réduction</div></div>'
        "</div>",
        unsafe_allow_html=True,
    )

    # ── Approche A : MD5
    st.markdown(
        '<div class="subsection-title">🔑 Approche A — Déduplication par hachage MD5</div>',
        unsafe_allow_html=True,
    )

    btn_md5 = (
        "🔼 Masquer la définition MD5"
        if st.session_state.show_md5_detail
        else "📖 Qu'est-ce que MD5 ? ▼"
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

    st.markdown("**Analyse des 28 suppressions MD5 :**")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
        <div class="section-card">
        <strong>Cas 1 — Même séquence, ARO différents</strong> <em>(majoritaire)</em><br><br>
        La même protéine (<code>NP_218312.1</code>, <code>NP_218371.1</code>, <code>NP_215774.1</code>) 
        est référencée plusieurs fois dans CARD car elle confère une résistance à 
        <em>plusieurs antibiotiques</em>. CARD lui associe un ARO distinct pour chaque résistance, 
        mais la séquence protéique est rigoureusement identique. 
        MD5 détecte et supprime ces doublons.
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
        <div class="section-card">
        <strong>Cas 2 — Accessions différentes, séquence identique</strong><br><br>
        Protéines annotées indépendamment dans différentes souches bactériennes.<br><br>
        Ex : <code>AAN43827.1</code> / <code>AAC75291.1</code> — deux accessions pour 
        le même gène <em>gyrA</em> dans <em>Shigella flexneri</em> et <em>E. coli</em>. 
        Séquence protéique rigoureusement identique.
        </div>
        """,
            unsafe_allow_html=True,
        )

    # ── Approche B : CD-HIT 100%
    st.markdown(
        '<div class="subsection-title">🧩 Approche B — Déduplication CD-HIT à 100% d\'identité</div>',
        unsafe_allow_html=True,
    )

    btn_cd = (
        "🔼 Masquer la définition CD-HIT"
        if st.session_state.show_cdhit_detail
        else "📖 Qu'est-ce que CD-HIT ? ▼"
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
                contient exactement 1 représentant conservé. Aucun cas de containment strict (A ⊂ B) 
                n'a été détecté.
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # ── Comparaison MD5 vs CD-HIT
    btn_comp = (
        "🔼 Masquer la comparaison"
        if st.session_state.show_md5_vs_cdhit
        else "⚖️ Voir comparaison MD5 vs CD-HIT ▼"
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
                ],
                "MD5": [
                    "✅",
                    "❌ partiellement*",
                    "✅",
                    "❌ non détecté",
                    "O(n) — très rapide",
                    "Aucune",
                ],
                "CD-HIT 100%": [
                    "✅",
                    "❌",
                    "✅",
                    "❌ non observé ici",
                    "O(n log n)",
                    "CD-HIT installé",
                ],
            }
        )
        st.dataframe(df_comp, use_container_width=True, hide_index=True)
        st.caption(
            "*MD5 détecte la duplication de séquence mais ne distingue pas biologiquement les ARO multiples — comportement identique à CD-HIT dans ce contexte."
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
        st.success(
            """
**✅ Conclusion — Étape 03 validée**

Dans CARD, une même séquence protéique peut apparaître plusieurs fois avec des annotations différentes, 
notamment lorsqu'elle est associée à plusieurs ARO ou plusieurs classes de résistance.

Les deux approches testées **(MD5 et CD-HIT 100%)** produisent des résultats **identiques** sur ce dataset :
- **6 285 séquences uniques** conservées après suppression de **28 doublons exacts**
- La stratégie **Union** garantit qu'aucune drug class n'est perdue lors de la fusion
- Le dataset est maintenant prêt pour le clustering CD-HIT (étape 04) et l'encodage ESM-2
        """
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
    c'est ce qu'on appelle le <em>data leakage</em>. Cette étape applique un clustering 
    CD-HIT pour regrouper ces séquences et assurer une partition propre du dataset.
    </div>
    """,
        unsafe_allow_html=True,
    )

    # ── Data Leakage
    st.markdown(
        '<div class="subsection-title">⚠️ Qu\'est-ce que le Data Leakage ?</div>',
        unsafe_allow_html=True,
    )

    btn_leak = (
        "🔼 Masquer l'explication"
        if st.session_state.show_data_leakage
        else "📖 Comprendre le data leakage — avec exemple ▼"
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
                <strong>🔬 Exemple concret :</strong><br><br>
                Supposons deux variants du gène <em>TEM-1</em> (beta-lactamase) :<br>
                — <code>TEM-1a</code> : séquence de 286 aa → <strong>Train set</strong><br>
                — <code>TEM-1b</code> : séquence de 286 aa, 95% identique à TEM-1a → <strong>Test set</strong><br><br>
                Le modèle, ayant vu TEM-1a pendant l'entraînement, reconnaît trivialement TEM-1b 
                au test. Il <strong>mémorise</strong> la famille de gènes au lieu d'apprendre 
                les caractéristiques généralisables de la résistance aux beta-lactamines.<br><br>
                <strong>Conséquence :</strong> F1-score et AUC-ROC artificiellement élevés → 
                le modèle semblera performant mais échouera sur de nouvelles séquences jamais vues.
            </div>
            <p style="margin-top:12px;">
                <strong>Solution :</strong> Toutes les séquences d'un même cluster CD-HIT doivent 
                rester dans le <em>même split</em>. Le split train/test se fait au niveau des 
                <strong>clusters</strong> et non des séquences individuelles.
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # ── Paramètres
    st.markdown(
        '<div class="subsection-title">⚙️ Paramètres d\'exécution CD-HIT</div>',
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
**Communs aux deux seuils :**
- `-g 1` — mode précis : chaque séquence est assignée au cluster **le plus similaire**
- Mémoire : `4 000 MB`
- Threads : `4`
- `-d 0` — accession complète dans le fichier `.clstr` (pas de troncature)
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

    # ── Résultats
    st.markdown(
        '<div class="subsection-title">📊 Résultats comparatifs 80% vs 90%</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="metrics-row">'
        '<div class="metric-card"><div class="mc-val">1 319</div><div class="mc-lbl">Clusters<br>à 80%</div></div>'
        '<div class="metric-card green"><div class="mc-val">1 497</div><div class="mc-lbl">Clusters<br>à 90% ✅</div></div>'
        '<div class="metric-card light"><div class="mc-val">+178</div><div class="mc-lbl">Séquences<br>de différence</div></div>'
        '<div class="metric-card"><div class="mc-val">76.2%</div><div class="mc-lbl">Réduction<br>à 90%</div></div>'
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
    - À **80%**, elles sont absorbées dans des clusters existants (clustering plus agressif)
    - À **90%**, elles sont suffisamment différentes pour former leur **propre cluster** (plus de diversité conservée)
    - Ces 178 séquences seront testées pour évaluer si elles apportent de l'information ou du bruit
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

- Tester si les **178 séquences supplémentaires** (présentes à 90% mais absorbées à 80%) apportent de l'information ou du bruit
- Comparer les deux modèles entraînés sur 80% et 90% via **F1-score** et **AUC-ROC**
- Si les performances sont similaires → les 178 séquences sont redondantes pour le modèle
- Si les performances diffèrent → les 178 séquences capturent de la **diversité biologique réelle**
        """
        )
    with tab3:
        st.error(
            """
**Règle critique — prévention absolue du data leakage :**

Toutes les séquences d'un même cluster **doivent rester dans le même split**.

Le split train/test se fait **au niveau des clusters**, pas des séquences individuelles.

**Exemple :**
- Cluster C42 contient 5 séquences similaires (TEM variants)
- → Toutes les 5 vont dans le train set **ou** toutes dans le test set
- → Jamais 3 dans train et 2 dans test

**Sinon :** fuite d'information → F1-score artificiellement élevé → modèle qui mémorise.
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
            "Séquences": ["6 318", "6 313", "6 285", "1 319", "1 497 ✅", "—"],
            "Fichier sortie": [
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
    Le dataset de <strong>1 497 séquences</strong> (seuil 90%, dataset final) est propre, dédupliqué 
    et exempt de redondances. Il est prêt pour l'encodage par <strong>ESM-2</strong> et 
    l'entraînement du modèle de prédiction multi-label de résistance aux antibiotiques.
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
                # Reset tous les sous-panneaux
                for k in [
                    "show_md5_detail",
                    "show_cdhit_detail",
                    "show_x_analysis",
                    "show_data_leakage",
                    "show_union_detail",
                    "show_md5_vs_cdhit",
                    "show_dedup_conclusion",
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
            '<div style="text-align:center;color:var(--muted);font-size:.82rem;margin:14px 0;">'
            "☝️ Cliquez sur une étape ci-dessus pour afficher son contenu détaillé."
            "</div>",
            unsafe_allow_html=True,
        )

    # ── Tableau état final ──
    st.markdown("---")
    _pipeline_state_table()
