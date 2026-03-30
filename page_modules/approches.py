import streamlit as st
import pandas as pd
from utils.helpers import section_divider, info_box
from utils.load_data import get_approche1_results


def render():
    st.markdown("# 🧪 Approches de Validation")
    st.markdown(
        '<p style="color:#64748b; font-size:1.05rem; margin-bottom:28px;">Trois approches complémentaires développées pour identifier les classes bactéricides dans CARD, validées par la littérature et les LLMs.</p>',
        unsafe_allow_html=True,
    )

    # Vue d'ensemble
    st.markdown(
        """
    <div class="section-card" style="background:linear-gradient(135deg, #eff6ff 0%, #e0f2fe 100%);">
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
            L'idée centrale : <strong>une classe d'antibiotiques est d'autant plus importante
            qu'elle concentre plusieurs mécanismes de résistance dans CARD</strong>.
            Les mécanismes sont extraits directement du champ <code>ARO_category</code> dans <code>card.json</code>.
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

    with st.expander("📊 Résultats détaillés Approche 1 "):
        st.markdown(
            "Heatmap des mécanismes de résistance communs (≥ 2) entre classes d’antibiotiques"
        )
        st.image(
            "assets/card/heatmap_summary_n2.png",
            use_container_width=True,
        )
        st.markdown("Combinaisons des mécanismes de résistance majeurs")
        st.image(
            "assets/card/combo_Inactivation_Tgt_Alteration_Efflux_Tgt_Protection.png",
            use_container_width=True,
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
            (RapidFuzz, seuil=80).<br>Un seuil minimal de 40 gènes par classe matchée est appliqué pour garantir la robustesse des résultats.
            </p>
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
            <p style="color:#475569; line-height:1.8; margin-bottom:10px;">
            <strong>Pipeline d'extraction MDR :</strong> Chaque gène ARO → liste Drug Classes + mécanismes → calcul Score MDR → filtrage seuils 2 et 3 → identification TOP genes (score maximum = <strong>13</strong> dans CARD)
            </p>
            <p style="color:#475569; line-height:1.8; margin:0;">
            <strong>Nombre total de gènes analysé :</strong> 3530 gènes MDR (seuil ≥ 2)
            </p>
        </div>
        """,
            unsafe_allow_html=True,
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
    with st.expander("📊 Résultats détaillés Approche 3"):
        st.image(
            "assets/card/figB_seuil2_TOP_CARD_general.png",
            use_container_width=True,
        )
