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
            <div><div style="font-size:1.8rem;">⚙️</div><strong style="color:#1a56db;">App. 1</strong><br><small style="color:#64748b;">Mécanismes ARO</small></div>
            <div style="color:#94a3b8; font-size:1.5rem;">+</div>
            <div><div style="font-size:1.8rem;">📋</div><strong style="color:#1a56db;">App. 2</strong><br><small style="color:#64748b;">ATC & Réf. Sci.</small></div>
            <div style="color:#94a3b8; font-size:1.5rem;">+</div>
            <div><div style="font-size:1.8rem;">🧬</div><strong style="color:#1a56db;">App. 3</strong><br><small style="color:#64748b;">Gènes MDR</small></div>
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
            <h4 style="color:#16a34a; margin-top:0;">✅ Résultats App. 1</h4>
            <p style="color:#475569; font-size:0.88rem; margin-bottom:10px;">Classes identifiées (présentes dans ≥ 2 mécanismes) :</p>
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
        st.markdown(
            """
        <div style="background:#fff7ed; border-radius:8px; padding:10px; margin-top:10px; font-size:0.82rem; color:#d97706;">
            ⚠️ <strong>Limite :</strong> Ne classe pas directement bactéricide/bactériostatique — nécessite croisement
        </div>
        """,
            unsafe_allow_html=True,
        )

    with st.expander("📊 Résultats détaillés Approche 1 (heatmap par mécanisme)"):
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
    st.markdown("## 📋 Approche 2 – Références Scientifiques (Matching ATC)")
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
            ⚠️ 21 classes CARD non matchées dans Réf. Sci. (dont Rifamycine, Nitroimidazole, Phosphonic acid)
        </div>
        """,
            unsafe_allow_html=True,
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
            <strong>Instances minimum :</strong> 10 gènes/classe | <strong>n total analysé :</strong> 3530 gènes MDR (seuil ≥ 2)
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
                b in cls for b in ["Penicillin", "Cephalo", "Carba", "Monob", "Rifamy"]
            )
            color = "#1a56db" if is_bactericide else "#64748b"
            st.markdown(
                f'<span style="display:inline-block; background:#eff6ff; color:{color}; padding:3px 10px; border-radius:6px; font-size:0.80rem; font-weight:600; margin:3px;">{cls}</span>',
                unsafe_allow_html=True,
            )
        st.markdown(
            """
        <div style="background:#fff7ed; border-radius:8px; padding:10px; margin-top:10px; font-size:0.82rem; color:#d97706;">
            ⚠️ Score MDR ne préjuge pas de l'activité bactéricide — nécessite croisement
        </div>
        """,
            unsafe_allow_html=True,
        )

    section_divider()

    # Bilan global
    st.markdown("## 📋 Bilan Global de la Démarche Méthodologique")
    bilan = pd.DataFrame(
        {
            "Approche": [
                "App. 1 – Mécanismes ARO",
                "App. 2 – Réf. Scientifique",
                "App. 2 – Réf. ATC",
                "App. 3 – Gènes MDR",
                "LLMs Biologiques",
                "Littérature CMB/CMI",
            ],
            "Apport": [
                "Identification classes avec large spectre de résistance génique dans CARD",
                "Correspondance CARD ↔ nomenclature internationale validée (25 matchées)",
                "Standard pharmaceutique OMS (17 matchées) – Monobactam inclus",
                "Révèle les classes ciblées par les gènes multi-résistants les plus dangereux",
                "Automatisation rapide – classification à la volée pour grandes listes",
                "Référence gold standard – ratio quantitatif objectif (CMB/CMI)",
            ],
            "Limite": [
                "Ne classe pas bactéricide/bactériostatique directement",
                "Certaines classes CARD non référencées (Rifamycine, Nitroimidazole…)",
                "29 classes non matchées dont Rifamycines, Nitroimidazoles",
                "Score MDR ne préjuge pas de l'activité bactéricide",
                "Faux positifs élevés (BioGPT) – discordances sur classes ambiguës",
                "Nécessite consultation manuelle – double activité = complexité",
            ],
        }
    )
    st.dataframe(bilan, use_container_width=True, hide_index=True, height=280)
