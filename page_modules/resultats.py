import streamlit as st
import pandas as pd
from utils.helpers import section_divider, info_box
from utils.load_data import BACTERICIDAL_CLASSES, get_llm_comparison_data, get_validated_results


def render():
    st.markdown("# ✅ Résultats Finaux")
    st.markdown('<p style="color:#64748b; font-size:1.05rem; margin-bottom:28px;">Synthèse des 8 classes antibiotiques bactéricides strictes validées par croisement des 3 approches et confirmation littérature.</p>', unsafe_allow_html=True)

    # Hero
    st.markdown("""
    <div style="background:linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
                border:2px solid #86efac; border-radius:18px; padding:32px 36px; margin-bottom:28px;">
        <div style="display:flex; align-items:center; gap:14px; margin-bottom:20px;">
            <div style="font-size:2.2rem;">🏆</div>
            <div>
                <h2 style="margin:0; color:#16a34a !important;">8 Classes Bactéricides Strictes Validées dans CARD</h2>
                <p style="margin:4px 0 0; color:#4ade80; font-size:0.9rem;">
                    Croisement 3 approches + littérature CMB/CMI · Ratio CMB/CMI ≤ 4 confirmé
                </p>
            </div>
        </div>
        <div style="display:flex; flex-wrap:wrap; gap:10px;">
    """ + "".join([f'<span class="badge-validated">✓ {c}</span>' for c in BACTERICIDAL_CLASSES]) + """
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("✅ Classes validées", "8", "sur 46 dans CARD")
    with col2:
        st.metric("⭐⭐⭐ Priorité max", "4", "Carb, Ceph, Pen, Glyco")
    with col3:
        st.metric("⭐⭐ Priorité haute", "4", "Nitro, Rifa, Mono, Phospho")
    with col4:
        st.metric("🤖 LLMs validés", "6/8", "par littérature CMB/CMI")

    section_divider()

    # Tableau synthèse des 3 approches (slide 50 exact)
    st.markdown("## 📋 Synthèse des 3 Approches – Tableau de Convergence")
    info_box("""
    <strong>Les trois approches sont complémentaires.</strong> L'intersection de leurs résultats permet 
    d'identifier les classes les plus critiques avec une forte confiance. 
    ✓ = présent | — = non retrouvé (hors référentiel ou score insuffisant)
    """, kind="info")

    df_val = get_validated_results()
    
    def style_check(val):
        if val == "✓":
            return "background-color:#f0fdf4; color:#16a34a; font-weight:700; text-align:center;"
        elif val == "—":
            return "background-color:#f8fafc; color:#94a3b8; text-align:center;"
        elif "★★★" in str(val):
            return "background-color:#fef9c3; color:#ca8a04; font-weight:700;"
        elif "★★" in str(val):
            return "background-color:#eff6ff; color:#1a56db; font-weight:600;"
        return ""

    styled = df_val.style.applymap(style_check, subset=["App.1 ARO", "App.2 Réf.", "App.2 ATC", "App.3 MDR", "Littérature", "Priorité ★"])
    st.dataframe(styled, use_container_width=True, hide_index=True, height=360)

    section_divider()

    # Classes validées par LLM + littérature (slide 20)
    st.markdown("## 🔬 Classes Validées par LLM et Confirmées par Littérature")
    info_box("""
    Ces 6 classes ont été identifiées par les LLMs (malgré leurs biais) et 
    <strong>validées par la littérature via le ratio CMB/CMI</strong>. 
    Source : Ullah & Ali (2017), EUCAST, CLSI, articles cliniques.
    """, kind="success")

    llm_validated = pd.DataFrame({
        "Drug Class (CARD)": ["Aminoglycoside antibiotic", "Carbapenem", "Cephalosporin", "Fluoroquinolone antibiotic", "Glycopeptide antibiotic", "Rifamycin antibiotic"],
        "Molécule": ["Gentamicin", "Meropenem", "Ceftriaxone", "Ciprofloxacin", "Vancomycin", "Rifampicin"],
        "Ratio CMB/CMI": [2.40, 2.58, 0.25, 3.00, 4.00, 3.00],
        "Mécanisme d'action": [
            "Inhibition synthèse protéique + perturbation membrane",
            "Inhibition synthèse paroi (PBPs)",
            "Inhibition synthèse paroi (PBPs)",
            "Inhibition topoisomérase II/IV (ADN gyrase)",
            "Liaison D-Ala-D-Ala → inhibition synthèse paroi",
            "Inhibition ARN polymérase",
        ],
        "Statut": ["⚡ Double activité", "✅ Bactéricide strict", "✅ Bactéricide strict", "⚡ Double activité", "✅ Bactéricide strict", "✅ Bactéricide strict"],
    })
    st.dataframe(llm_validated, use_container_width=True, hide_index=True)

    section_divider()

    # Bactéricides suggérés par LLM mais NON validés (slide 21)
    st.markdown("## ❌ Bactéricides Suggérés par LLM – Non Validés par Littérature")
    info_box("""
    Ces classes ont été classifiées comme bactéricides par les LLMs 
    mais la <strong>littérature les considère bactériostatiques</strong> — illustration du problème de faux positifs.
    """, kind="warning")

    llm_false_pos = pd.DataFrame({
        "Drug Class (CARD)": ["Macrolide antibiotic", "Oxazolidinone antibiotic", "Lincosamide antibiotic", "Phenicol antibiotic", "Streptogramin A antibiotic", "Streptogramin B antibiotic"],
        "Molécule": ["Azithromycin", "Linezolid", "Clindamycin", "Chloramphenicol", "Virginiamycin M", "Quinupristin"],
        "CMB/CMI (LLM)": [2.60, 4.00, 4.00, 4.00, 2.00, 2.50],
        "Mécanisme": ["Inhibition synthèse protéique (50S)", "Inhibition initiation traduction (50S)", "Inhibition synthèse protéique (50S)", "Inhibition synthèse protéique (50S)", "Inhibition synthèse protéique (50S)", "Inhibition synthèse protéique (50S)"],
        "Réalité littérature": ["❌ Bactériostatique", "❌ Bactériostatique", "❌ Bactériostatique", "❌ Bactériostatique", "❌ Bactériostatique", "❌ Bactériostatique"],
    })
    st.dataframe(llm_false_pos, use_container_width=True, hide_index=True)

    section_divider()

    # Comparaison complète LLM vs littérature
    st.markdown("## 🔄 Comparaison Complète : LLM vs Littérature de Référence")
    df_llm = get_llm_comparison_data()
    
    def color_cell(val):
        if "Bactéricide strict" in str(val) or val == "✅":
            return "background-color:#f0fdf4; color:#16a34a; font-weight:600;"
        elif "biais" in str(val) or "Incohérent" in str(val):
            return "background-color:#fef2f2; color:#dc2626; font-weight:600;"
        elif "Double" in str(val) or val == "⚡":
            return "background-color:#e0f2fe; color:#0369a1; font-weight:600;"
        elif "Bactériostatique" in str(val) or val == "❌":
            return "background-color:#f1f5f9; color:#64748b;"
        return ""

    styled_llm = df_llm.style.applymap(color_cell, subset=["BioGPT", "BioMedLM", "Littérature (réf.)", "Validation finale"])
    st.dataframe(styled_llm, use_container_width=True, hide_index=True, height=480)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div style="background:#f0fdf4; border-radius:8px; padding:10px 14px; font-size:0.83rem;">✅ <strong>Bactéricide strict</strong></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div style="background:#e0f2fe; border-radius:8px; padding:10px 14px; font-size:0.83rem;">⚡ <strong>Double activité</strong></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div style="background:#fef2f2; border-radius:8px; padding:10px 14px; font-size:0.83rem;">🔴 <strong>Biais/Incohérent LLM</strong></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div style="background:#f1f5f9; border-radius:8px; padding:10px 14px; font-size:0.83rem;">❌ <strong>Bactériostatique</strong></div>', unsafe_allow_html=True)
