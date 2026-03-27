import streamlit as st
from utils.helpers import section_divider, info_box


def render():
    st.markdown("# 💬 Discussion & Conclusions")
    st.markdown('<p style="color:#64748b; font-size:1.05rem; margin-bottom:28px;">Analyse critique des résultats, discordances LLM, bilan méthodologique et perspectives.</p>', unsafe_allow_html=True)

    # LLM limitations (slide 17 & 48)
    st.markdown("## 🤖 Limites des LLMs Biologiques")
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("""
        <div class="section-card" style="border-top:4px solid #ef4444;">
            <h4 style="color:#ef4444; margin-top:0;">🔴 BioGPT – Biais Systématique</h4>
            <p style="color:#475569; line-height:1.8;">
            BioGPT présente un <strong>taux élevé de faux positifs</strong> : il classifie
            <em>TOUS</em> les antibiotiques comme bactéricides, sans distinction.
            Ce biais systématique le rend inutilisable seul pour cette tâche.
            </p>
            <div style="background:#fef2f2; border-radius:8px; padding:12px; margin-top:12px;">
                <strong style="color:#dc2626; font-size:0.88rem;">Conséquence :</strong>
                <p style="color:#475569; font-size:0.85rem; margin:6px 0 0;">
                Impossible de distinguer les 8 classes bactéricides strictes des 9 bactériostatiques.
                Toutes reçoivent la même étiquette "bactéricide".
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="section-card" style="border-top:4px solid #f59e0b;">
            <h4 style="color:#f59e0b; margin-top:0;">🟡 BioMedLM – Résultats Incohérents</h4>
            <p style="color:#475569; line-height:1.8;">
            BioMedLM produit des <strong>résultats incohérents</strong> : confusion entre classes
            similaires, pas de distinction fiable bactéricide/bactériostatique.
            </p>
            <div style="background:#fffbeb; border-radius:8px; padding:12px; margin-top:12px;">
                <strong style="color:#d97706; font-size:0.88rem;">Conséquence :</strong>
                <p style="color:#475569; font-size:0.85rem; margin:6px 0 0;">
                Confusion notable sur Oxazolidinones, Macrolides, Streptogramines —
                classes correctement identifiées comme bactériostatiques dans la littérature.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    info_box("""
    <strong>Conclusion LLMs :</strong> Les LLMs biologiques sont <strong>inadaptés utilisés seuls</strong>
    pour cette classification. Ils peuvent suggérer des candidats initiaux mais nécessitent
    une validation obligatoire par la littérature (ratio CMB/CMI) et les données CARD.
    """, kind="warning")

    section_divider()

    # Discordances (slide 48)
    st.markdown("## ⚠️ Classes Discordantes – Analyse Détaillée")
    st.markdown("Certaines classes présentent des discordances entre les prédictions LLM et les références scientifiques.")

    discordant = [
        {
            "name": "Oxazolidinones", "icon": "🔴",
            "llm": "Bactéricide (BioGPT & BioMedLM)",
            "lit": "Bactériostatique / Double activité",
            "expl": "Linézolide = bactériostatique sur staph/entérocoques mais bactéricide sur certains streptocoques selon concentration.",
            "decision": "❌ Exclu – Bactériostatique retenu",
        },
        {
            "name": "Macrolides", "icon": "🔴",
            "llm": "Variable / Bactéricide (biais BioGPT)",
            "lit": "Bactériostatique (classique)",
            "expl": "Azithromycine peut être bactéricide à concentrations élevées — dépendance concentration. La littérature classe les macrolides bactériostatiques en conditions standards.",
            "decision": "❌ Exclu – Bactériostatique retenu",
        },
        {
            "name": "Fluoroquinolones", "icon": "🟡",
            "llm": "Bactéricide (BioGPT)",
            "lit": "Double activité – bactéricide concentration-dépendant",
            "expl": "Bactéricide concentration-dépendant via inhibition des topoisomérases I et II — consensus sur double activité selon dose et espèce cible.",
            "decision": "⚡ Double activité – Classification contextuelle",
        },
        {
            "name": "Aminoglycosides", "icon": "🟡",
            "llm": "Bactéricide (BioGPT & BioMedLM)",
            "lit": "Double activité – bactéricide à fortes doses",
            "expl": "Bactéricide à fortes doses (modèle CMB/CMI ≤ 4), bactériostatique à faibles doses. Inactifs en conditions anaérobies — activité dose-dépendante.",
            "decision": "⚡ Double activité retenu",
        },
    ]

    for item in discordant:
        with st.expander(f"{item['icon']} {item['name']} – Discordance LLM vs Littérature"):
            col1, col2 = st.columns(2, gap="large")
            with col1:
                st.markdown(f"""
                <div class="section-card" style="background:#fef2f2; border:1px solid #fca5a5;">
                    <h5 style="margin-top:0; color:#dc2626;">Prédiction LLMs</h5>
                    <p style="color:#dc2626; font-size:0.9rem; font-weight:600; margin:0;">{item['llm']}</p>
                    <br>
                    <h5 style="margin-top:0; color:#16a34a;">Consensus Littérature</h5>
                    <p style="color:#16a34a; font-size:0.9rem; font-weight:600; margin:0;">{item['lit']}</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="section-card">
                    <h5 style="margin-top:0; color:#1a56db;">Explication de la discordance</h5>
                    <p style="color:#475569; font-size:0.88rem; line-height:1.7;">{item['expl']}</p>
                    <div style="background:#f0fdf4; border-radius:8px; padding:10px; margin-top:10px;">
                        <strong style="font-size:0.85rem;">Décision finale : </strong>
                        <span style="font-size:0.85rem;">{item['decision']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    section_divider()

    # Bilan méthodologique
    st.markdown("## 📊 Bilan Global de la Démarche")
    st.markdown("""
    <div class="section-card">
        <table style="width:100%; border-collapse:collapse; font-size:0.88rem;">
            <thead>
                <tr style="background:#1a56db; color:white;">
                    <th style="padding:10px 14px; text-align:left; border-radius:0;">Approche</th>
                    <th style="padding:10px 14px; text-align:left;">✅ Apport</th>
                    <th style="padding:10px 14px; text-align:left;">⚠️ Limite</th>
                </tr>
            </thead>
            <tbody>
                <tr style="background:#f8fafc;">
                    <td style="padding:10px 14px; font-weight:600; color:#1a56db;">App. 1 – Mécanismes ARO</td>
                    <td style="padding:10px 14px; color:#475569;">Identification des classes avec large spectre de résistance génique dans CARD</td>
                    <td style="padding:10px 14px; color:#d97706;">Ne classe pas bactéricide/bactériostatique directement</td>
                </tr>
                <tr style="background:white;">
                    <td style="padding:10px 14px; font-weight:600; color:#1a56db;">App. 2 – Réf. Scientifique</td>
                    <td style="padding:10px 14px; color:#475569;">Correspondance CARD ↔ nomenclature internationale validée</td>
                    <td style="padding:10px 14px; color:#d97706;">Certaines classes CARD non référencées dans ATC/littérature</td>
                </tr>
                <tr style="background:#f8fafc;">
                    <td style="padding:10px 14px; font-weight:600; color:#1a56db;">App. 3 – Gènes MDR</td>
                    <td style="padding:10px 14px; color:#475569;">Révèle les classes ciblées par les gènes multi-résistants les plus dangereux</td>
                    <td style="padding:10px 14px; color:#d97706;">Score MDR ne préjuge pas de l'activité bactéricide</td>
                </tr>
                <tr style="background:white;">
                    <td style="padding:10px 14px; font-weight:600; color:#dc2626;">LLMs Biologiques</td>
                    <td style="padding:10px 14px; color:#475569;">Automatisation rapide — classification à la volée pour grandes listes</td>
                    <td style="padding:10px 14px; color:#d97706;">Faux positifs élevés (BioGPT) — discordances sur classes ambiguës</td>
                </tr>
                <tr style="background:#f8fafc;">
                    <td style="padding:10px 14px; font-weight:600; color:#16a34a;">Littérature CMB/CMI</td>
                    <td style="padding:10px 14px; color:#475569;">Référence gold standard — ratio quantitatif objectif</td>
                    <td style="padding:10px 14px; color:#d97706;">Nécessite consultation manuelle — double activité = complexité</td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

    section_divider()

    # Perspectives (slide 52)
    st.markdown("## 🚀 Perspectives & Travaux Futurs")
    col1, col2 = st.columns(2, gap="medium")
    futures = [
        ("🔬", "Validation expérimentale", "#eff6ff", "#1a56db",
         "Affiner la liste par validation expérimentale (time-kill curves, CMB mesurées sur souches ATCC standardisées)."),
        ("📊", "Données CMB/CMI réelles (EUCAST/CLSI)", "#eff6ff", "#1a56db",
         "Intégrer des données CMB/CMI réelles issues des bases EUCAST et CLSI dans le pipeline automatisé."),
        ("🤖", "Tester GPT-4, Claude pour classification", "#f5f3ff", "#7c3aed",
         "Tester d'autres LLMs (GPT-4, Claude) pour la classification automatique et comparer aux résultats BioGPT/BioMedLM."),
        ("🔗", "Étendre aux antibiotiques spécifiques", "#f0fdf4", "#16a34a",
         "Étendre aux antibiotiques individuels (pas seulement aux classes) pour une granularité plus fine."),
        ("🌐", "Référentiel CARD enrichi", "#fef9c3", "#ca8a04",
         "Construire un référentiel CARD enrichi avec l'activité bactéricide annotée et proposer une intégration officielle."),
        ("⚙️", "Pipeline automatisé JSON/CSV", "#f0fdf4", "#16a34a",
         "Améliorer le pipeline automatisé avec exports JSON/CSV complets et interface de requête pour chercheurs."),
    ]
    for i, (icon, title, bg, color, desc) in enumerate(futures):
        with col1 if i % 2 == 0 else col2:
            st.markdown(f"""
            <div class="section-card" style="background:{bg}; margin-bottom:12px;">
                <div style="display:flex; align-items:flex-start; gap:12px;">
                    <span style="font-size:1.5rem;">{icon}</span>
                    <div>
                        <strong style="color:{color}; font-size:0.95rem;">{title}</strong>
                        <p style="color:#475569; font-size:0.87rem; line-height:1.7; margin:6px 0 0;">{desc}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    section_divider()

    # Conclusion finale (slide 52 & 54)
    st.markdown("## 🎯 Conclusions & Résumé")
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("""
        <div class="section-card" style="background:linear-gradient(135deg, #f0fdf4 0%, #eff6ff 100%); border:2px solid #86efac;">
            <h3 style="color:#16a34a; margin-top:0;">✅ Ce qui a été accompli</h3>
            <ul style="color:#475569; line-height:2; margin:0; padding-left:18px; font-size:0.9rem;">
                <li>✓ 3 approches complémentaires développées</li>
                <li>✓ Classes bactéricides CARD identifiées</li>
                <li>✓ LLMs évalués et limites documentées</li>
                <li>✓ Revue de littérature systématique</li>
                <li>✓ Ratio CMB/CMI comme critère objectif</li>
                <li>✓ Liste finale de <strong>8 classes bactéricides strictes</strong> validées dans CARD</li>
                <li>✓ Visualisations & exports JSON/CSV complets</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="section-card" style="background:#eff6ff; border:2px solid #bfdbfe;">
            <h3 style="color:#1a56db; margin-top:0;">❓ Question Centrale</h3>
            <blockquote style="color:#1e293b; font-style:italic; font-size:0.95rem; line-height:1.8; border-left:4px solid #1a56db; padding-left:14px; margin:0;">
            Comment distinguer de manière fiable et automatique les classes bactéricides
            des bactériostatiques dans CARD en exploitant conjointement les données
            génomiques et la littérature scientifique ?
            </blockquote>
            <div style="margin-top:14px; background:white; border-radius:8px; padding:12px; font-size:0.88rem; color:#475569;">
                <strong>Réponse :</strong> En croisant 3 approches génomiques/pharmacologiques avec
                le gold standard CMB/CMI, en évaluant les LLMs comme aide mais pas comme source unique.
            </div>
        </div>
        """, unsafe_allow_html=True)

    section_divider()

    # Références (slide 53)
    st.markdown("## 📚 Références Bibliographiques")
    refs = [
        ("1", "Ullah, H., & Ali, S. (2017)", "Classification of Anti-Bacterial Agents and Their Functions. Antibacterial agents, Chapter 1."),
        ("2", "McGowan, J.E. (2006)", "Antimicrobial resistance in hospital organisms and its relation to antibiotic use. Reviews of Infectious Diseases."),
        ("3", "Lowy, F.D. (2003)", "Antimicrobial resistance: the example of Staphylococcus aureus. Journal of Clinical Investigation."),
        ("4", "McArthur et al. (2013)", "The Comprehensive Antibiotic Resistance Database (CARD). Antimicrobial Agents and Chemotherapy."),
        ("5", "Jorgensen, J.H. & Ferraro, M.J. (2009)", "Antimicrobial susceptibility testing: a review. Clinical Infectious Diseases."),
        ("6", "Lewis, K. (2010)", "Persister cells and the riddle of biofilm survival. Biochemistry (Moscow)."),
        ("7", "Lahlou, M. (2013)", "The success of natural products in drug discovery. Pharmacology & Pharmacy."),
        ("8", "EUCAST (2024)", "Clinical breakpoints and dosing of antibiotics. European Committee on Antimicrobial Susceptibility Testing."),
    ]
    for num, author, title in refs:
        st.markdown(f"""
        <div style="display:flex; gap:12px; align-items:flex-start; padding:10px 0; border-bottom:1px solid #e2e8f0;">
            <div style="background:#1a56db; color:white; font-weight:700; font-size:0.85rem;
                         border-radius:6px; padding:4px 10px; min-width:28px; text-align:center;">{num}</div>
            <div style="font-size:0.88rem; color:#475569; line-height:1.6;">
                <strong style="color:#1e293b;">{author}</strong> — {title}
            </div>
        </div>
        """, unsafe_allow_html=True)
