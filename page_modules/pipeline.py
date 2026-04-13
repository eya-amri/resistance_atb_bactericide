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

    /* ── Contenu de l'étape ── */
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
        min-width: 115px; max-width: 145px; flex: 1;
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
        font-size: .9rem; font-weight: 800;
        color: var(--navy); margin-bottom: 10px;
    }
    .def-box p { font-size: .85rem; color: var(--text); line-height: 1.8; margin: 0; }

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

    /* ── Tag justification ── */
    .justif-tag {
        background: #fff8e1; border:1px solid #ffc107;
        border-radius:8px; padding:12px 16px;
        font-size:.83rem; color:#78350f;
        margin-top:10px; line-height:1.7;
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
            Pipeline Extraction &amp; Nettoyage — CARD → Dataset propre
        </div>
        <div class="pipeline-flow">
            <div class="pf-step">
                <div class="pf-num">Étape 01</div>
                <span class="pf-ico">📥</span>
                <div class="pf-name">Parsing JSON<br>+ Extraction</div>
                <div class="pf-cnt">~6 500 séq.</div>
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
                <div class="pf-name">Déduplication<br>MD5</div>
                <div class="pf-cnt">6 285 séq.</div>
            </div>
            <div class="pf-arrow">→</div>
            <div class="pf-step" style="background:linear-gradient(135deg,#0a2463,var(--navy));">
                <div class="pf-num">Étape 04</div>
                <span class="pf-ico">🧩</span>
                <div class="pf-name">Clustering<br>CD-HIT 90%</div>
                <div class="pf-cnt">1 497 séq.</div>
            </div>
        </div>
        <div style="text-align:center;font-size:.82rem;color:var(--muted);margin-top:6px;">
            Cliquez sur une étape ci-dessous pour afficher le détail complet
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

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🎯 Champs extraits par séquence**")
        for f in [
            "`id`",
            "`ARO_id`",
            "`ARO_name`",
            "`sequence_id`",
            "`sequence`",
            "`protein_accession`",
            "`drug_classes`",
        ]:
            st.markdown(f"- {f}")
    with col2:
        st.markdown("**⚙️ Caractéristiques**")
        st.markdown(
            """
- Compatible format JSON CARD
- Exportable en FASTA
- Annotations essentielles maintenues
- Préparation pour ESM-2
        """
        )

    st.markdown("**📄 Résultat attendu — Colonnes CSV :**")
    st.code(
        "id | ARO_id | ARO_name | sequence_id | sequence | protein_accession | drug_classes",
        language="text",
    )

    st.markdown(
        """
    <div class="hbanner">
    <strong>Objectif :</strong> Transformer les données brutes JSON de CARD en un dataset homogène 
    et structuré, prêt pour les étapes de nettoyage suivantes.
    </div>
    """,
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

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**❌ Critères de suppression**")
        st.markdown(
            """
- Séquences **< 50 acides aminés**
- Caractères : `X`, `B`, `Z`, `U`, `O`
        """
        )
        st.markdown(
            '<div class="metrics-row">'
            '<div class="metric-card"><div class="mc-val">6 313</div><div class="mc-lbl">Séquences<br>conservées</div></div>'
            '<div class="metric-card"><div class="mc-val">50 aa</div><div class="mc-lbl">Seuil<br>minimum</div></div>'
            "</div>",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            '<div class="justif-tag">'
            "📚 <strong>Seuil 50 aa :</strong> Standard de <em>DeepARG (Arango-Argoty et al., 2018)</em>. "
            "Les fragments sous ce seuil ne représentent pas des gènes fonctionnels complets "
            "et génèrent du bruit dans tout encodeur.<br><br>"
            "📚 <strong>Caractères X, B, Z, U, O :</strong> Ambigus ou rares, "
            "incompatibles avec les encodeurs ESM-2."
            "</div>",
            unsafe_allow_html=True,
        )

    btn_x = (
        "🔼 Masquer l'analyse"
        if st.session_state.show_x_analysis
        else "🔍 Voir détail — Analyse des séquences filtrées (caractères X)"
    )
    if st.button(btn_x, key="btn_x_analysis", type="secondary"):
        st.session_state.show_x_analysis = not st.session_state.show_x_analysis
        st.rerun()

    if st.session_state.show_x_analysis:
        st.markdown("---")
        st.markdown("#### 🔬 Analyse des 5 séquences contenant des caractères X")
        st.markdown(
            """
        <div class="hbanner">
        Ces séquences sont <strong>biologiquement réelles</strong> — le X n'est pas une erreur du pipeline.
        C'est une limite du séquençage original, documentée dans NCBI.
        Leur suppression est la décision correcte pour ESM-2 qui ne tolère pas les ambiguïtés.
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
                "cause": "N dans l'ADN (ATCACGNGGCCC) → codon NGG non résolvable → X",
                "cultivable": "✅ Oui",
                "ncbi": "✅ Oui",
            },
            {
                "acc": "ACS83748.1",
                "gene": "tet(43)",
                "org": "uncultured bacterium AOTet43",
                "seq": "...GLVGAMPENRTSLGAALNDTAQEVGTSLGMAVIGTLIAVLXTTTLPNGDXSLDLATS...",
                "nb_x": 2,
                "cause": "Bases S (C ou G) et Y (C ou T) → deux codons non résolvables → 2 X",
                "cultivable": "❌ Non cultivée (métagénomique)",
                "ncbi": "✅ Oui",
            },
            {
                "acc": "AAR96051.1",
                "gene": "otr(C)",
                "org": "Streptomyces rimosus",
                "seq": "...VGLGPXGAAXXRGALP...",
                "nb_x": 3,
                "cause": "N répété dans l'ADN (GGGCCGANCGGCGCGGCAANANAACGT) → 3 codons non résolvables",
                "cultivable": "✅ Oui (productrice d'oxytétracycline)",
                "ncbi": "✅ Oui (séquençage 2004 non recorrigé)",
            },
            {
                "acc": "AHF82023.1",
                "gene": "AQU-2",
                "org": "Aeromonas hydrophila",
                "seq": "...AAPXEMGSQRLFNK...",
                "nb_x": 1,
                "cause": "K = G ou T (IUPAC ambigu) dans GCGCCGAAKGAGATG → codon AAK non résolvable",
                "cultivable": "✅ Oui (pathogène aquatique)",
                "ncbi": "✅ Oui",
            },
            {
                "acc": "AHF82024.1",
                "gene": "AQU-3",
                "org": "Aeromonas dhakensis",
                "seq": "...GAYVAFVXAKGVGI...",
                "nb_x": 1,
                "cause": "M = A ou C (IUPAC ambigu) dans GCGCCTTCGTGCMGGCC → codon non résolvable",
                "cultivable": "✅ Oui (pathogène émergent)",
                "ncbi": "✅ Oui",
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
                    <strong>Cultivable :</strong> {s['cultivable']}<br>
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
            "**Conclusion :** Toutes ces séquences sont biologiquement réelles. Le X n'est pas une erreur du pipeline — c'est une limite du séquençage original documentée dans NCBI. Leur suppression est la décision correcte pour ESM-2."
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
            <span class="step-title-big">Déduplication exacte par MD5</span>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    CARD contient plusieurs accessions GenBank pour le même ARO avec des séquences parfois identiques.
    Un **hash MD5** sur la séquence brute détecte ces doublons en **O(n)** sans aucune dépendance externe.
    """
    )

    st.markdown(
        '<div class="metrics-row">'
        '<div class="metric-card"><div class="mc-val">6 313</div><div class="mc-lbl">Séquences<br>en entrée</div></div>'
        '<div class="metric-card"><div class="mc-val">6 285</div><div class="mc-lbl">Séquences<br>conservées</div></div>'
        '<div class="metric-card"><div class="mc-val">28</div><div class="mc-lbl">Supprimées</div></div>'
        '<div class="metric-card"><div class="mc-val">0.4%</div><div class="mc-lbl">Taux de<br>réduction</div></div>'
        "</div>",
        unsafe_allow_html=True,
    )

    # Bouton définition MD5
    btn_md5 = (
        "🔼 Masquer la définition MD5"
        if st.session_state.show_md5_detail
        else "📖 Voir définition — Qu'est-ce que MD5 ?"
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
                MD5 est une <strong>fonction de hachage cryptographique</strong> qui transforme une chaîne de 
                caractères de longueur arbitraire en une empreinte numérique fixe de <strong>128 bits</strong> 
                (32 caractères hexadécimaux).<br><br>
                <strong>Dans ce pipeline :</strong> chaque séquence est normalisée (majuscules, suppression 
                des espaces) puis hachée. Deux séquences produisant le <em>même hash MD5</em> sont 
                rigoureusement identiques. La première occurrence est conservée, les suivantes supprimées.<br><br>
                <strong>Avantage clé :</strong> Complexité <strong>O(n)</strong> — une seule passe sur toutes 
                les séquences, sans comparaison pairwise. Plus rapide que CD-HIT pour la déduplication exacte, 
                et complémentaire à lui.
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("**🔍 Analyse des 28 suppressions**")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
        <div class="section-card">
        <strong>Cas 1 — Même séquence, ARO différents</strong> <em>(majoritaire)</em><br><br>
        La même protéine (<code>NP_218312.1</code>, <code>NP_218371.1</code>, <code>NP_215774.1</code>) 
        est référencée plusieurs fois car elle confère une résistance à <em>plusieurs antibiotiques</em>. 
        CARD lui associe un ARO distinct pour chaque résistance, mais la séquence est identique.
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
        <div class="section-card">
        <strong>Cas 2 — Accessions différentes, séquence identique</strong><br><br>
        Protéines annotées indépendamment dans différentes souches bactériennes.<br>
        Ex : <code>AAN43827.1</code> / <code>AAC75291.1</code> pour <em>gyrA</em> de 
        <em>Shigella flexneri</em> et <em>E. coli</em>.
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("**⚖️ Comparaison MD5 vs CD-HIT 100% — mêmes résultats sur ce dataset**")
    import pandas as pd

    df_comp = pd.DataFrame(
        {
            "Critère": [
                "Séquences identiques (string exact)",
                "Même accession + ARO différents",
                "Accessions différentes identiques",
                "Sous-séquence (A ⊂ B)",
            ],
            "MD5": ["✅", "❌ partiellement", "✅", "❌ théorique"],
            "CD-HIT 100%": ["✅", "❌", "✅", "❌ non observé"],
        }
    )
    st.dataframe(df_comp, use_container_width=True, hide_index=True)

    st.markdown(
        """
    <div class="justif-tag">
    💡 <strong>Conclusion :</strong> MD5 opère directement sur la chaîne brute, indépendamment des accessions 
    ou annotations. Cela permet de détecter <em>systématiquement</em> toutes les duplications exactes, 
    même lorsqu'elles sont associées à des ARO différents.
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
            <span class="step-title-big">Clustering CD-HIT — Réduction de redondance</span>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    **Near-duplicate clustering** sur les 6 285 séquences dédupliquées pour prévenir 
    le **data leakage** entre train et test sets. Deux seuils comparés : **80%** et **90%**.
    """
    )

    # Bouton définition CD-HIT
    btn_cd = (
        "🔼 Masquer la définition CD-HIT"
        if st.session_state.show_cdhit_detail
        else "📖 Voir définition — Qu'est-ce que CD-HIT ?"
    )
    if st.button(btn_cd, key="btn_cdhit_def", type="secondary"):
        st.session_state.show_cdhit_detail = not st.session_state.show_cdhit_detail
        st.rerun()

    if st.session_state.show_cdhit_detail:
        st.markdown(
            """
        <div class="def-box">
            <div class="def-title">🧩 CD-HIT — Cluster Database at High Identity with Tolerance</div>
            <p>
                CD-HIT est un programme de <strong>clustering de séquences biologiques</strong> par similarité.
                Il regroupe des séquences partageant un pourcentage d'identité ≥ à un seuil défini 
                (paramètre <code>-c</code>).<br><br>
                <strong>Principe :</strong> Pour chaque cluster, la séquence la plus longue est désignée 
                <em>représentante</em>. Les autres membres sont supprimés du dataset mais restent traçables 
                dans le fichier <code>.clstr</code>.<br><br>
                <strong>Paramètre word size (-n) :</strong> Pré-filtre rapide basé sur des k-mers. 
                CD-HIT recommande <code>n=5</code> pour les seuils ≥ 90% et <code>n=4</code> pour 80–90%.<br><br>
                <strong>Utilisation dans ce pipeline :</strong> Prévenir le data leakage — deux séquences 
                trop similaires ne doivent pas se retrouver dans des splits train/test différents, 
                sinon le modèle mémorise au lieu de généraliser.
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("**⚙️ Paramètres d'exécution**")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
**Communs aux deux seuils :**
- `-g 1` — mode précis (chaque séquence → cluster le plus similaire)
- Mémoire : `4 000 MB`
- Threads : `4`
- `-d 0` — accession complète dans `.clstr`
        """
        )
    with col2:
        st.markdown(
            """
**Spécifique par seuil :**
- Seuil 80% → `-c 0.8 -n 4`
- Seuil 90% → `-c 0.9 -n 5`

*(word size selon recommandations CD-HIT)*
        """
        )

    st.markdown("---")
    st.markdown("**📊 Résultats comparatifs**")
    st.markdown(
        '<div class="metrics-row">'
        '<div class="metric-card"><div class="mc-val">1 319</div><div class="mc-lbl">Clusters<br>à 80%</div></div>'
        '<div class="metric-card"><div class="mc-val">1 497</div><div class="mc-lbl">Clusters<br>à 90%</div></div>'
        '<div class="metric-card"><div class="mc-val">+178</div><div class="mc-lbl">Séquences<br>de différence</div></div>'
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
            "Seuil 90%": ["6 285", "1 497", "1 497", "4 788", "76.2 %", "5"],
            "Différence": ["—", "+178", "+178", "−178", "−2.8 pts", "—"],
        }
    )
    st.dataframe(df_clust, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("**🎯 Choix du seuil — Recommandations**")
    tab1, tab2, tab3 = st.tabs(
        ["✅ 90% — Dataset final", "🔍 80% — Robustesse", "⚠️ Split Train/Test"]
    )
    with tab1:
        st.success(
            """
**Seuil 90% recommandé — standard dans la littérature AMR.**

- Conserve la diversité biologique
- Élimine les redondances évidentes
- Adapté à l'encodage ESM-2

**→ Dataset final : 1 497 séquences**
        """
        )
    with tab2:
        st.info(
            """
Le seuil **80%** permet de tester si les 178 séquences supplémentaires apportent de l'information ou du bruit.

Comparaison via **F1-score** et **AUC-ROC**.
        """
        )
    with tab3:
        st.error(
            """
**Règle critique — prévention du data leakage :**

Toutes les séquences d'un même cluster **doivent rester dans le même split**.

Sinon → fuite d'information → performance artificiellement élevée.
        """
        )

    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Tableau état final
# ─────────────────────────────────────────────
def _pipeline_state_table():
    st.markdown("### 📁 État du pipeline — Récapitulatif")
    import pandas as pd

    df = pd.DataFrame(
        {
            "Étape": ["01", "02", "03", "04a", "04b", "05"],
            "Module": [
                "Extraction JSON",
                "Nettoyage",
                "Déduplication (MD5)",
                "Clustering 80%",
                "Clustering 90%",
                "ESM-2 + entraînement",
            ],
            "Séquences": ["~6 500", "6 313", "6 285", "1 319", "1 497", "—"],
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
    ✅ <strong>Pipeline complété jusqu'à l'étape 04.</strong><br>
    Le dataset de <strong>1 497 séquences</strong> (seuil 90%) est prêt pour l'encodage par 
    <strong>ESM-2</strong> et l'entraînement du modèle de prédiction multi-label.
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
    Ce pipeline décrit le processus de récupération et de préparation des séquences protéiques 
    des gènes de résistance aux antibiotiques (ARG) à partir de la base <strong>CARD</strong>. 
    Il assure que les séquences utilisées pour la prédiction multi-label soient 
    <em>fiables, valides et prêtes pour l'encodage</em>.
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
        ("03", "🔑", "Déduplication\nMD5"),
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
                st.session_state.show_md5_detail = False
                st.session_state.show_cdhit_detail = False
                st.session_state.show_x_analysis = False
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
