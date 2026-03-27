# definitions.py
import streamlit as st
from utils.helpers import section_divider, info_box
from utils.load_data import BACTERICIDAL_CLASSES, BACTERIOSTATIC_CLASSES, DUAL_CLASSES
import pandas as pd


def render():
    st.markdown("# 📖 Définitions & Classification")
    st.markdown(
        '<p style="color:#64748b; font-size:1.05rem; margin-bottom:24px;">Cadre théorique de la classification bactéricide/bactériostatique et listes des classes par activité.</p>',
        unsafe_allow_html=True,
    )

    # Bactéricide vs Bactériostatique
    st.markdown("## ⚗️ Cadre Théorique : Bactéricide vs Bactériostatique")
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown(
            """
        <div class="section-card" style="border-top:4px solid #1a56db; height:100%;">
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
                <div style="background:#eff6ff; border-radius:10px; padding:10px; font-size:1.6rem;">☠️</div>
                <h3 style="margin:0; color:#1a56db;">BACTÉRICIDE</h3>
            </div>
            <p style="color:#475569; line-height:1.8; font-style:italic; margin-bottom:12px;">Détruit les bactéries</p>
            <ul style="color:#475569; line-height:2; margin:0; padding-left:20px;">
                <li>Inhibition de la <strong>synthèse de la paroi bactérienne</strong></li>
                <li>Altération de la <strong>membrane bactérienne</strong></li>
                <li>Inhibition des <strong>enzymes bactériennes essentielles</strong></li>
                <li>Inhibition de la <strong>traduction des protéines</strong></li>
            </ul>
            <div style="background:#eff6ff; border-radius:8px; padding:12px; margin-top:14px;">
                <strong style="color:#1a56db; font-size:0.88rem;">Réduction ≥ 3 log₁₀ UFC/mL par rapport à l'inoculum initial</strong>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
        <div class="section-card" style="border-top:4px solid #64748b; height:100%;">
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
                <div style="background:#f1f5f9; border-radius:10px; padding:10px; font-size:1.6rem;">⏸️</div>
                <h3 style="margin:0; color:#64748b;">BACTÉRIOSTATIQUE</h3>
            </div>
            <p style="color:#475569; line-height:1.8; font-style:italic; margin-bottom:12px;">Inhibe la croissance bactérienne</p>
            <ul style="color:#475569; line-height:2; margin:0; padding-left:20px;">
                <li>Inhibition de la <strong>synthèse des protéines</strong></li>
                <li>Inhibition au niveau du <strong>ribosome 50S</strong></li>
                <li>Liaison au ribosome 50S → <strong>arrêt traduction</strong></li>
                <li>Interférence avec <strong>réplication de l'ADN</strong></li>
            </ul>
            <div style="background:#f1f5f9; border-radius:8px; padding:12px; margin-top:14px;">
                <strong style="color:#64748b; font-size:0.88rem;">La croissance reprend à l'arrêt du traitement — dépend du système immunitaire</strong>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    section_divider()

    # Bactéricides stricts
    st.markdown("## 🏆 Les Classes Bactéricides Strictes")
    st.markdown(
        """
    <div class="section-card" style="background:#eff6ff;">
        <p style="color:#475569; line-height:1.8; margin:0 0 12px 0;">
        Les <strong>bactéricides stricts</strong> sont des antibiotiques qui tuent systématiquement les bactéries,
        indépendamment de la concentration relative et de la phase de croissance bactérienne.
        Leur effet létal est <em>direct et irréversible</em>.
        </p>
        <div style="display:flex; flex-wrap:wrap; gap:8px; margin-top:12px;">
    """,
        unsafe_allow_html=True,
    )
    badges = "".join(
        [f'<span class="badge-validated">✓ {c}</span>' for c in BACTERICIDAL_CLASSES]
    )
    st.markdown(badges + "</div></div>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    for col, (icon, title, desc) in zip(
        [col1, col2, col3, col4],
        [
            (
                "🏥",
                "Infections graves",
                "Utilisés dans les infections graves ou potentiellement mortelles",
            ),
            (
                "🔬",
                "Phase stationnaire",
                "Efficaces contre bactéries en phase de croissance lente",
            ),
            (
                "⚡",
                "Élimination rapide",
                "Permettent une élimination rapide et complète",
            ),
            ("🛡️", "Immunodéprimés", "Cruciaux pour les patients immunodéprimés"),
        ],
    ):
        with col:
            st.markdown(
                f"""
            <div class="section-card" style="text-align:center; background:white;">
                <div style="font-size:1.6rem;">{icon}</div>
                <strong style="color:#1a56db; font-size:0.85rem; display:block; margin:8px 0 6px;">{title}</strong>
                <p style="color:#64748b; font-size:0.8rem; margin:0;">{desc}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        section_divider()

    # ── LLMs ─────────────────────────────────────────────────────
    st.markdown("## 🤖 Tests LLMs Spécialisés – BioGPT & BioMedLM")
    info_box(
        """
    <strong>⚠️ Résultats critiques :</strong> BioGPT présente un <strong>taux élevé de faux positifs</strong>
    (classifie TOUS les antibiotiques comme bactéricides — biais systématique).
    BioMedLM donne des <strong>résultats incohérents</strong> avec confusion entre classes similaires.
    Conclusion : <strong>LLMs biologiques inadaptés seuls</strong> → nécessité de recourir à la littérature.
    """,
        kind="warning",
    )

    tab1, tab2, tab3 = st.tabs(
        ["🔵 BioGPT (Microsoft)", "🟣 BioMedLM (Stanford)", "📊 Bilan Comparatif"]
    )

    with tab1:
        col1, col2 = st.columns([3, 2], gap="large")
        with col1:
            st.markdown(
                """
            <div class="section-card">
                <h4 style="color:#1a56db; margin-top:0;">BioGPT – Description</h4>
                <p style="color:#475569; line-height:1.8;">
                Pré-entraîné sur <strong>millions d'articles PubMed</strong>. Optimisé pour le langage
                biomédical et la génération de réponses factuelles à partir de textes scientifiques.
                </p>
                <div style="background:#fef2f2; border-radius:8px; padding:14px; margin-top:12px; border-left:4px solid #ef4444;">
                    <strong style="color:#dc2626;">⚠️ Résultat obtenu :</strong>
                    <p style="color:#475569; margin:8px 0 0; font-size:0.9rem;">
                    <strong>TAUX ÉLEVÉ DE FAUX POSITIFS</strong> → Classifie TOUS les antibiotiques
                    comme bactéricides (biais systématique). Ce modèle ne distingue pas les classes
                    bactéricides des bactériostatiques de façon fiable.
                    </p>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                """
            <div class="section-card" style="background:#f0fdf4; border:1px solid #bbf7d0;">
                <h4 style="color:#16a34a; margin-top:0;">✅ Avantages</h4>
                <ul style="color:#475569; line-height:1.9; margin:0; padding-left:16px; font-size:0.88rem;">
                    <li>Couverture large (millions PubMed)</li>
                    <li>Rapidité et flexibilité</li>
                    <li>Open source</li>
                </ul>
            </div>
            """,
                unsafe_allow_html=True,
            )
            st.markdown(
                """
            <div class="section-card" style="background:#fef2f2; border:1px solid #fca5a5; margin-top:0;">
                <h4 style="color:#dc2626; margin-top:0;">❌ Limites constatées</h4>
                <ul style="color:#475569; line-height:1.9; margin:0; padding-left:16px; font-size:0.88rem;">
                    <li><strong>Biais systématique</strong> : classe tout bactéricide</li>
                    <li>Hallucinations sur classes rares</li>
                    <li>Pas de distinction fiable</li>
                </ul>
            </div>
            """,
                unsafe_allow_html=True,
            )

    with tab2:
        col1, col2 = st.columns([3, 2], gap="large")
        with col1:
            st.markdown(
                """
            <div class="section-card">
                <h4 style="color:#7c3aed; margin-top:0;">BioMedLM – Description</h4>
                <p style="color:#475569; line-height:1.8;">
                Modèle biomédical dédié (Stanford CRFM), entraîné sur des corpus <strong>médicaux
                et pharmacologiques</strong>. Capable d'extraire et de compléter des informations
                sur les médicaments et antibiotiques.
                </p>
                <div style="background:#fef2f2; border-radius:8px; padding:14px; margin-top:12px; border-left:4px solid #ef4444;">
                    <strong style="color:#dc2626;">⚠️ Résultat obtenu :</strong>
                    <p style="color:#475569; margin:8px 0 0; font-size:0.9rem;">
                    <strong>Résultats incohérents</strong> → Confusion entre classes similaires.
                    Pas de distinction fiable entre bactéricide et bactériostatique.
                    </p>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                """
            <div class="section-card" style="background:#f0fdf4; border:1px solid #bbf7d0;">
                <h4 style="color:#16a34a; margin-top:0;">✅ Avantages</h4>
                <ul style="color:#475569; line-height:1.9; margin:0; padding-left:16px; font-size:0.88rem;">
                    <li>Meilleur raisonnement clinique</li>
                    <li>Mention ratio CMB/CMI</li>
                    <li>Données pharmacologiques</li>
                </ul>
            </div>
            """,
                unsafe_allow_html=True,
            )
            st.markdown(
                """
            <div class="section-card" style="background:#fef2f2; border:1px solid #fca5a5; margin-top:0;">
                <h4 style="color:#dc2626; margin-top:0;">❌ Limites constatées</h4>
                <ul style="color:#475569; line-height:1.9; margin:0; padding-left:16px; font-size:0.88rem;">
                    <li>Résultats incohérents</li>
                    <li>Confusion entre classes similaires</li>
                    <li>Pas de distinction fiable</li>
                </ul>
            </div>
            """,
                unsafe_allow_html=True,
            )

    with tab3:
        st.markdown(
            """
        <div class="section-card" style="background:#fef2f2; border:2px solid #fca5a5;">
            <h4 style="color:#dc2626; margin-top:0;">🔴 Conclusion sur les LLMs biologiques</h4>
            <p style="color:#475569; line-height:1.8; margin-bottom:12px;">
            Les tests de BioGPT et BioMedLM ont mis en évidence des <strong>limitations critiques</strong>
            rendant impossible l'établissement d'une liste définitive par LLM seul :
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        comparison = pd.DataFrame(
            {
                "Modèle": ["BioGPT (Microsoft)", "BioMedLM (Stanford)"],
                "Problème principal": [
                    "Taux élevé de FAUX POSITIFS – classe TOUT bactéricide",
                    "Résultats incohérents – confusion entre classes",
                ],
                "Avantages": [
                    "Couverture large, rapidité",
                    "Raisonnement clinique, données pharma",
                ],
                "Conclusion": ["❌ Inadapté seul", "❌ Inadapté seul"],
            }
        )
        st.dataframe(comparison, use_container_width=True, hide_index=True)

        info_box(
            """
        <strong>→ Solution adoptée :</strong> Les LLMs ont été utilisés comme source initiale de candidats,
        puis chaque classification a été vérifiée par la <strong>littérature biomédicale (ratio CMB/CMI)</strong>
        et les données CARD (approches 1, 2, 3).
        """,
            kind="info",
        )

    section_divider()

    # Ratio CMB/CMI
    st.markdown("## 📐 Critère Quantitatif : Ratio CMB/CMI")
    info_box(
        """
    Le ratio CMB/CMI est le <strong>critère de référence gold standard</strong> pour classer objectivement un antibiotique.
    CMB = Concentration Minimale Bactéricide | CMI = Concentration Minimale Inhibitrice.
    """,
        kind="info",
    )

    col1, col2, col3 = st.columns(3, gap="medium")
    for col, (bg, color, header_color, ratio, label, desc, note) in zip(
        [col1, col2, col3],
        [
            (
                "#fef2f2",
                "#dc2626",
                "#dc2626",
                "CMB/CMI ≤ 4",
                "BACTÉRICIDE",
                "L'antibiotique tue 99,99% de la population bactérienne à une concentration proche de la CMI.",
                "",
            ),
            (
                "#f0fdf4",
                "#16a34a",
                "#16a34a",
                "4 < CMB/CMI < 32",
                "BACTÉRIOSTATIQUE",
                "L'antibiotique inhibe la croissance sans tuer efficacement les bactéries.",
                "",
            ),
            (
                "#eff6ff",
                "#1a56db",
                "#1a56db",
                "CMB/CMI ≥ 32",
                "TOLÉRANCE",
                "Les bactéries sont inhibées par la CMI mais résistent à la bactéricidie malgré des concentrations élevées.",
                "Survient quand un ATB normalement bactéricide perd son effet létal. CMB augmente fortement sans que CMI change.",
            ),
        ],
    ):
        with col:
            st.markdown(
                f"""
            <div class="section-card" style="background:{bg}; border:2px solid {color}; text-align:center;">
                <div style="background:{color}; color:white; font-size:1.1rem; font-weight:700;
                             border-radius:8px; padding:10px; margin-bottom:14px;">{ratio}</div>
                <div style="font-weight:700; color:{color}; font-size:1.1rem; margin-bottom:10px;">{label}</div>
                <p style="color:#475569; font-size:0.88rem; line-height:1.7; margin:0;">{desc}</p>
                {"" if not note else f'<p style="color:#64748b; font-size:0.80rem; font-style:italic; margin-top:10px;">{note}</p>'}
            </div>
            """,
                unsafe_allow_html=True,
            )

    section_divider()

    # Double activité
    st.markdown("## ⚡ Double Activité (Bactéricide et Bactériostatique)")
    col1, col2 = st.columns([2, 3], gap="large")
    with col1:
        st.markdown(
            """
        <div class="section-card" style="border-top:4px solid #0ea5e9;">
            <h4 style="margin-top:0; color:#0369a1;">Classes à double activité</h4>
        </div>
        """,
            unsafe_allow_html=True,
        )
        dual_unique = list(dict.fromkeys(DUAL_CLASSES))
        for cls in dual_unique:
            st.markdown(
                f'<span style="display:inline-block; background:#e0f2fe; color:#0369a1; padding:5px 12px; border-radius:20px; font-size:0.82rem; font-weight:600; margin:3px;">{cls}</span>',
                unsafe_allow_html=True,
            )
    with col2:
        st.markdown(
            """
        <div class="section-card">
            <h4 style="color:#0369a1; margin-top:0;">Définition & Facteurs</h4>
            <p style="color:#475569; line-height:1.8;">
            Un antibiotique à double activité présente à la fois des effets bactéricides et bactériostatiques selon :
            </p>
            <ul style="color:#475569; line-height:1.9; margin:0; padding-left:20px;">
                <li>La <strong>concentration plasmique</strong> de l'antibiotique</li>
                <li>La <strong>durée d'exposition</strong> des bactéries</li>
                <li>La <strong>nature et sensibilité intrinsèque</strong> de la souche bactérienne</li>
            </ul>
            <div style="background:#f0f9ff; border-radius:8px; padding:12px; margin-top:14px; font-size:0.85rem; color:#0369a1;">
                ⚠️ Cette propriété reflète la dépendance de l'effet antibiotique à la pharmacodynamique et aux cibles moléculaires spécifiques de la bactérie.
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    section_divider()

    # Listes des 3 catégories
    st.markdown("## 📋 Classification Complète des Classes Antibiotiques")
    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        st.markdown(
            '<div class="section-card" style="border-top:4px solid #1a56db;"><h4 style="color:#1a56db; margin-top:0;">☠️ Bactéricides Stricts</h4></div>',
            unsafe_allow_html=True,
        )
        for cls in BACTERICIDAL_CLASSES:
            st.markdown(
                f'<span class="badge-bactericide">{cls}</span>', unsafe_allow_html=True
            )
    with col2:
        st.markdown(
            '<div class="section-card" style="border-top:4px solid #64748b;"><h4 style="color:#64748b; margin-top:0;">⏸️ Bactériostatiques</h4></div>',
            unsafe_allow_html=True,
        )
        for cls in BACTERIOSTATIC_CLASSES:
            st.markdown(
                f'<span style="display:inline-block; background:#e2e8f0; color:#475569; padding:4px 12px; border-radius:20px; font-size:0.78rem; font-weight:600; margin:3px;">{cls}</span>',
                unsafe_allow_html=True,
            )
    with col3:
        st.markdown(
            '<div class="section-card" style="border-top:4px solid #0ea5e9;"><h4 style="color:#0ea5e9; margin-top:0;">⚡ Double Activité</h4></div>',
            unsafe_allow_html=True,
        )
        for cls in list(dict.fromkeys(DUAL_CLASSES)):
            st.markdown(
                f'<span style="display:inline-block; background:#e0f2fe; color:#0369a1; padding:4px 12px; border-radius:20px; font-size:0.78rem; font-weight:600; margin:3px;">{cls}</span>',
                unsafe_allow_html=True,
            )

    # Bactéricides stricts référence vs CARD
    section_divider()
    st.markdown("## 🔄 Bactéricides Stricts : Référence vs CARD (slide 14)")
    col1, col2 = st.columns(2, gap="large")
    ref_list = [
        "Pénicillines",
        "Céphalosporines",
        "Carbapénèmes",
        "Quinolones",
        "Glycopeptides",
        "Lipopeptides",
        "Nitroimidazoles",
        "Polymyxines",
        "Phosphonic acid antibiotics",
        "Rifamycines",
        "Monobactam",
    ]
    with col1:
        st.markdown(
            '<div class="section-card" style="border-top:4px solid #64748b;"><h4 style="color:#64748b; margin-top:0;">📚 Bactéricides Stricts (Référence littérature)</h4></div>',
            unsafe_allow_html=True,
        )
        for cls in ref_list:
            st.markdown(
                f'<span style="display:inline-block; background:#f1f5f9; color:#475569; padding:4px 12px; border-radius:20px; font-size:0.82rem; font-weight:600; margin:3px;">• {cls}</span>',
                unsafe_allow_html=True,
            )
    with col2:
        st.markdown(
            '<div class="section-card" style="border-top:4px solid #1a56db;"><h4 style="color:#1a56db; margin-top:0;">🗄️ Bactéricides Stricts (CARD – noms officiels)</h4></div>',
            unsafe_allow_html=True,
        )
        for cls in BACTERICIDAL_CLASSES:
            st.markdown(
                f'<span class="badge-validated">✓ {cls}</span>', unsafe_allow_html=True
            )
