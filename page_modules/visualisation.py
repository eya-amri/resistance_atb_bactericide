# visualisation.py
import streamlit as st
import pandas as pd
from utils.helpers import section_divider, info_box
from utils.load_data import get_distribution_data, get_card_stats, get_mdr_data
from utils.charts import (
    bar_chart_classes,
    pie_chart_distribution_card,
    mdr_bar_chart,
    bar_aro_mechanisms,
    pie_chart_distribution,
)


def render():
    st.markdown("# 📊 Visualisation des Données")
    st.markdown(
        '<p style="color:#64748b; font-size:1.05rem; margin-bottom:28px;">Exploration graphique basée sur les données réelles extraites de CARD et les résultats des 3 approches.</p>',
        unsafe_allow_html=True,
    )

    stats = get_card_stats()

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🧬 Total classes CARD", stats["total"], "Drug Classes")
    with col2:
        st.metric(
            "☠️ Bactéricides stricts",
            stats["bactericide_strict"],
            f"{stats['pct_bactericide_strict']}% — validées",
        )
    with col3:
        st.metric(
            "⏸️ Bactériostatiques",
            stats["bacteriostatic"],
            f"{stats['pct_bacteriostatic']}% du total",
        )
    with col4:
        st.metric(
            "❓ Non déterminées",
            stats["undetermined"],
            f"{stats['pct_undetermined']}% — lacune",
        )

    section_divider()

    # Distribution CARD réelle
    st.markdown("## 📈 Distribution Réelle des 46 Classes CARD")
    col1, col2 = st.columns([2, 3], gap="large")
    with col1:
        fig_pie = pie_chart_distribution_card()
        st.plotly_chart(
            fig_pie, use_container_width=True, config={"displayModeBar": False}
        )
    with col2:
        df = get_distribution_data()
        fig_bar = bar_chart_classes(df)
        st.plotly_chart(
            fig_bar, use_container_width=True, config={"displayModeBar": False}
        )

    section_divider()

    # Approche 1 – Mécanismes ARO
    st.markdown("## 🔬 Approche 1 – Nombre de Drug Classes par Mécanisme ARO")
    info_box(
        """
    <strong>Idée centrale :</strong> Une classe d'antibiotiques est d'autant plus importante qu'elle concentre
    plusieurs mécanismes de résistance dans CARD. 5 mécanismes analysés depuis le champ
    <code>ARO_category</code> dans <code>card.json</code>.
    """,
        kind="info",
    )
    fig_mech = bar_aro_mechanisms()
    st.plotly_chart(
        fig_mech, use_container_width=True, config={"displayModeBar": False}
    )

    col1, col2, col3, col4, col5 = st.columns(5)
    mech_data = [
        ("Antibiotic Inactivation", 22, "#3b82f6"),
        ("Target Alteration", 41, "#ef4444"),
        ("Antibiotic Efflux", 33, "#22c55e"),
        ("Target Protection", 15, "#f97316"),
        ("Target Replacement", 8, "#a855f7"),
    ]
    for col, (name, count, color) in zip([col1, col2, col3, col4, col5], mech_data):
        with col:
            st.markdown(
                f"""
            <div style="text-align:center; background:white; border-radius:10px; padding:12px 8px;
                        border:2px solid {color}; margin-top:8px;">
                <div style="font-size:1.5rem; font-weight:800; color:{color};">{count}</div>
                <div style="font-size:0.72rem; color:#475569; font-weight:500; margin-top:4px;">{name}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    section_divider()

    # Approche 3 – MDR
    st.markdown("## 🧬 Approche 3 – Top Classes dans les Gènes Multi-Résistants")
    info_box(
        """
    <strong>Score MDR</strong> = nombre de Drug Classes distinctes ciblées par un seul gène de résistance.
    Score maximum observé dans CARD = <strong>13</strong> | n = <strong>3530 gènes MDR</strong> (seuil ≥ 2).
    Les barres <strong>bleu foncé</strong> = classes présentes dans les gènes au score maximal (TOP genes).
    """,
        kind="info",
    )
    df_mdr = get_mdr_data()
    fig_mdr = mdr_bar_chart(df_mdr)
    st.plotly_chart(fig_mdr, use_container_width=True, config={"displayModeBar": False})

    section_divider()

    # Tableau données
    st.markdown("## 🗂️ Tableau Complet – Classes CARD Analysées")
    df = get_distribution_data()
    filter_col, _ = st.columns([2, 3])
    with filter_col:
        filt = st.selectbox(
            "Filtrer par activité :",
            [
                "Toutes",
                "Bactéricide",
                "Bactériostatique",
                "Double activité",
                "Non déterminé",
            ],
        )
    display_df = df if filt == "Toutes" else df[df["Activité"] == filt]

    def style_activity(val):
        colors = {
            "Bactéricide": "background-color:#eff6ff; color:#1a56db; font-weight:600;",
            "Bactériostatique": "background-color:#f1f5f9; color:#475569; font-weight:600;",
            "Double activité": "background-color:#e0f2fe; color:#0369a1; font-weight:600;",
            "Non déterminé": "background-color:#f8fafc; color:#94a3b8; font-weight:600;",
        }
        return colors.get(val, "")

    styled = display_df.style.applymap(style_activity, subset=["Activité"])
    st.dataframe(styled, use_container_width=True, hide_index=True, height=420)
    st.markdown(
        f'<div style="text-align:right; color:#94a3b8; font-size:0.82rem;">{len(display_df)} classe(s) sur {len(df)} — données CARD réelles</div>',
        unsafe_allow_html=True,
    )
