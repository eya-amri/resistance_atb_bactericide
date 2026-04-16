import streamlit as st
from utils.helpers import inject_global_css, info_box


# ─────────────────────────────────────────────
#  Session state
# ─────────────────────────────────────────────
def _init():
    defaults = {
        "neg_step": None,
        "show_reservoir_detail": False,
        "show_cdhit_detail_neg": False,
        "show_diamond_detail": False,
        "show_interpro_detail": False,
        "show_cdhit_algo_neg": False,
        "show_diamond_params": False,
        "show_interpro_dbs": False,
        "show_uniprot_arch": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ─────────────────────────────────────────────
#  CSS local — Design moderne
# ─────────────────────────────────────────────
def _inject_neg_pipeline_css():
    st.markdown(
        """
    <style>
    /* Styles spécifiques pour la page negative_pipeline */
    .pipeline-overview {
        background: linear-gradient(135deg, #ffffff, #f8fafc);
        border-radius: 24px;
        padding: 28px 24px;
        margin-bottom: 32px;
        border: 1px solid rgba(0, 180, 216, 0.15);
        box-shadow: 0 8px 20px rgba(0,0,0,0.03);
    }
    .po-eyebrow {
        font-size: 0.7rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: var(--ocean);
        font-weight: 700;
        margin-bottom: 12px;
    }
    .po-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: var(--navy);
        margin-bottom: 24px;
        line-height: 1.2;
    }
    .pipeline-flow {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 12px;
        margin-bottom: 20px;
        background: #f1f5f9;
        padding: 20px;
        border-radius: 20px;
    }
    .pf-step {
        flex: 1;
        min-width: 130px;
        background: white;
        border-radius: 16px;
        padding: 12px 10px;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        transition: all 0.2s ease;
    }
    .pf-step.active-step {
        border: 2px solid var(--sky);
        background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
        transform: translateY(-2px);
    }
    .pf-num {
        font-size: 0.9rem;
        font-weight: 600;
        color: var(--muted);
        margin-bottom: 6px;
    }
    .pf-ico {
        font-size: 1.8rem;
        display: block;
        margin-bottom: 6px;
    }
    .pf-name {
        font-size: 0.9rem;
        font-weight: 700;
        color: var(--navy);
        margin-bottom: 6px;
        line-height: 1.3;
    }
    .pf-cnt {
        font-size: 0.9rem;
        color: var(--ocean);
        font-weight: 600;
        background: #eef2ff;
        display: inline-block;
        padding: 2px 8px;
        border-radius: 20px;
    }
    .pf-status {
        font-size: 0.9rem;
        color: #10b981;
        font-weight: 600;
        margin-left: 6px;
    }
    .pf-arrow {
        font-size: 1.5rem;
        color: var(--sky);
        font-weight: 300;
    }
    .po-hint {
        font-size: 0.75rem;
        color: var(--muted);
        text-align: center;
        margin-top: 16px;
        font-style: italic;
    }
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
    .metrics-row {
        display: flex;
        flex-wrap: wrap;
        gap: 16px;
        margin: 24px 0;
    }
    .metric-card {
        background: #f8fafc;
        border-radius: 16px;
        padding: 16px 20px;
        flex: 1;
        text-align: center;
        border: 1px solid #e2e8f0;
    }
    .metric-card.green { background: #ecfdf5; border-color: #a7f3d0; }
    .metric-card.red { background: #fef2f2; border-color: #fecaca; }
    .metric-card.amber { background: #fffbeb; border-color: #fde68a; }
    .metric-card.light { background: #f0f9ff; border-color: #bae6fd; }
    .mc-val {
        font-size: 1.8rem;
        font-weight: 800;
        color: var(--navy);
        line-height: 1.2;
    }
    .mc-lbl {
        font-size: 0.7rem;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .justif-tag {
        background: #f1f5f9;
        border-left: 3px solid var(--sky);
        padding: 12px 16px;
        border-radius: 12px;
        font-size: 0.8rem;
        margin: 16px 0;
        color: var(--text);
    }
    .def-box, .algo-step, .param-explanation {
        background: #f8fafc;
        border-radius: 16px;
        padding: 20px;
        margin: 20px 0;
        border: 1px solid #e2e8f0;
    }
    .def-title {
        font-weight: 800;
        color: var(--navy);
        font-size: 1rem;
        margin-bottom: 12px;
    }
    .param-table {
        width: 100%;
        border-collapse: collapse;
        margin: 16px 0;
        font-size: 0.8rem;
    }
    .param-row td {
        padding: 12px;
        border-bottom: 1px solid #e2e8f0;
        vertical-align: top;
    }
    .param-row td:first-child {
        font-weight: 700;
        color: var(--navy);
        width: 120px;
    }
    .result-highlight {
        background: linear-gradient(135deg, #e0f2fe, #f0f9ff);
        border-radius: 20px;
        padding: 24px;
        text-align: center;
        margin: 20px 0;
    }
    .rh-title {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: var(--ocean);
    }
    .rh-val {
        font-size: 2rem;
        font-weight: 800;
        color: var(--navy);
        margin: 8px 0;
    }
    .swissprot-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 16px;
        border-left: 4px solid var(--sky);
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
#  Vue d'ensemble pipeline négatif
# ─────────────────────────────────────────────
def _pipeline_overview_block():
    active = st.session_state.neg_step

    steps = [
        ("05a", "🎲", "Reservoir Sampling\n70,000 séq.", "70,000", "✅"),
        ("05b", "🧬", "CD-HIT 90%\nRédundance", "58,171", "✅"),
        ("05c", "⚡", "DIAMOND\nHomologie ARG", "56,122", "✅"),
        ("05d", "🔬", "InterProScan\nDomaines", "56,122", "✅"),
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
    <div class="pipeline-overview">
        <div class="po-eyebrow">DATASET NÉGATIF — PIPELINE DE CONSTRUCTION</div>
        <div class="po-title">Filtrage multi‑niveaux pour un dataset de référence fiable</div>
        <div class="pipeline-flow">{flow_html}</div>
        <div class="po-hint">Cliquez sur une étape ci-dessous pour afficher son contenu détaillé</div>
    </div>
    """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
#  ÉTAPE 05a — Reservoir Sampling
# ─────────────────────────────────────────────
def _step_05a():
    st.markdown(
        """
    <div class="step-content">
        <div class="step-header">
            <span class="step-num-badge">Étape 05a</span>
            <span class="step-title-big">Reservoir Sampling — Échantillonnage aléatoire</span>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class="hbanner">
    La base <strong>UniProtKB/Swiss-Prot</strong> contient <strong>574 627</strong> séquences protéiques annotées manuellement et de haute qualité. 
    Cette étape sélectionne aléatoirement <strong>70 000 séquences</strong> pour constituer la base du dataset négatif, 
    tout en garantissant la reproductibilité et l'absence de biais.
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🎯 Source : UniProtKB/Swiss-Prot**")
        st.markdown(
            """
            - **574 627** entrées protéiques
            - Annotation **manuelle** par des experts
            - Non‑redondant par construction
            - Haute qualité et traçabilité
            """
        )
        if st.button(
            "📖 Architecture UniProt", key="btn_uniprot_arch", type="secondary"
        ):
            st.session_state.show_uniprot_arch = not st.session_state.show_uniprot_arch
            st.rerun()

        if st.session_state.show_uniprot_arch:
            st.markdown(
                """
            <div class="def-box">
                <div class="def-title">🏛️ Architecture d'UniProt</div>
                <p>UniProt est produit par un consortium de trois institutions : <strong>SIB, EBI, PIR</strong>.</p>
                <p><strong>UniProtKB</strong> se divise en deux sections :</p>
                <ul>
                    <li><strong>Swiss-Prot (Reviewed)</strong> : annotée manuellement, non redondante, haute confiance → utilisée ici.</li>
                    <li><strong>TrEMBL (Unreviewed)</strong> : annotation automatique, volumineuse, peut contenir des erreurs.</li>
                </ul>
                <p>Chaque entrée Swiss-Prot contient : identifiant, accession, fonction, taxonomie, références, séquence.</p>
            </div>
            """,
                unsafe_allow_html=True,
            )
    with col2:
        st.markdown("**⚙️ Algorithme : Reservoir Sampling**")
        st.markdown(
            """
            - Parcourt le fichier **une seule fois**
            - Maintient un réservoir de taille **k = 70 000**
            - Remplace aléatoirement des éléments au fil de la lecture
            - **Mémoire constante** O(k)
            - Reproductible via `RANDOM_SEED = 42`
            """
        )
        st.markdown(
            '<div class="justif-tag">📚 <strong>Pourquoi 70 000 ?</strong> Swiss-Prot est non‑redondante. 70 000 séquences offrent une marge pour absorber les pertes des filtres suivants tout en restant représentative.</div>',
            unsafe_allow_html=True,
        )

    st.markdown("**📊 Statistiques d'échantillonnage**")
    st.markdown(
        '<div class="metrics-row">'
        '<div class="metric-card"><div class="mc-val">574 627</div><div class="mc-lbl">Séquences Swiss-Prot</div></div>'
        '<div class="metric-card green"><div class="mc-val">70 000</div><div class="mc-lbl">Séquences échantillonnées</div></div>'
        '<div class="metric-card light"><div class="mc-val">360.7 aa</div><div class="mc-lbl">Longueur moyenne</div></div>'
        '<div class="metric-card amber"><div class="mc-val">1 575</div><div class="mc-lbl">&lt; 50 aa (gardées)</div></div>'
        "</div>",
        unsafe_allow_html=True,
    )

    st.success(
        "**✅ Résultat :** Fichier `negative_raw_sample.fasta` — 70 000 séquences prêtes pour la déduplication."
    )
    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ÉTAPE 05b — CD-HIT 90%
# ─────────────────────────────────────────────
def _step_05b():
    st.markdown(
        """
    <div class="step-content">
        <div class="step-header">
            <span class="step-num-badge">Étape 05b</span>
            <span class="step-title-big">CD-HIT 90% — Suppression de la redondance</span>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class="hbanner">
    Même dans Swiss-Prot, certaines protéines très proches (orthologues, isoformes) peuvent partager plus de 90% d'identité. 
    Si on les garde toutes, le modèle <strong>apprend des patterns redondants</strong> et surestime ses performances. 
    CD-HIT regroupe les séquences similaires et ne conserve qu'un représentant par cluster.
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🎯 Pourquoi 90% ?**")
        st.markdown(
            """
            - Seuil standard dans la littérature AMR
            - Conserve la diversité biologique réelle
            - Élimine les variants quasi‑identiques
            - Deux séquences à 89% peuvent avoir des profils de résistance différents
            """
        )
    with col2:
        st.markdown("**📊 Résultat**")
        st.markdown(
            '<div class="metrics-row" style="margin-top:0">'
            '<div class="metric-card"><div class="mc-val">70 000</div><div class="mc-lbl">Entrée</div></div>'
            '<div class="metric-card green"><div class="mc-val">58 171</div><div class="mc-lbl">Sortie</div></div>'
            '<div class="metric-card red"><div class="mc-val">11 829</div><div class="mc-lbl">Supprimées</div></div>'
            '<div class="metric-card light"><div class="mc-val">~17%</div><div class="mc-lbl">Réduction</div></div>'
            "</div>",
            unsafe_allow_html=True,
        )

    # Algorithme CD-HIT
    btn_algo = (
        "🔼 Masquer l'algorithme"
        if st.session_state.show_cdhit_algo_neg
        else "🔍 Voir le fonctionnement interne de CD-HIT ▼"
    )
    if st.button(btn_algo, key="btn_cdhit_algo_neg", type="secondary"):
        st.session_state.show_cdhit_algo_neg = not st.session_state.show_cdhit_algo_neg
        st.rerun()

    if st.session_state.show_cdhit_algo_neg:
        st.markdown(
            """
        <div class="def-box">
            <div class="def-title">🧩 CD-HIT — Fonctionnement interne</div>
            <p><strong>1. Tri par longueur décroissante</strong> : la plus longue séquence devient représentante.</p>
            <p><strong>2. Filtre par k-mers</strong> : comparaison rapide via des mots de 5 acides aminés (paramètre -n 5).</p>
            <p><strong>3. Alignement local</strong> : calcul de l'identité entre séquences ayant passé le filtre.</p>
            <p><strong>4. Clustering</strong> : si identité ≥ seuil, la séquence rejoint le cluster ; sinon, nouveau cluster.</p>
            <p><strong>5. Mode précis (-g 1)</strong> : assignation au cluster le plus similaire, plus lent mais plus cohérent.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("**⚙️ Paramètres d'exécution**")
    st.markdown(
        """
    <table class="param-table">
        <tr class="param-row"><td>-c 0.90</td><td>Seuil d'identité : 90%</td></tr>
        <tr class="param-row"><td>-n 5</td><td>Taille des k-mers (standard pour ≥90%)</td></tr>
        <tr class="param-row"><td>-g 1</td><td>Mode précis — meilleure qualité biologique</td></tr>
        <tr class="param-row"><td>-M 8000</td><td>Mémoire maximale allouée (MB)</td></tr>
        <tr class="param-row"><td>-T 0</td><td>Utilise tous les cœurs CPU disponibles</td></tr>
    </table>
    """,
        unsafe_allow_html=True,
    )

    st.success(
        "**✅ Résultat :** `negative_cdhit90_repr.fasta` — 58 171 séquences non redondantes."
    )
    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ÉTAPE 05c — DIAMOND
# ─────────────────────────────────────────────
def _step_05c():
    st.markdown(
        """
    <div class="step-content">
        <div class="step-header">
            <span class="step-num-badge">Étape 05c</span>
            <span class="step-title-big">DIAMOND — Filtre d'homologie ARG</span>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class="hbanner">
    <strong>⚠️ Étape la plus critique.</strong> DIAMOND compare chaque séquence négative à une base de <strong>27 022 ARG positifs</strong> 
    (issus de CARD). Toute séquence présentant une similarité significative est exclue. Cela évite les <strong>faux négatifs</strong> 
    (protéines qui ressemblent à des ARG sans en être).
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🎯 Principe**")
        st.markdown(
            """
            - Alignement local ultra‑rapide (seed‑and‑extend)
            - Base ARG pré‑indexée (fichier `.dmnd`)
            - Sortie TSV avec 6 colonnes : `qseqid sseqid pident qcovhsp evalue bitscore`
            """
        )
    with col2:
        st.markdown("**📊 Résultat**")
        st.markdown(
            '<div class="metrics-row" style="margin-top:0">'
            '<div class="metric-card"><div class="mc-val">58 171</div><div class="mc-lbl">Entrée</div></div>'
            '<div class="metric-card green"><div class="mc-val">56 122</div><div class="mc-lbl">Sortie</div></div>'
            '<div class="metric-card red"><div class="mc-val">2 049</div><div class="mc-lbl">Supprimées</div></div>'
            "</div>",
            unsafe_allow_html=True,
        )

    # Paramètres
    btn_params = (
        "🔼 Masquer les paramètres"
        if st.session_state.show_diamond_params
        else "⚙️ Voir les paramètres stricts de DIAMOND ▼"
    )
    if st.button(btn_params, key="btn_diamond_params", type="secondary"):
        st.session_state.show_diamond_params = not st.session_state.show_diamond_params
        st.rerun()

    if st.session_state.show_diamond_params:
        st.markdown(
            """
        <div class="def-box">
            <div class="def-title">🔧 Paramètres de filtrage DIAMOND</div>
            <table class="param-table">
                <tr class="param-row"><td><strong>--id 30.0</strong></td><td>Identité ≥ 30% : seuil strict pour détecter une homologie fonctionnelle.</td></tr>
                <tr class="param-row"><td><strong>--query-cover 80.0</strong></td><td>Couverture ≥ 80% de la séquence requête.</td></tr>
                <tr class="param-row"><td><strong>--evalue 1e-10</strong></td><td>E‑value ≤ 1e-10 : probabilité d'alignement aléatoire infime.</td></tr>
                <tr class="param-row"><td><strong>--sensitive</strong></td><td>Mode sensible plus lent mais plus exhaustif.</td></tr>
                <tr class="param-row"><td><strong>--max-target-seqs 1</strong></td><td>On ne garde que le meilleur hit.</td></tr>
            </table>
            <p class="justif-tag">💡 Ces seuils sont délibérément stricts : même une similarité modérée avec un ARG connu justifie l'exclusion.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.info(
        "**🔬 Logique :** On collecte les `qseqid` des séquences ayant un hit valide → suppression. "
        "Le fichier de sortie `negative_after_diamond.fasta` contient 56 122 séquences."
    )

    st.success(
        "**✅ Résultat :** `negative_after_diamond.fasta` — 56 122 séquences sans similarité avec des ARG connus."
    )
    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ÉTAPE 05d — InterProScan
# ─────────────────────────────────────────────
def _step_05d():
    st.markdown(
        """
    <div class="step-content">
        <div class="step-header">
            <span class="step-num-badge">Étape 05d</span>
            <span class="step-title-big">InterProScan — Détection de domaines de résistance</span>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class="hbanner">
    <strong>Dernier filtre.</strong> Une protéine peut ne pas ressembler globalement à un ARG (passer DIAMOND) 
    mais contenir un <strong>domaine fonctionnel caractéristique</strong> de la résistance (ex : pompe d'efflux MFS). 
    InterProScan détecte ces signatures locales via des modèles HMM.
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🎯 Bases de données intégrées**")
        st.markdown(
            """
            - **Pfam** : modèles HMM de domaines
            - **TIGRFAM** : familles fonctionnelles
            - **PROSITE** : motifs et signatures
            - **PRINTS** : empreintes protéiques
            - **HAMAP** : annotations expertes
            """
        )
        if st.button(
            "📚 Voir les bases de données", key="btn_interpro_dbs", type="secondary"
        ):
            st.session_state.show_interpro_dbs = not st.session_state.show_interpro_dbs
            st.rerun()

        if st.session_state.show_interpro_dbs:
            st.markdown(
                """
            <div class="def-box">
                <div class="def-title">🧩 Détection par modèles HMM</div>
                <p>Chaque domaine protéique est représenté par un modèle de Markov caché (HMM) décrivant la probabilité d'observer certains acides aminés à chaque position.</p>
                <p><strong>Résistance détectée via :</strong></p>
                <ul>
                    <li>Accessions exactes : <code>PF00144</code> (β-lactamase), <code>TIGR01028</code> (tetracycline), ...</li>
                    <li>Mots‑clés : "beta-lactamase", "aminoglycoside", "efflux", ...</li>
                </ul>
            </div>
            """,
                unsafe_allow_html=True,
            )
    with col2:
        st.markdown("**📊 Résultat final**")
        st.markdown(
            '<div class="metrics-row" style="margin-top:0">'
            '<div class="metric-card"><div class="mc-val">56 122</div><div class="mc-lbl">Entrée</div></div>'
            '<div class="metric-card green"><div class="mc-val">56 122</div><div class="mc-lbl">Sortie finale</div></div>'
            '<div class="metric-card light"><div class="mc-val">0</div><div class="mc-lbl">Supprimées</div></div>'
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="justif-tag">📌 <strong>Note :</strong> Sur cet échantillon, aucune séquence n\'a été exclue par InterProScan, validant la qualité du filtrage DIAMOND.</div>',
            unsafe_allow_html=True,
        )

    st.markdown("**⚙️ Architecture asynchrone**")
    st.markdown(
        """
        - Utilisation de `asyncio` + `aiohttp` pour paralléliser les requêtes
        - Batch de 20 séquences, 1 seconde entre chaque batch (respect des limites API EBI)
        - Backoff exponentiel en cas d'erreur (429, 5xx)
        """
    )

    st.success(
        "**✅ Résultat final :** `negative_final.fasta` — 56 122 séquences négatives validées, prêtes pour l'entraînement."
    )
    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Tableau récapitulatif final
# ─────────────────────────────────────────────
def _pipeline_summary_table():
    st.markdown("### 📊 Récapitulatif complet du pipeline")
    import pandas as pd

    df = pd.DataFrame(
        {
            "Étape": ["05a", "05b", "05c", "05d"],
            "Module": [
                "Reservoir Sampling",
                "CD-HIT 90%",
                "DIAMOND BLASTp",
                "InterProScan",
            ],
            "Entrée": ["574 627", "70 000", "58 171", "56 122"],
            "Sortie": ["70 000", "58 171", "56 122", "56 122"],
            "Réduction": ["−504 627", "−11 829", "−2 049", "0"],
            "Fichier clé": [
                "negative_raw_sample.fasta",
                "negative_cdhit90_repr.fasta",
                "negative_after_diamond.fasta",
                "negative_final.fasta",
            ],
            "Statut": ["✅", "✅", "✅", "✅"],
        }
    )
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown(
        """
    <div class="hbanner" style="margin-top: 24px;">
    ✅ <strong>Pipeline de construction du dataset négatif complété.</strong><br>
    <strong>56 122 séquences</strong> de haute qualité, sans redondance, sans similarité avec des ARG connus, 
    et sans domaine de résistance détecté. Dataset prêt pour l'entraînement du modèle de classification.
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
    _inject_neg_pipeline_css()

    # En-tête
    st.markdown(
        '<div class="sh-title">🧬 Construction du Dataset Négatif</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
    <div class="hbanner">
    Ce pipeline construit un dataset négatif <strong>fiable et sans ambiguïté</strong> à partir d'<strong>UniProtKB/Swiss-Prot</strong>.
    L'objectif est de fournir des exemples de protéines <em>non résistantes</em> pour entraîner un modèle capable de distinguer 
    les gènes de résistance aux antibiotiques (ARG) des protéines normales.
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Vue d'ensemble
    _pipeline_overview_block()

    # Sélecteur d'étapes
    st.markdown("### 🔎 Sélectionnez une étape")
    cols = st.columns(4)
    steps = [
        ("05a", "🎲", "Reservoir\nSampling"),
        ("05b", "🧬", "CD-HIT\n90%"),
        ("05c", "⚡", "DIAMOND\nBLASTp"),
        ("05d", "🔬", "InterPro\nScan"),
    ]
    for i, (num, emoji, title) in enumerate(steps):
        with cols[i]:
            is_active = st.session_state.neg_step == num
            if st.button(
                f"{emoji} Étape {num}\n{title}",
                key=f"neg_step_btn_{num}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state.neg_step = None if is_active else num
                # Reset des détails
                for k in [
                    "show_reservoir_detail",
                    "show_cdhit_detail_neg",
                    "show_diamond_detail",
                    "show_interpro_detail",
                    "show_cdhit_algo_neg",
                    "show_diamond_params",
                    "show_interpro_dbs",
                    "show_uniprot_arch",
                ]:
                    st.session_state[k] = False
                st.rerun()

    # Contenu de l'étape sélectionnée
    step = st.session_state.neg_step
    if step == "05a":
        _step_05a()
    elif step == "05b":
        _step_05b()
    elif step == "05c":
        _step_05c()
    elif step == "05d":
        _step_05d()
    else:
        st.markdown(
            '<div style="text-align:center;color:var(--muted);font-size:.84rem;margin:18px 0;padding:20px;'
            'background:#f8fafc;border-radius:14px;border:1px dashed rgba(0,180,216,.2);">'
            "☝️ Cliquez sur une étape ci-dessus pour afficher son contenu détaillé."
            "</div>",
            unsafe_allow_html=True,
        )

    # Tableau récapitulatif
    st.markdown("---")
    _pipeline_summary_table()
