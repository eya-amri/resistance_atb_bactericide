import streamlit as st


def render():
    st.markdown("## 📚 Références Bibliographiques")
    st.markdown(
        '<p style="color:#64748b; font-size:1rem; margin-bottom:28px;">'
        "Sources scientifiques utilisées dans les trois volets du projet : classification, ratio CMB/CMI et validation par les travaux récents en IA ."
        "</p>",
        unsafe_allow_html=True,
    )

    # ─────────────────────────────────────────────
    # Section 1 – Identification des classes bactéricides
    # ─────────────────────────────────────────────
    st.markdown(
        """
        <div style="background:linear-gradient(135deg,#eff6ff,#e0f2fe);
                    border-left:4px solid #1a56db; border-radius:14px;
                    padding:20px 24px; margin-bottom:8px;">
            <div style="font-size:0.72rem; letter-spacing:2.5px; text-transform:uppercase;
                        color:#1a56db; font-weight:700; margin-bottom:6px;">Volet 1</div>
            <div style="font-size:1.2rem; font-weight:800; color:#023e8a; margin-bottom:6px;">
                🔬 Identification des Classes Bactéricides
            </div>
            <div style="font-size:0.88rem; color:#475569; line-height:1.6;">
                Références utilisées pour définir et classifier les antibiotiques bactéricides
                et bactériostatiques ainsi que leurs familles pharmacologiques.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "📖 Voir les références — Classification",
        key="toggle_class",
        use_container_width=False,
    ):
        st.session_state["show_class"] = not st.session_state.get("show_class", False)

    if st.session_state.get("show_class", False):
        refs_class = [
            (
                "1",
                "Ishak A., Mazonakis N., Spernovasilis N., Akinosoglou K., Tsioutis C. (2024)",
                "Bactericidal versus bacteriostatic antibacterials: clinical significance, differences "
                "and synergistic potential in clinical practice. Journal of Antimicrobial Chemotherapy. "
                "https://doi.org/10.1093/jac/dkae380 — Advance Access publication 29 October 2024.",
            ),
            (
                "2",
                "Microbio-infectio 101 (2018)",
                "Familles d'Antibiotiques. Document pédagogique enregistré le 08/03/2018. "
                "Synthèse des grandes familles d'ABS et leurs mécanismes d'action.",
            ),
            (
                "3",
                "OpenStax Microbiology (LibreTexts)",
                "Microbiology — OpenStax CNX. "
                "https://bio.libretexts.org/Bookshelves/Microbiology/Microbiology_(OpenStax). "
                "Référence encyclopédique sur les agents antimicrobiens et leur classification.",
            ),
        ]
        _render_ref_list(refs_class)

    st.markdown("<br>", unsafe_allow_html=True)

    # ─────────────────────────────────────────────
    # Section 2 – Ratio CMB/CMI
    # ─────────────────────────────────────────────
    st.markdown(
        """
        <div style="background:linear-gradient(135deg,#f0fdf4,#dcfce7);
                    border-left:4px solid #16a34a; border-radius:14px;
                    padding:20px 24px; margin-bottom:8px;">
            <div style="font-size:0.72rem; letter-spacing:2.5px; text-transform:uppercase;
                        color:#16a34a; font-weight:700; margin-bottom:6px;">Volet 2</div>
            <div style="font-size:1.2rem; font-weight:800; color:#14532d; margin-bottom:6px;">
                🧫 Calcul du Ratio CMB / CMI
            </div>
            <div style="font-size:0.88rem; color:#475569; line-height:1.6;">
                Études expérimentales ayant servi à établir les seuils de ratio CMB/CMI
                et à caractériser l'activité bactéricide <em>in vitro</em> et en biofilm.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "📖 Voir les références — Ratio CMB/CMI",
        key="toggle_ratio",
        use_container_width=False,
    ):
        st.session_state["show_ratio"] = not st.session_state.get("show_ratio", False)

    if st.session_state.get("show_ratio", False):
        refs_ratio = [
            (
                "1",
                "Ogawa Y. & Mii M.",
                "Screening for highly active β-lactam antibiotics against Agrobacterium tumefaciens.",
            ),
            (
                "2",
                "Agarwal G., Kapil A., Kabra S.K., Das B.K., Dwivedi S.N.",
                "In vitro efficacy of ciprofloxacin and gentamicin against a biofilm of "
                "Pseudomonas aeruginosa and its free-living forms.",
            ),
            (
                "3",
                "Khameneh B., Iranshahy M., Ghandadi M., Atashbeyk D.G., Fazly Bazzaz B.S., Iranshahi M.",
                "Investigation of the antibacterial activity and efflux pump inhibitory effect of "
                "co-loaded piperine and gentamicin nanoliposomes in methicillin-resistant "
                "Staphylococcus aureus.",
            ),
            (
                "4",
                "Sandoe J.A.T., Wysome J., West A.P., Heritage J., Wilcox M.H. (2006)",
                "Measurement of ampicillin, vancomycin, linezolid and gentamicin activity against "
                "enterococcal biofilms. Journal of Antimicrobial Chemotherapy, 57, 767–770. "
                "doi:10.1093/jac/dkl013.",
            ),
            (
                "5",
                "Lutsar I., Ahmed A., Friedland I.R., Trujillo M., Wubbel L., Olsen K., McCracken G.H. Jr. (1997)",
                "Pharmacodynamics and bactericidal activity of ceftriaxone therapy in experimental "
                "cephalosporin-resistant pneumococcal meningitis. Antimicrobial Agents and Chemotherapy, "
                "41(11), 2414–2417.",
            ),
        ]
        _render_ref_list(refs_ratio)

    st.markdown("<br>", unsafe_allow_html=True)

    # ─────────────────────────────────────────────
    # Section 3 – Validation par apprentissage automatique
    # ─────────────────────────────────────────────
    st.markdown(
        """
        <div style="background:linear-gradient(135deg,#fff7ed,#fef3c7);
                    border-left:4px solid #f97316; border-radius:14px;
                    padding:20px 24px; margin-bottom:8px;">
            <div style="font-size:0.72rem; letter-spacing:2.5px; text-transform:uppercase;
                        color:#f97316; font-weight:700; margin-bottom:6px;">Volet 3</div>
            <div style="font-size:1.2rem; font-weight:800; color:#78350f; margin-bottom:6px;">
                🤖 Références scientifiques basées sur les travaux de prédiction de la résistance
            </div>
            <div style="font-size:0.88rem; color:#475569; line-height:1.6;">
                Travaux récents en IA et bioinformatique utilisés pour valider et contextualiser
                les approches de prédiction de résistance aux antimicrobiens.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "📖 Voir les références ",
        key="toggle_valid",
        use_container_width=False,
    ):
        st.session_state["show_valid"] = not st.session_state.get("show_valid", False)

    if st.session_state.get("show_valid", False):
        refs_valid = [
            (
                "1",
                "Siddiqui M.S.B. & Tarannum N. (2026)",
                "Fusing sequence motifs and pan-genomic features: Antimicrobial resistance prediction "
                "using an explainable lightweight 1D CNN–XGBoost ensemble. SCAsia & HPC Asia 2026, pp. 374–383.",
            ),
            (
                "2",
                "Bagaria A. (2025)",
                "AMR-MoEGA: Antimicrobial resistance prediction using mixture of experts and genetic "
                "algorithms. arXiv:2511.12223.",
            ),
            (
                "3",
                "Popa S.L. et al. (2022)",
                "Deep learning and antibiotic resistance. Antibiotics, 11(11), 1674.",
            ),
            (
                "4",
                "He L., Li H., Qi R., Zou Q., Wang Y. (2025)",
                "MCT-ARG: Identification and classification of antibiotic resistance genes based on a "
                "multi-channel transformer model. Science of the Total Environment, 1006, 180848.",
            ),
            (
                "5",
                "Ren Y. et al. (2022)",
                "Multi-label classification for multi-drug resistance prediction of Escherichia coli. "
                "Computational and Structural Biotechnology Journal, 20, 1264–1270.",
            ),
            (
                "6",
                "Astudillo C.A. et al. (2024)",
                "Multi-label classification to predict antibiotic resistance from raw clinical MALDI-TOF "
                "mass spectrometry data. Scientific Reports, 14(1), 31283.",
            ),
            (
                "7",
                "Wishal S. & Sahara R. (2026)",
                "Predicting multi-drug resistance in bacterial isolates through performance comparison "
                "and LIME-based interpretation of classification models. arXiv:2602.22400.",
            ),
            (
                "8",
                "Sodagari H.R. et al. (2025)",
                "Machine learning prediction of multidrug resistance in swine-derived Campylobacter spp. "
                "using United States antimicrobial resistance surveillance data (2013–2023). "
                "Veterinary Sciences, 12(10), 937.",
            ),
        ]
        _render_ref_list(refs_valid)

    st.markdown("<br><br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Helper interne : affichage de la liste
# ─────────────────────────────────────────────
def _render_ref_list(refs: list):
    st.markdown(
        '<div style="background:#ffffff; border-radius:12px; padding:8px 20px; '
        'border:1px solid #e2e8f0; margin-top:8px; margin-bottom:4px;">',
        unsafe_allow_html=True,
    )
    for num, author, title in refs:
        st.markdown(
            f"""
            <div style="display:flex; gap:12px; align-items:flex-start;
                        padding:12px 0; border-bottom:1px solid #f1f5f9;">
                <div style="background:#1a56db; color:white; font-weight:700; font-size:0.82rem;
                             border-radius:6px; padding:4px 10px; min-width:28px;
                             text-align:center; flex-shrink:0;">{num}</div>
                <div style="font-size:0.87rem; color:#475569; line-height:1.6;">
                    <strong style="color:#1e293b;">{author}</strong><br>{title}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


# Pour tester le module directement
if __name__ == "__main__":
    st.set_page_config(page_title="Références Bibliographiques", layout="wide")
    render()
