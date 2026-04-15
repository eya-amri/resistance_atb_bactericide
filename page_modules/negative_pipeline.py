import streamlit as st
from utils.helpers import section_divider, info_box


def render():

    # ───────────────── NAVBAR TOP ─────────────────
    st.markdown(
        """
    <div style="
        display:flex;
        justify-content:center;
        gap:30px;
        padding:14px;
        border-radius:14px;
        background:linear-gradient(135deg,#e0f2fe,#f0f9ff);
        margin-bottom:25px;
        font-weight:600;
    ">
        <a href="#architecture" style="text-decoration:none;color:#023e8a;">Architecture</a>
        <a href="#steps" style="text-decoration:none;color:#023e8a;">Pipeline</a>
        <a href="#diamond" style="text-decoration:none;color:#023e8a;">DIAMOND</a>
        <a href="#interpro" style="text-decoration:none;color:#023e8a;">InterProScan</a>
        <a href="#result" style="text-decoration:none;color:#023e8a;">Résultat</a>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # ───────────────── HERO ─────────────────
    st.markdown(
        """
    <div class="hero-wrap">
        <div class="hero-left">
            <div class="hero-eyebrow">DATA ENGINEERING • BIOINFORMATIQUE</div>
            <div class="hero-title">
                Construction du <span class="accent">Dataset Négatif</span>
            </div>
            <div class="hero-subtitle">
                Pipeline robuste basé sur UniProtKB/Swiss-Prot avec filtrage multi-niveaux
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # ───────────────── INTRO ─────────────────
    st.markdown('<div id="architecture"></div>', unsafe_allow_html=True)

    st.markdown("### 🧠 Pourquoi ce pipeline ?")

    info_box(
        """
    L'objectif est de construire un dataset négatif **fiable et sans ambiguïté** 
    pour entraîner un modèle capable de distinguer les protéines de résistance (ARG) 
    des protéines normales.
    """
    )

    st.markdown(
        """
    - Source : **UniProtKB / Swiss-Prot**
    - Données : séquences **manuellement annotées**
    - Avantage : **non-redondance + haute qualité**
    """
    )

    section_divider()

    # ───────────────── PIPELINE STEPS ─────────────────
    st.markdown('<div id="steps"></div>', unsafe_allow_html=True)
    st.markdown("## ⚙️ Pipeline global")

    st.markdown(
        """
    **Flux de transformation des données :**

    ```
    574,627 → 70,000 → 58,171 → 56,122 → FINAL
    ```
    """
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Sampling", "70,000")
    col2.metric("CD-HIT", "58,171")
    col3.metric("DIAMOND", "56,122")
    col4.metric("Final", "56,122")

    section_divider()

    # ───────────────── STEP DETAILS ─────────────────
    st.markdown("## 🔬 Étapes détaillées")

    st.markdown("### 1️⃣ Reservoir Sampling")
    st.markdown(
        """
    - Échantillonnage aléatoire de **70,000 séquences**
    - Algorithme : **Reservoir Sampling**
    - Avantage : mémoire constante
    """
    )

    st.markdown("### 2️⃣ CD-HIT (90%)")
    st.markdown(
        """
    - Supprime les séquences similaires (>90%)
    - Réduction du biais phylogénétique
    - Résultat : **58,171 séquences**
    """
    )

    # ───────────────── DIAMOND ─────────────────
    st.markdown('<div id="diamond"></div>', unsafe_allow_html=True)

    st.markdown("## ⚡ DIAMOND — Filtre d’homologie")

    info_box(
        """
    DIAMOND élimine toutes les séquences ressemblant à des ARG.
    """,
        "warning",
    )

    st.markdown(
        """
    **Critères utilisés :**
    - Identité ≥ 30%
    - Couverture ≥ 80%
    - E-value ≤ 1e-10

    Résultat :
    - 58,171 → **56,122**
    """
    )

    section_divider()

    # ───────────────── INTERPRO ─────────────────
    st.markdown('<div id="interpro"></div>', unsafe_allow_html=True)

    st.markdown("## 🧬 InterProScan — Filtre fonctionnel")

    st.markdown(
        """
    Détection de domaines protéiques via :
    - Pfam
    - TIGRFAM
    - PROSITE
    """
    )

    info_box(
        """
    Même sans similarité globale, une protéine peut contenir un domaine de résistance.
    InterProScan permet de détecter ces cas.
    """,
        "info",
    )

    st.markdown(
        """
    ✔️ Résultat :
    - Aucun domaine de résistance détecté
    - Dataset final validé
    """
    )

    section_divider()

    # ───────────────── RESULT ─────────────────
    st.markdown('<div id="result"></div>', unsafe_allow_html=True)

    st.markdown("## 📊 Résultat final")

    st.success(
        """
    ✔️ 56,122 séquences négatives  
    ✔️ Haute qualité  
    ✔️ Aucun ARG détecté  
    ✔️ Dataset prêt pour Machine Learning
    """
    )

    # ───────────────── LOGS ─────────────────
    st.markdown("## 🖥️ Logs d'exécution")

    st.code(
        """
ALL STEPS COMPLETED SUCCESSFULLY
Final output: negative_final.fasta
"""
    )
