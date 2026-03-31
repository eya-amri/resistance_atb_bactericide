import streamlit as st
import pandas as pd
from utils.helpers import section_divider, info_box
from utils.load_data import get_approche1_results
import os


def render():
    st.markdown("# 🧪 Approches de Validation")
    st.markdown(
        """
        <div class="hbanner">
            Après avoir identifié les classes bactéricides dans CARD, l’objectif est d’en évaluer l’importance biologique et clinique.<br>
            Pour cela, trois approches complémentaires ont été mises en place : analyser la concentration de mécanismes de résistance (Approche 1),
            valider les correspondances avec les références scientifiques et pharmaceutiques (Approche 2), et étudier l’implication des gènes dans la multi-résistance (Approche 3). 
            Cette démarche permet de croiser les sources d’information et de confirmer la pertinence des classes identifiées.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Vue d'ensemble
    st.markdown(
        """
    <div class="section-card" >
        <div style="display:flex; justify-content:space-around; flex-wrap:wrap; gap:16px; text-align:center; align-items:center;">
            <div><div style="font-size:1.8rem;">⚙️</div><strong style="color:#1a56db;">Approche. 1</strong><br><small style="color:#64748b;">Mécanismes de résistance</small></div>
            <div style="color:#94a3b8; font-size:1.5rem;">+</div>
            <div><div style="font-size:1.8rem;">📋</div><strong style="color:#1a56db;">Approche. 2</strong><br><small style="color:#64748b;">ATC & Réf. Sci.</small></div>
            <div style="color:#94a3b8; font-size:1.5rem;">+</div>
            <div><div style="font-size:1.8rem;">🧬</div><strong style="color:#1a56db;">Approche. 3</strong><br><small style="color:#64748b;">Gènes MDR</small></div>
            <div style="color:#94a3b8; font-size:1.5rem;">+</div>
            <div><div style="font-size:1.8rem;">✅</div><strong style="color:#16a34a;">10 Classes</strong><br><small style="color:#64748b;">Validées</small></div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    section_divider()

    # ── Approche 1 ────────────────────────────────────────────────
    st.markdown("## 🔬 Approche 1 – Mécanismes de Résistance (ARO)")
    col1, col2 = st.columns([3, 2], gap="large")
    with col1:
        st.markdown(
            """
        <div class="section-card">
            <h4 style="color:#1a56db; margin-top:0;">Objectif & Principe</h4>
            <p style="color:#475569; line-height:1.8;">
            Cette approche vise à évaluer l'importance des classes d'antibiotiques identifiées dans CARD en fonction des mécanismes de résistance qu'elles concentrent. <br>
            L'idée centrale est que <strong>plus une classe regroupe de mécanismes de résistance, plus elle est biologiquement significative</strong> et potentiellement critique dans le contexte clinique.<br>
            Les mécanismes sont extraits directement du champ <code>ARO_category</code> dans <code>card.json</code> et servent à mesurer la polyvalence et l'impact des classes sur la résistance.
            </p>
            <h5 style="color:#1a56db; margin-bottom:8px;">5 Mécanismes Ciblés (ARO)</h5>
            <ol style="color:#475569; line-height:2; margin:0; padding-left:20px;">
                <li><strong>Antibiotic Inactivation</strong> — 22 Drug Classes</li>
                <li><strong>Antibiotic Target Alteration</strong> — 41 Drug Classes </li>
                <li><strong>Antibiotic Efflux</strong> — 33 Drug Classes </li>
                <li><strong>Antibiotic Target Protection</strong> — 15 Drug Classes</li>
                <li><strong>Antibiotic Target Replacement</strong> — 8 Drug Classes </li>
            </ol>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
        <div class="section-card" style="background:#f0fdf4; border:1px solid #bbf7d0;">
            <h4 style="color:#16a34a; margin-top:0;">✅ Résultats Approche. 1</h4>
            <p style="color:#475569; font-size:0.88rem; margin-bottom:10px;">Classes identifiées :</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
        for cls in get_approche1_results():
            color = "#1a56db" if "Tetracycline" not in cls else "#f97316"
            st.markdown(
                f'<span style="display:inline-block; background:#eff6ff; color:{color}; padding:4px 12px; border-radius:8px; font-size:0.82rem; font-weight:600; margin:3px; border-left:3px solid {color};">{cls}</span>',
                unsafe_allow_html=True,
            )

    # ── Mapping labels lisibles ────────────────────────────────────────
    MECHANISM_LABELS = {
        "Tgt_Alteration": "Target Alteration",
        "Tgt_Protection": "Target Protection",
        "Tgt_Replacement": "Target Replacement",
        "Inactivation": "Inactivation",
        "Efflux": "Efflux",
    }

    def parse_combo_title(fname: str) -> str:
        """
        combo_Efflux_Tgt_Protection.png  →  Efflux | Target Protection
        combo_Inactivation_Tgt_Alteration_Efflux.png  →  Inactivation | Target Alteration | Efflux
        """
        name = fname.replace("combo_", "").replace(".png", "")
        for key, label in MECHANISM_LABELS.items():
            name = name.replace(key, label.replace(" ", "§"))
        parts = [p.replace("§", " ") for p in name.split("_") if p]
        return " | ".join(parts)

    def show_level(folder: str, description: str):
        base = f"assets/card/app1/{folder}"

        st.markdown(f"_{description}_")
        st.divider()

        # ── Heatmap ───────────────────────────────────────────────────
        st.markdown("### 🗺️ Heatmap globale")
        # Expander pour la définition

        st.markdown(
            """
                Les heatmaps illustrent la fréquence ou le nombre de gènes partagés entre plusieurs mécanismes 
                et classes d’antibiotiques.  
                Elle permet de repérer les combinaisons les plus courantes de mécanismes et de classes, 
                donnant une vue globale des co-occurrences et interactions entre résistances.
                """
        )
        heatmap_path = f"{base}/heatmap_summary_{folder}.png"
        if os.path.exists(heatmap_path):
            st.image(heatmap_path, use_container_width=True)
        else:
            st.warning(f"Heatmap introuvable : `{heatmap_path}`")

        st.divider()

        # ── Combos ────────────────────────────────────────────────────
        combo_files = sorted(
            [
                f
                for f in os.listdir(base)
                if f.startswith("combo_") and f.endswith(".png")
            ]
        )

        if combo_files:
            st.markdown(f"### 📊 Combinaisons — {len(combo_files)} au total")
            st.markdown(
                """
                    Ces images illustrent les gènes partagés entre plusieurs mécanismes et classes d’antibiotiques.  
                    Elles permettent de repérer les combinaisons les plus courantes et les interactions entre résistances.
                    """
            )
            for fname in combo_files:
                label = parse_combo_title(fname)  # ← ici le fix
                st.markdown(f"#### 🔬 {label}")
                st.image(f"{base}/{fname}", use_container_width=True)
                st.markdown("")

        # ── Non commune ──────────────────────────────
        nc_path = f"{base}/non_commune_{folder}.png"
        if os.path.exists(nc_path):
            st.markdown("### 📌 Classes non communes")
            st.markdown(
                """
                    Ces images mettent en évidence les classes d’antibiotiques rares ou spécifiques à certains mécanismes.  
                    Elles permettent d’identifier les résistances uniques ou moins fréquentes.
                    """
            )
            st.image(nc_path, use_container_width=True)
        else:
            st.warning(f"image introuvable : `{nc_path}`")
        st.divider()

    with st.expander("📊 Résultats détaillés Approche 1"):

        tab_n2, tab_n3, tab_n4, tab_n5 = st.tabs(
            [
                "🔵 N=2",
                "🟡 N=3",
                "🟠 N=4",
                "🔴 N=5",
            ]
        )

        with tab_n2:
            show_level(
                "n2",
                "Classes partageant **2 mécanismes de résistance** communs dans CARD.",
            )

        with tab_n3:
            show_level(
                "n3",
                "Les beta-lactamines commencent à dominer à **3 mécanismes** communs.",
            )

        with tab_n4:
            show_level(
                "n4",
                "À **4 mécanismes**, Cephalosporin, Penicillin, Carbapenem et Monobactam "
                "dominent toutes les intersections.",
            )

        with tab_n5:
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("💊 Fluoroquinolone", "303 gènes")
            col_b.metric("💊 Tetracycline", "181 gènes")
            col_c.metric("💊 Rifamycin", "63 gènes")
            st.divider()
            show_level(
                "n5",
                "À **N=5** (tous les mécanismes), seulement **3 classes** persistent.",
            )
        st.markdown(
            """
        <div class="section-card">
        <p style="color:#475569;">Les heatmaps N=2, N=3, N=4 et N=5 mécanismes montrent que
        <strong>Cephalosporin, Penicillin beta-lactam, Carbapenem, Monobactam</strong>
        dominent systématiquement toutes les intersections — confirmant leur importance dans CARD.</p>
        <p style="color:#475569;">À N=5 mécanismes (tous) : seulement 3 classes persistent —
        <strong>Fluoroquinolone (303 gènes)</strong>, Tetracycline (181), Rifamycin (63).</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    section_divider()

    # ── Approche 2 ────────────────────────────────────────────────
    st.markdown("## 📋 Approche 2 – Références Scientifiques")
    col1, col2 = st.columns([3, 2], gap="large")
    with col1:
        st.markdown(
            """
        <div class="section-card">
            <h4 style="color:#1a56db; margin-top:0;">Logique : Matching Multi-Niveaux</h4>
            <p style="color:#475569; line-height:1.8;">
            Cette approche confronte les Drug Classes de CARD avec deux référentiels de classification
            pharmaceutique internationaux via un <strong>algorithme de matching à 2 niveaux</strong>
            (RapidFuzz, seuil=80).
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:12px;">
                <div style="background:#eff6ff; border-radius:8px; padding:12px;">
                    <strong style="color:#1a56db; font-size:0.88rem;">Référence Scientifique (41 classes)</strong>
                    <p style="color:#475569; font-size:0.82rem; margin:6px 0 0;">Littérature microbiologique — 25 classes matchées CARD</p>
                </div>
                <div style="background:#eff6ff; border-radius:8px; padding:12px;">
                    <strong style="color:#1a56db; font-size:0.88rem;">Référence ATC OMS (17 classes)</strong>
                    <p style="color:#475569; font-size:0.82rem; margin:6px 0 0;">Standard pharmaceutique international — 17 classes matchées CARD</p>
                </div>
            </div>
             <p style="color:#475569; line-height:1.8;">
            Pour renforcer la fiabilité des classes retenues, un <strong>seuil minimal de 40 gènes par classe</strong> a été appliqué. 
            Ce seuil garantit que seules les classes associées à un nombre suffisant de gènes de résistance dans CARD sont considérées, 
            évitant ainsi de retenir des classes trop rares ou peu représentatives qui pourraient biaiser les analyses.
            </p>
            <h5 style="color:#1a56db; margin:14px 0 8px;">Pipeline de Matching :</h5>
            <ol style="color:#475569; line-height:2; margin:0; padding-left:20px; font-size:0.9rem;">
                <li><strong>Normalisation</strong> — ASCII, minuscules, suppression "antibiotic"</li>
                <li><strong>Matching par Inclusion</strong> — vérifie si terme contenu dans DC CARD</li>
                <li><strong>Matching Fuzzy (RapidFuzz)</strong> — seuil confiance = 80/100</li>
            </ol>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
        <div class="section-card">
            <h4 style="color:#1a56db; margin-top:0;">📊 Résultats (Top classes matchées)</h4>
        </div>
        """,
            unsafe_allow_html=True,
        )
        top_matched = [
            ("Cephalosporin", 3404),
            ("Penicillin beta-lactam", 3115),
            ("Carbapenem", 2572),
            ("Monobactam", 1310),
            ("Fluoroquinolone antibiotic", 307),
            ("Aminoglycoside antibiotic", 303),
            ("Glycopeptide antibiotic", 103),
            ("Rifamycin antibiotic", 63),
        ]

        for cls, genes in top_matched:
            pct = int(genes / 3404 * 100)
            st.markdown(
                f"""
            <div style="margin-bottom:8px;">
                <div style="display:flex; justify-content:space-between; font-size:0.82rem; color:#475569; margin-bottom:3px;">
                    <span>{cls}</span><span><strong>{genes}</strong> gènes</span>
                </div>
                <div style="background:#e2e8f0; border-radius:4px; height:6px;">
                    <div style="background:#1a56db; width:{pct}%; height:100%; border-radius:4px;"></div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        st.markdown(
            """
            <div style="background:#fff7ed; border-radius:8px; padding:10px; margin-top:10px; font-size:0.82rem; color:#d97706;">
                ⚠️ La classe "phosphonic acid antibiotic" présente 48 gènes dans la base et possède une activité bactéricide, mais elle n’est pas rapportée dans les références scientifiques utilisées pour les travaux de prédiction de la résistance aux antibiotiques.
            </div>
            """,
            unsafe_allow_html=True,
        )
    with st.expander("📊 Résultats détaillés Approche 2"):
        st.markdown("### 📍 Drug Classes matchées avec Références Scientifiques")
        st.image(
            "assets/card/fig1_DC_CARD_matchees_ref_scientifique.png",
            use_container_width=True,
        )
        st.markdown("### 📍 Drug Classes NON matchées avec Références Scientifiques")
        st.image(
            "assets/card/fig2_DC_CARD_non_matchees_ref_scientifique.png",
            use_container_width=True,
        )

    section_divider()

    # ── Approche 3 ────────────────────────────────────────────────
    st.markdown("## 🧬 Approche 3 – Gènes Multi-Résistants (MDR)")
    col1, col2 = st.columns([3, 2], gap="large")
    with col1:
        st.markdown(
            """
        <div class="section-card">
            <h4 style="color:#1a56db; margin-top:0;">Concept du Score MDR</h4>
            <div style="background:#eff6ff; border-radius:10px; padding:14px; margin-bottom:14px; text-align:center;">
                <strong style="color:#1a56db;">Score MDR = Nombre de Drug Classes distinctes associées à ce gène dans CARD</strong><br>
                <span style="color:#475569; font-size:0.85rem;">Un gène avec Score MDR élevé = gène de multi-résistance ciblant plusieurs familles simultanément</span>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="section-card" style="background:linear-gradient(135deg, #e6f2ff 0%, #cceaff 100%); border-radius:12px; padding:16px; margin-top:12px;">
                <h4 style="color:#1a56db; margin-top:0;">Interprétation et intérêt biologique</h4>
                <p style="color:#475569; line-height:1.8;">
                Cette approche permet d’identifier les gènes les plus critiques dans la résistance aux antibiotiques en se basant sur leur capacité à cibler plusieurs classes simultanément. 
                <strong>Plus le score MDR est élevé, plus le gène est associé à un large spectre de résistance</strong>, ce qui en fait un indicateur clé de multi-résistance bactérienne.
                </p>
                <p style="color:#475569; line-height:1.8;">
                L’analyse repose sur <strong>3530 gènes MDR</strong> (avec un seuil ≥ 2 classes), ce qui permet de se concentrer uniquement sur les gènes réellement impliqués dans des phénomènes de résistance multiples, 
                tout en excluant les cas isolés ou peu significatifs.
                </p>
                <p style="color:#475569; line-height:1.8;">
                Cette approche met ainsi en évidence les classes d’antibiotiques les plus souvent ciblées par les gènes multi-résistants, 
                permettant de <strong>prioriser les familles critiques</strong> dans CARD et d’identifier les combinaisons de résistance les plus préoccupantes en contexte clinique.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with st.expander("Pipeline d'extraction MDR "):
        st.image(
            "assets/card/Pipeline d'extraction MDR pour ARO.png",
            use_container_width=True,
        )
    with col2:
        st.markdown(
            """
        <div class="section-card" style="background:#f0fdf4; border:1px solid #bbf7d0;">
            <h4 style="color:#16a34a; margin-top:0;">TOP genes (score=13)</h4>
            <p style="color:#475569; font-size:0.85rem; margin-bottom:10px;">Classes présentes dans les gènes au score maximal :</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
        top_mdr = [
            "Penicillin beta-lactam",
            "Cephalosporin",
            "Carbapenem",
            "Monobactam",
            "Macrolide antibiotic",
            "Fluoroquinolone",
            "Tetracycline",
            "Rifamycin antibiotic",
        ]
        for cls in top_mdr:
            is_bactericide = any(
                b in cls
                for b in [
                    "Penicillin",
                    "Cephalo",
                    "Carba",
                    "Monob",
                    "Rifamy",
                    "Fluoroquinolone",
                ]
            )
            color = "#1a56db" if is_bactericide else "#64748b"
            st.markdown(
                f'<span style="display:inline-block; background:#eff6ff; color:{color}; padding:3px 10px; border-radius:6px; font-size:0.80rem; font-weight:600; margin:3px;">{cls}</span>',
                unsafe_allow_html=True,
            )
        # ── Légende ──
        st.markdown(
            """
            <div style="margin-top:5px; font-size:0.75rem; color:#475569;">
                <span style="display:inline-block; width:12px; height:12px; background:#1a56db; margin-right:4px; vertical-align:middle;"></span>Bactéricide
                <span style="display:inline-block; width:12px; height:12px; background:#64748b; margin:0 4px 0 12px; vertical-align:middle;"></span>Non-bactéricide
            </div>
            """,
            unsafe_allow_html=True,
        )

    with st.expander("📊 Résultats détaillés Approche 3"):
        st.image(
            "assets/card/figB_seuil2_TOP_CARD_general.png",
            use_container_width=True,
        )
