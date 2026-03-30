# definitions.py
import streamlit as st
from utils.helpers import section_divider, info_box
from utils.load_data import BACTERICIDAL_CLASSES, BACTERIOSTATIC_CLASSES, DUAL_CLASSES
import pandas as pd
import plotly.graph_objects as go


# ─────────────────────────────────────────────────────────────────────────────
# DATA LOCALES
# ─────────────────────────────────────────────────────────────────────────────

CARD_BACTERICIDE_LIST = [
    "carbapenem",
    "cephalosporin",
    "glycopeptide antibiotic",
    "nitroimidazole antibiotic",
    "penicillin beta-lactam",
    "phosphonic acid antibiotic",
    "rifamycin antibiotic",
    "monobactam",
    "aminoglycosides",
    "fluoroquinolones",
]
CARD_BACTERICIDE_STRICT_LIST = [
    "carbapenem",
    "cephalosporin",
    "glycopeptide antibiotic",
    "nitroimidazole antibiotic",
    "penicillin beta-lactam",
    "phosphonic acid antibiotic",
    "rifamycin antibiotic",
    "monobactam",
]

CARD_ARO_GENES = {
    "Cephalosporin": 3404,
    "Penicillin beta-lactam": 3115,
    "Carbapenem": 2572,
    "Monobactam": 1310,
    "Fluoroquinolone": 307,
    "Aminoglycoside": 303,
    "Macrolide": 212,
    "Peptide": 187,
    "Tetracycline": 186,
    "Phenicol": 140,
    "Lincosamide": 108,
    "Glycopeptide": 103,
    "Streptogramin": 99,
    "Rifamycin": 63,
    "Phosphonic acid": 48,
    "Glycylcycline": 37,
    "Oxazolidinone": 18,
    "Nitroimidazole": 18,
    "Sulfonamide": 10,
}

# mapping activité pour les 19 classes CARD avec ARO
_ACT_MAP = {
    "Cephalosporin": "Bactéricide strict",
    "Penicillin beta-lactam": "Bactéricide strict",
    "Carbapenem": "Bactéricide strict",
    "Monobactam": "Bactéricide strict",
    "Glycopeptide": "Bactéricide strict",
    "Rifamycin": "Bactéricide strict",
    "Phosphonic acid": "Bactéricide strict",
    "Nitroimidazole": "Bactéricide strict",
    "Fluoroquinolone": "Double activité",
    "Aminoglycoside": "Double activité",
    "Glycylcycline": "Double activité",
    "Macrolide": "Bactériostatique",
    "Tetracycline": "Bactériostatique",
    "Phenicol": "Bactériostatique",
    "Lincosamide": "Bactériostatique",
    "Streptogramin": "Bactériostatique",
    "Oxazolidinone": "Bactériostatique",
    "Sulfonamide": "Bactériostatique",
    "Peptide": "Non déterminé",
}

_COLOR_MAP = {
    "Bactéricide strict": "#1a56db",
    "Double activité": "#0ea5e9",
    "Bactériostatique": "#64748b",
    "Non déterminé": "#94a3b8",
}

PLOTLY_LAYOUT = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10, r=10, t=36, b=10),
    font=dict(family="DM Sans, sans-serif", color="#475569"),
)


# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────


def _inject_def_css():
    st.markdown(
        """
    <style>
    .def-list-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:14px 0 8px;}
    .def-list-item{
        display:flex;align-items:center;gap:12px;background:#ffffff;
        border:1.5px solid #e0eaf6;border-radius:12px;padding:13px 16px;
        box-shadow:0 2px 8px rgba(0,100,180,0.06);
        transition:box-shadow .2s,border-color .2s;
    }
    .def-list-item:hover{border-color:#93c5fd;box-shadow:0 4px 16px rgba(0,100,180,0.12);}
    .def-list-dot{width:10px;height:10px;border-radius:50%;flex-shrink:0;}
    .def-list-label{font-size:0.93rem;font-weight:700;color:#1e3a5f;letter-spacing:0.01em;}
    .dot-bactericide   {background:#1a56db;}
    .dot-bacteriostatic{background:#64748b;}
    .dot-dual          {background:#0ea5e9;}
    .item-bactericide  {border-left:4px solid #1a56db!important;}
    .item-bacteriostatic{border-left:4px solid #64748b!important;}
    .item-dual         {border-left:4px solid #0ea5e9!important;}

    /* modal */
    .modal-bg{display:none;position:fixed;inset:0;z-index:9999;
        background:rgba(2,30,70,.55);backdrop-filter:blur(6px);
        align-items:center;justify-content:center;}
    .modal-bg.open{display:flex;}
    .modal-inner{
        background:#fff;border-radius:20px;padding:32px 36px;
        max-width:640px;width:94%;max-height:85vh;overflow-y:auto;
        box-shadow:0 24px 80px rgba(2,62,138,.28);
        position:relative;animation:fadeUp .25s ease;}
    @keyframes fadeUp{from{opacity:0;transform:translateY(24px);}to{opacity:1;transform:translateY(0);}}
    .modal-close-btn{position:absolute;top:14px;right:18px;background:none;border:none;
        font-size:1.2rem;cursor:pointer;color:#64748b;transition:color .2s;}
    .modal-close-btn:hover{color:#dc2626;}

    /* boutons */
    .viz-btn{
        display:inline-flex;align-items:center;gap:8px;
        background:linear-gradient(135deg,#1a56db,#0ea5e9);
        color:#fff;border:none;border-radius:30px;padding:9px 20px;
        font-size:0.83rem;font-weight:600;cursor:pointer;margin-top:12px;
        box-shadow:0 4px 14px rgba(26,86,219,.25);
        transition:transform .2s,box-shadow .2s;}
    .viz-btn:hover{transform:translateY(-2px);box-shadow:0 8px 22px rgba(26,86,219,.35);}

    /* ratio cards */
    .ratio-card{border-radius:14px;padding:22px 20px;text-align:center;border-width:2px;border-style:solid;}
    .ratio-pill{display:inline-block;color:white;font-size:1.05rem;font-weight:800;
        border-radius:8px;padding:9px 16px;margin-bottom:12px;width:100%;}

    /* triangle warning */
    .warn-triangle{
        background:linear-gradient(135deg,#fff7ed,#fef3c7);
        border-left:5px solid #f97316;border-radius:14px;
        padding:20px 24px;margin-top:20px;
        font-size:0.9rem;color:#78350f;line-height:1.8;}
    .warn-triangle h4{margin:0 0 10px;color:#c2410c;font-size:1rem;}

    /* card result */
    .card-result-block{border-radius:16px;padding:22px 24px;border:2px solid;margin-bottom:16px;}

    /* stat badge inline */
    .stat-inline{
        display:inline-flex;align-items:center;gap:10px;
        padding:10px 14px;border-radius:10px;margin-bottom:8px;width:100%;}
    </style>
    """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS GÉNÉRIQUES
# ─────────────────────────────────────────────────────────────────────────────


def _list_grid(items, color_class, item_class):
    html = "".join(
        f'<div class="def-list-item {item_class}">'
        f'<span class="def-list-dot {color_class}"></span>'
        f'<span class="def-list-label">{item}</span></div>'
        for item in items
    )
    st.markdown(f'<div class="def-list-grid">{html}</div>', unsafe_allow_html=True)


def _section_label(text):
    st.markdown(
        f'<p style="font-size:0.75rem;color:#64748b;font-weight:700;letter-spacing:1.5px;'
        f'text-transform:uppercase;margin:16px 0 4px;">{text}</p>',
        unsafe_allow_html=True,
    )


def _pc(fig):
    """plotly_chart shortcut."""
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ─────────────────────────────────────────────────────────────────────────────
# CHARTS
# ─────────────────────────────────────────────────────────────────────────────


def _bar_bactericide_only():
    bact = {
        k: v
        for k, v in CARD_ARO_GENES.items()
        if k
        in [
            "Cephalosporin",
            "Penicillin beta-lactam",
            "Carbapenem",
            "Monobactam",
            "Glycopeptide",
            "Rifamycin",
            "Phosphonic acid",
            "Nitroimidazole",
            "Aminoglycoside",
            "Fluoroquinolone",
        ]
    }
    classes = list(bact.keys())
    genes = list(bact.values())
    colors = [
        "#0ea5e9" if c in ["Aminoglycoside", "Fluoroquinolone"] else "#1a56db"
        for c in classes
    ]
    fig = go.Figure(
        go.Bar(
            x=classes,
            y=genes,
            marker=dict(color=colors, line=dict(color="white", width=1.5)),
            text=[f"{g:,}" for g in genes],
            textposition="outside",
            textfont=dict(size=10, color="#475569"),
            hovertemplate="<b>%{x}</b><br>ARO : <b>%{y:,}</b><extra></extra>",
        )
    )
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(
            text="Classes Bactéricides CARD — Gènes ARO",
            font=dict(size=13, color="#1a56db"),
        ),
        xaxis=dict(tickangle=-22, tickfont=dict(size=10), showgrid=False),
        yaxis=dict(
            showgrid=True,
            gridcolor="#f0f4f8",
            title="Gènes ARO",
            tickfont=dict(size=10),
        ),
        height=340,
        showlegend=False,
    )
    return fig


def _bar_bactericide_strict():
    strict = {
        k: v
        for k, v in CARD_ARO_GENES.items()
        if k
        in [
            "Cephalosporin",
            "Penicillin beta-lactam",
            "Carbapenem",
            "Monobactam",
            "Glycopeptide",
            "Rifamycin",
            "Phosphonic acid",
            "Nitroimidazole",
        ]
    }
    classes = list(strict.keys())
    genes = list(strict.values())
    fig = go.Figure(
        go.Bar(
            x=classes,
            y=genes,
            marker=dict(
                color="#1a56db", opacity=0.87, line=dict(color="white", width=1.5)
            ),
            text=[f"{g:,}" for g in genes],
            textposition="outside",
            textfont=dict(size=10, color="#475569"),
            hovertemplate="<b>%{x}</b><br>ARO : <b>%{y:,}</b><extra></extra>",
        )
    )
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(
            text="Bactéricides Stricts CARD — Gènes ARO",
            font=dict(size=13, color="#1a56db"),
        ),
        xaxis=dict(tickangle=-20, tickfont=dict(size=10), showgrid=False),
        yaxis=dict(
            showgrid=True,
            gridcolor="#f0f4f8",
            title="Gènes ARO",
            tickfont=dict(size=10),
        ),
        height=320,
        showlegend=False,
    )
    return fig


def _bar_bacteriostatic():
    bstatic = {
        k: v
        for k, v in CARD_ARO_GENES.items()
        if k
        in [
            "Macrolide",
            "Tetracycline",
            "Phenicol",
            "Lincosamide",
            "Streptogramin",
            "Oxazolidinone",
            "Sulfonamide",
        ]
    }
    classes = list(bstatic.keys())
    genes = list(bstatic.values())
    fig = go.Figure(
        go.Bar(
            x=classes,
            y=genes,
            marker=dict(
                color="#64748b", opacity=0.83, line=dict(color="white", width=1.5)
            ),
            text=[f"{g:,}" for g in genes],
            textposition="outside",
            textfont=dict(size=10, color="#475569"),
            hovertemplate="<b>%{x}</b><br>ARO : <b>%{y:,}</b><extra></extra>",
        )
    )
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(
            text="Bactériostatiques CARD — Gènes ARO",
            font=dict(size=13, color="#64748b"),
        ),
        xaxis=dict(tickangle=-20, tickfont=dict(size=10), showgrid=False),
        yaxis=dict(
            showgrid=True,
            gridcolor="#f0f4f8",
            title="Gènes ARO",
            tickfont=dict(size=10),
        ),
        height=300,
        showlegend=False,
    )
    return fig


def _bar_dual():
    dual_aro = {
        "Fluoroquinolone": 307,
        "Aminoglycoside": 303,
        "Tetracycline": 186,
        "Phenicol": 140,
        "Glycylcycline": 37,
        "Oxazolidinone": 18,
    }
    fig = go.Figure(
        go.Bar(
            x=list(dual_aro.keys()),
            y=list(dual_aro.values()),
            marker=dict(
                color="#0ea5e9", opacity=0.87, line=dict(color="white", width=1.5)
            ),
            text=[f"{g:,}" for g in dual_aro.values()],
            textposition="outside",
            textfont=dict(size=10, color="#475569"),
            hovertemplate="<b>%{x}</b><br>ARO : <b>%{y:,}</b><extra></extra>",
        )
    )
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(
            text="Classes Double Activité — Gènes ARO",
            font=dict(size=13, color="#0369a1"),
        ),
        xaxis=dict(tickfont=dict(size=10), showgrid=False),
        yaxis=dict(
            showgrid=True,
            gridcolor="#f0f4f8",
            title="Gènes ARO",
            tickfont=dict(size=10),
        ),
        height=300,
        showlegend=False,
    )
    return fig


def _donut_distribution():
    labels = [
        "Bactéricide strict",
        "Double activité",
        "Bactériostatique",
        "Non déterminé",
    ]
    values = [8, 2, 9, 27]
    colors = ["#1a56db", "#0ea5e9", "#64748b", "#e2e8f0"]
    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.55,
            marker=dict(colors=colors, line=dict(color="#fff", width=3)),
            textinfo="label+percent",
            textfont=dict(size=11, family="DM Sans", color="#1e3a5f"),
            hovertemplate="<b>%{label}</b><br>%{value} classes (%{percent})<extra></extra>",
            pull=[0.05, 0.03, 0, 0],
        )
    )
    fig.add_annotation(
        text="<b>46</b><br>classes CARD",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=13, color="#1e3a5f", family="DM Sans"),
    )
    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=340,
        legend=dict(
            orientation="v",
            x=1.02,
            y=0.5,
            font=dict(size=11, color="#475569", family="DM Sans"),
        ),
        margin=dict(l=0, r=10, t=20, b=0),
    )
    return fig


def _bar_aro_all():
    classes = list(CARD_ARO_GENES.keys())
    genes = list(CARD_ARO_GENES.values())
    bar_colors = [_COLOR_MAP[_ACT_MAP[c]] for c in classes]
    fig = go.Figure()
    # barres
    fig.add_trace(
        go.Bar(
            x=genes,
            y=classes,
            orientation="h",
            marker=dict(
                color=bar_colors, line=dict(color="rgba(255,255,255,0.4)", width=1)
            ),
            text=[f"{g:,}" for g in genes],
            textposition="outside",
            textfont=dict(size=9, color="#475569"),
            hovertemplate="<b>%{y}</b><br>ARO : <b>%{x:,}</b><extra></extra>",
            showlegend=False,
        )
    )
    # légende manuelle
    for act, col in _COLOR_MAP.items():
        fig.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                marker=dict(size=10, color=col, symbol="square"),
                name=act,
                showlegend=True,
            )
        )
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(
            text="Distribution des Gènes ARO par Classe (CARD – 19 classes documentées)",
            font=dict(size=13, color="#1e3a5f"),
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="#f0f4f8",
            title="Nombre de gènes ARO",
            tickfont=dict(size=9),
        ),
        yaxis=dict(tickfont=dict(size=10, color="#1e3a5f")),
        height=580,
        legend=dict(orientation="h", x=0, y=-0.1, font=dict(size=10)),
        margin=dict(l=10, r=80, t=36, b=10),
    )
    return fig


def _gauge_ratio(value, label, color):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={
                "text": label,
                "font": {"size": 11, "color": "#1e3a5f", "family": "DM Sans"},
            },
            number={
                "font": {"size": 20, "color": color, "family": "DM Sans"},
                "suffix": "×",
            },
            gauge={
                "axis": {
                    "range": [0, 64],
                    "tickwidth": 1,
                    "tickcolor": "#e2e8f0",
                    "tickfont": {"size": 8},
                },
                "bar": {"color": color},
                "bgcolor": "#f8fafc",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 4], "color": "#dbeafe"},
                    {"range": [4, 32], "color": "#f1f5f9"},
                    {"range": [32, 64], "color": "#eff6ff"},
                ],
                "threshold": {
                    "line": {"color": color, "width": 3},
                    "thickness": 0.75,
                    "value": value,
                },
            },
        )
    )
    fig.update_layout(
        margin=dict(l=10, r=10, t=44, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        height=200,
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# MODAL LLM (HTML pur, uid unique pour éviter conflits)
# ─────────────────────────────────────────────────────────────────────────────


def _llm_modal_button(uid="a"):
    st.markdown(
        f"""
    <button class="viz-btn" onclick="document.getElementById('llmM_{uid}').classList.add('open')">
        🤖 Voir détail LLM
    </button>
    <div class="modal-bg" id="llmM_{uid}" onclick="if(event.target===this)this.classList.remove('open')">
      <div class="modal-inner">
        <button class="modal-close-btn" onclick="document.getElementById('llmM_{uid}').classList.remove('open')">✕</button>
        <h3 style="color:#1a56db;margin-top:0;">🤖 LLMs Testés – Analyse Critique</h3>

        <div style="border:1.5px solid #dbeafe;border-radius:12px;padding:16px;margin-bottom:12px;">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
            <span style="font-size:1.2rem;">🔵</span>
            <strong style="color:#1a56db;">BioGPT (Microsoft)</strong>
          </div>
          <p style="color:#475569;font-size:0.85rem;margin:0 0 8px;">Pré-entraîné sur <strong>millions d'articles PubMed</strong>. Optimisé pour le langage biomédical.</p>
          <div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px;">
            <span style="background:#f0fdf4;color:#16a34a;border-radius:6px;padding:3px 9px;font-size:0.77rem;font-weight:600;">✅ Large couverture PubMed</span>
            <span style="background:#f0fdf4;color:#16a34a;border-radius:6px;padding:3px 9px;font-size:0.77rem;font-weight:600;">✅ Open source</span>
          </div>
          <div style="background:#fef2f2;border-radius:8px;padding:9px 12px;font-size:0.82rem;color:#dc2626;border-left:3px solid #ef4444;">
            ❌ <strong>Biais systématique</strong> : classe TOUT bactéricide.<br>
            ❌ Hallucinations fréquentes sur les classes rares.
          </div>
        </div>

        <div style="border:1.5px solid #ede9fe;border-radius:12px;padding:16px;margin-bottom:12px;">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
            <span style="font-size:1.2rem;">🟣</span>
            <strong style="color:#7c3aed;">BioMedLM (Stanford CRFM)</strong>
          </div>
          <p style="color:#475569;font-size:0.85rem;margin:0 0 8px;">Corpus <strong>médicaux et pharmacologiques</strong> dédiés.</p>
          <div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px;">
            <span style="background:#f0fdf4;color:#16a34a;border-radius:6px;padding:3px 9px;font-size:0.77rem;font-weight:600;">✅ Raisonnement clinique</span>
            <span style="background:#f0fdf4;color:#16a34a;border-radius:6px;padding:3px 9px;font-size:0.77rem;font-weight:600;">✅ Données pharma</span>
          </div>
          <div style="background:#fef2f2;border-radius:8px;padding:9px 12px;font-size:0.82rem;color:#dc2626;border-left:3px solid #ef4444;">
            ❌ <strong>Résultats incohérents</strong> : confusion entre classes similaires.
          </div>
        </div>

        <div style="border:1.5px solid #fde68a;border-radius:12px;padding:16px;margin-bottom:12px;">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
            <span style="font-size:1.2rem;">🟠</span>
            <strong style="color:#d97706;">Mistral-7B-Instruct-v0.3</strong>
          </div>
          <p style="color:#475569;font-size:0.85rem;margin:0 0 8px;">Modèle généraliste <strong>7B paramètres</strong> Mistral AI, testé en mode instruction.</p>
          <div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px;">
            <span style="background:#f0fdf4;color:#16a34a;border-radius:6px;padding:3px 9px;font-size:0.77rem;font-weight:600;">✅ Général & polyvalent</span>
            <span style="background:#f0fdf4;color:#16a34a;border-radius:6px;padding:3px 9px;font-size:0.77rem;font-weight:600;">✅ Open source</span>
          </div>
          <div style="background:#fef2f2;border-radius:8px;padding:9px 12px;font-size:0.82rem;color:#dc2626;border-left:3px solid #ef4444;">
            ❌ <strong>Non performant</strong> sur la classification fine bactéricide/bactériostatique.<br>
            ❌ Confusions fréquentes entre sous-classes et précision pharmacologique insuffisante.
          </div>
        </div>

        <div style="background:#f0fdf4;border-radius:10px;padding:12px 16px;font-size:0.84rem;color:#14532d;border-left:4px solid #16a34a;">
          <strong>→ Conclusion :</strong> Aucun LLM testé n'est suffisant seul. Validation basée sur
          le <strong>ratio CMB/CMI</strong> et la <strong>littérature biomédicale</strong>.
        </div>
      </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# RENDER PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────


def render():
    _inject_def_css()

    st.markdown("# 📖 Définitions & Classification")
    st.markdown(
        '<p style="color:#64748b;font-size:1.05rem;margin-bottom:24px;">'
        "Cadre théorique de la classification bactéricide/bactériostatique, "
        "listes des classes par activité et visualisations CARD."
        "</p>",
        unsafe_allow_html=True,
    )

    # ══════════════════════════════════════════════════════════════════════════
    # 1. BACTÉRICIDE vs BACTÉRIOSTATIQUE
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("## ⚗️ Cadre Théorique : Bactéricide vs Bactériostatique")
    col1, col2 = st.columns(2, gap="large")

    with col1:
        # Définition
        st.markdown(
            """
        <div class="section-card" style="border-top:4px solid #1a56db;">
          <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
            <div style="background:#eff6ff;border-radius:10px;padding:10px;font-size:1.6rem;">☠️</div>
            <h3 style="margin:0;color:#1a56db;">BACTÉRICIDE</h3>
          </div>
          <p style="color:#475569;line-height:1.8;font-style:italic;margin-bottom:12px;">Détruit les bactéries</p>
          <ul style="color:#475569;line-height:2;margin:0;padding-left:20px;">
            <li>Inhibition de la <strong>synthèse de la paroi bactérienne</strong></li>
            <li>Altération de la <strong>membrane bactérienne</strong></li>
            <li>Inhibition des <strong>enzymes bactériennes essentielles</strong></li>
            <li>Inhibition de la <strong>traduction des protéines</strong></li>
          </ul>
          <div style="background:#eff6ff;border-radius:8px;padding:12px;margin-top:14px;">
            <strong style="color:#1a56db;font-size:0.88rem;">Réduction ≥ 3 log₁₀ UFC/mL par rapport à l'inoculum initial</strong>
          </div>
        </div>
        """,
            unsafe_allow_html=True,
        )
        # Liste
        _section_label("Classes bactéricides CARD")
        _list_grid(BACTERICIDAL_CLASSES, "dot-bactericide", "item-bactericide")
        # Histogramme
        _pc(_bar_bactericide_only())

    with col2:
        # Définition
        st.markdown(
            """
        <div class="section-card" style="border-top:4px solid #64748b;">
          <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
            <div style="background:#f1f5f9;border-radius:10px;padding:10px;font-size:1.6rem;">⏸️</div>
            <h3 style="margin:0;color:#64748b;">BACTÉRIOSTATIQUE</h3>
          </div>
          <p style="color:#475569;line-height:1.8;font-style:italic;margin-bottom:12px;">Inhibe la croissance bactérienne</p>
          <ul style="color:#475569;line-height:2;margin:0;padding-left:20px;">
            <li>Inhibition de la <strong>synthèse des protéines</strong></li>
            <li>Inhibition au niveau du <strong>ribosome 50S</strong></li>
            <li>Liaison au ribosome 50S → <strong>arrêt traduction</strong></li>
            <li>Interférence avec <strong>réplication de l'ADN</strong></li>
          </ul>
          <div style="background:#f1f5f9;border-radius:8px;padding:12px;margin-top:14px;">
            <strong style="color:#64748b;font-size:0.88rem;">La croissance reprend à l'arrêt du traitement — dépend du système immunitaire</strong>
          </div>
        </div>
        """,
            unsafe_allow_html=True,
        )
        # Liste
        _section_label("Classes bactériostatiques")
        _list_grid(BACTERIOSTATIC_CLASSES, "dot-bacteriostatic", "item-bacteriostatic")
        # Histogramme
        _pc(_bar_bacteriostatic())

    section_divider()

    # ══════════════════════════════════════════════════════════════════════════
    # 2. BACTÉRICIDES STRICTS
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("## 🏆 Les Classes Bactéricides Strictes")
    st.markdown(
        """
    <div class="section-card" style="background:#eff6ff;">
      <p style="color:#475569;line-height:1.8;margin:0 0 12px 0;">
      Les <strong>bactéricides stricts</strong> tuent systématiquement les bactéries, indépendamment
      de la concentration et de la phase de croissance. Leur effet létal est <em>direct et irréversible</em>.
      </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    _section_label("8 classes bactéricides strictes (CARD)")
    _list_grid(BACTERICIDAL_CLASSES, "dot-bactericide", "item-bactericide")

    # Histogramme stricts
    _pc(_bar_bactericide_strict())

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
            <div class="section-card" style="text-align:center;background:white;">
              <div style="font-size:1.6rem;">{icon}</div>
              <strong style="color:#1a56db;font-size:0.85rem;display:block;margin:8px 0 6px;">{title}</strong>
              <p style="color:#64748b;font-size:0.8rem;margin:0;">{desc}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

    section_divider()

    # ══════════════════════════════════════════════════════════════════════════
    # 3. DOUBLE ACTIVITÉ
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("## ⚡ Double Activité (Bactéricide et Bactériostatique)")
    col1, col2 = st.columns([2, 3], gap="large")

    with col1:
        st.markdown(
            """
        <div class="section-card" style="border-top:4px solid #0ea5e9;">
          <h4 style="margin-top:0;color:#0369a1;">Classes à double activité</h4>
        </div>
        """,
            unsafe_allow_html=True,
        )
        _list_grid(list(dict.fromkeys(DUAL_CLASSES)), "dot-dual", "item-dual")
        _pc(_bar_dual())

    with col2:
        st.markdown(
            """
        <div class="section-card">
          <h4 style="color:#0369a1;margin-top:0;">Définition & Facteurs</h4>
          <p style="color:#475569;line-height:1.8;">
          Un antibiotique à double activité présente à la fois des effets bactéricides et bactériostatiques selon :
          </p>
          <ul style="color:#475569;line-height:1.9;margin:0;padding-left:20px;">
            <li>La <strong>concentration plasmique</strong> de l'antibiotique</li>
            <li>La <strong>durée d'exposition</strong> des bactéries</li>
            <li>La <strong>nature et sensibilité intrinsèque</strong> de la souche bactérienne</li>
          </ul>
          <div style="background:#f0f9ff;border-radius:8px;padding:12px;margin-top:14px;font-size:0.85rem;color:#0369a1;">
            ⚠️ Cette propriété reflète la dépendance de l'effet antibiotique à la pharmacodynamique
            et aux cibles moléculaires spécifiques de la bactérie.
          </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    section_divider()

    # ══════════════════════════════════════════════════════════════════════════
    # 4. LLMs
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("## 🤖 Tests LLMs Spécialisés – BioGPT, BioMedLM & Mistral")
    info_box(
        """
    <strong>⚠️ Résultats critiques :</strong> BioGPT : <strong>faux positifs systématiques</strong>.
    BioMedLM : <strong>résultats incohérents</strong>. Mistral-7B : <strong>non performant</strong>.
    → Nécessité de recourir à la littérature et au ratio CMB/CMI.
    """,
        kind="warning",
    )

    _llm_modal_button("llm1")

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "🔵 BioGPT (Microsoft)",
            "🟣 BioMedLM (Stanford)",
            "🟠 Mistral-7B",
            "📊 Bilan Comparatif",
        ]
    )
    with tab1:
        col1, col2 = st.columns([3, 2], gap="large")
        with col1:
            st.markdown(
                """
            <div class="section-card">
              <h4 style="color:#1a56db;margin-top:0;">BioGPT – Description</h4>
              <p style="color:#475569;line-height:1.8;">Pré-entraîné sur <strong>millions d'articles PubMed</strong>.</p>
              <div style="background:#fef2f2;border-radius:8px;padding:14px;margin-top:12px;border-left:4px solid #ef4444;">
                <strong style="color:#dc2626;">⚠️ TAUX ÉLEVÉ DE FAUX POSITIFS</strong> → Biais systématique bactéricide.
              </div>
            </div>""",
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                """
            <div class="section-card" style="background:#f0fdf4;border:1px solid #bbf7d0;">
              <h4 style="color:#16a34a;margin-top:0;">✅ Avantages</h4>
              <ul style="color:#475569;line-height:1.9;margin:0;padding-left:16px;font-size:0.88rem;">
                <li>Large couverture PubMed</li><li>Rapidité</li><li>Open source</li>
              </ul>
            </div>
            <div class="section-card" style="background:#fef2f2;border:1px solid #fca5a5;margin-top:0;">
              <h4 style="color:#dc2626;margin-top:0;">❌ Limites</h4>
              <ul style="color:#475569;line-height:1.9;margin:0;padding-left:16px;font-size:0.88rem;">
                <li>Biais systématique</li><li>Hallucinations</li>
              </ul>
            </div>""",
                unsafe_allow_html=True,
            )

    with tab2:
        col1, col2 = st.columns([3, 2], gap="large")
        with col1:
            st.markdown(
                """
            <div class="section-card">
              <h4 style="color:#7c3aed;margin-top:0;">BioMedLM – Description</h4>
              <p style="color:#475569;line-height:1.8;">Corpus <strong>médicaux et pharmacologiques</strong> (Stanford CRFM).</p>
              <div style="background:#fef2f2;border-radius:8px;padding:14px;margin-top:12px;border-left:4px solid #ef4444;">
                <strong style="color:#dc2626;">⚠️ Résultats incohérents</strong> → Confusion entre classes.
              </div>
            </div>""",
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                """
            <div class="section-card" style="background:#f0fdf4;border:1px solid #bbf7d0;">
              <h4 style="color:#16a34a;margin-top:0;">✅ Avantages</h4>
              <ul style="color:#475569;line-height:1.9;margin:0;padding-left:16px;font-size:0.88rem;">
                <li>Raisonnement clinique</li><li>Données pharma</li>
              </ul>
            </div>
            <div class="section-card" style="background:#fef2f2;border:1px solid #fca5a5;margin-top:0;">
              <h4 style="color:#dc2626;margin-top:0;">❌ Limites</h4>
              <ul style="color:#475569;line-height:1.9;margin:0;padding-left:16px;font-size:0.88rem;">
                <li>Incohérences</li><li>Confusion classes</li>
              </ul>
            </div>""",
                unsafe_allow_html=True,
            )

    with tab3:
        col1, col2 = st.columns([3, 2], gap="large")
        with col1:
            st.markdown(
                """
            <div class="section-card">
              <h4 style="color:#d97706;margin-top:0;">Mistral-7B-Instruct-v0.3 – Description</h4>
              <p style="color:#475569;line-height:1.8;">
              Modèle généraliste <strong>7B paramètres</strong> Mistral AI, mode instruction.
              Fine-tuné pour le suivi d'instructions.
              </p>
              <div style="background:#fef2f2;border-radius:8px;padding:14px;margin-top:12px;border-left:4px solid #ef4444;">
                <strong style="color:#dc2626;">⚠️ NON PERFORMANT</strong> sur la classification fine.
                Confusions fréquentes entre sous-classes et précision pharmacologique insuffisante.
              </div>
            </div>""",
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                """
            <div class="section-card" style="background:#f0fdf4;border:1px solid #bbf7d0;">
              <h4 style="color:#16a34a;margin-top:0;">✅ Avantages</h4>
              <ul style="color:#475569;line-height:1.9;margin:0;padding-left:16px;font-size:0.88rem;">
                <li>Général & polyvalent</li><li>Suivi d'instructions</li><li>Open source</li>
              </ul>
            </div>
            <div class="section-card" style="background:#fef2f2;border:1px solid #fca5a5;margin-top:0;">
              <h4 style="color:#dc2626;margin-top:0;">❌ Limites</h4>
              <ul style="color:#475569;line-height:1.9;margin:0;padding-left:16px;font-size:0.88rem;">
                <li>Non performant classification fine</li>
                <li>Connaissances biomédicales limitées</li>
              </ul>
            </div>""",
                unsafe_allow_html=True,
            )

    with tab4:
        comparison = pd.DataFrame(
            {
                "Modèle": [
                    "BioGPT (Microsoft)",
                    "BioMedLM (Stanford)",
                    "Mistral-7B-Instruct-v0.3",
                ],
                "Problème principal": [
                    "Faux positifs – classe TOUT bactéricide",
                    "Résultats incohérents – confusion classes",
                    "Non performant – précision pharmacologique insuffisante",
                ],
                "Avantages": [
                    "Couverture large, rapidité",
                    "Raisonnement clinique",
                    "Polyvalent, open source",
                ],
                "Conclusion": [
                    "❌ Inadapté seul",
                    "❌ Inadapté seul",
                    "❌ Inadapté seul",
                ],
            }
        )
        st.dataframe(comparison, use_container_width=True, hide_index=True)
        info_box(
            """<strong>→ Solution adoptée :</strong> LLMs comme source initiale de candidats,
        puis validation par <strong>ratio CMB/CMI</strong> et la <strong>littérature biomédicale</strong>.""",
            kind="info",
        )

    section_divider()

    # ══════════════════════════════════════════════════════════════════════════
    # 5. RATIO CMB/CMI
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("## 📐 Critère Quantitatif : Ratio CMB/CMI")
    info_box(
        """Le ratio CMB/CMI est le <strong>critère gold standard</strong> pour classer objectivement un antibiotique.
    CMB = Concentration Minimale Bactéricide | CMI = Concentration Minimale Inhibitrice.""",
        kind="info",
    )

    col1, col2, col3 = st.columns(3, gap="medium")
    for col, (bg, color, ratio, label, desc, note) in zip(
        [col1, col2, col3],
        [
            (
                "#fef2f2",
                "#dc2626",
                "CMB/CMI ≤ 4",
                "BACTÉRICIDE",
                "L'antibiotique tue 99,99 % de la population bactérienne à une concentration proche de la CMI.",
                "",
            ),
            (
                "#f0fdf4",
                "#16a34a",
                "4 < CMB/CMI < 32",
                "BACTÉRIOSTATIQUE",
                "L'antibiotique inhibe la croissance sans tuer efficacement les bactéries.",
                "",
            ),
            (
                "#eff6ff",
                "#1a56db",
                "CMB/CMI ≥ 32",
                "TOLÉRANCE",
                "Les bactéries résistent à la bactéricidie malgré des concentrations élevées.",
                "CMB augmente fortement sans que CMI change.",
            ),
        ],
    ):
        with col:
            st.markdown(
                f"""
            <div class="ratio-card" style="background:{bg};border-color:{color};">
              <div class="ratio-pill" style="background:{color};">{ratio}</div>
              <div style="font-weight:700;color:{color};font-size:1.05rem;margin-bottom:10px;">{label}</div>
              <p style="color:#475569;font-size:0.88rem;line-height:1.7;margin:0;">{desc}</p>
              {"" if not note else f'<p style="color:#64748b;font-size:0.80rem;font-style:italic;margin-top:10px;">{note}</p>'}
            </div>
            """,
                unsafe_allow_html=True,
            )

    # Gauges exemples
    st.markdown(
        "<br><strong style='color:#1e3a5f;'>Exemples de ratios CMB/CMI – Molécules représentatives</strong>",
        unsafe_allow_html=True,
    )
    gc1, gc2, gc3, gc4 = st.columns(4)
    for col, (val, lbl, c) in zip(
        [gc1, gc2, gc3, gc4],
        [
            (2.58, "Meropenem\n(Bactéricide strict)", "#1a56db"),
            (2.60, "Azithromycin\n(Double activité)", "#0ea5e9"),
            (4.0, "Linezolid\n(Bactériostatique)", "#64748b"),
            (40.0, "Tolérance\n(exemple)", "#94a3b8"),
        ],
    ):
        with col:
            _pc(_gauge_ratio(val, lbl, c))

    _llm_modal_button("llm2")

    section_divider()

    # ══════════════════════════════════════════════════════════════════════════
    # 6. CLASSIFICATION COMPLÈTE
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("## 📋 Classification Complète des Classes Antibiotiques")
    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        st.markdown(
            '<div class="section-card" style="border-top:4px solid #1a56db;"><h4 style="color:#1a56db;margin-top:0;">☠️ Bactéricides Stricts</h4></div>',
            unsafe_allow_html=True,
        )
        _list_grid(BACTERICIDAL_CLASSES, "dot-bactericide", "item-bactericide")
    with col2:
        st.markdown(
            '<div class="section-card" style="border-top:4px solid #64748b;"><h4 style="color:#64748b;margin-top:0;">⏸️ Bactériostatiques</h4></div>',
            unsafe_allow_html=True,
        )
        _list_grid(BACTERIOSTATIC_CLASSES, "dot-bacteriostatic", "item-bacteriostatic")
    with col3:
        st.markdown(
            '<div class="section-card" style="border-top:4px solid #0ea5e9;"><h4 style="color:#0ea5e9;margin-top:0;">⚡ Double Activité</h4></div>',
            unsafe_allow_html=True,
        )
        _list_grid(list(dict.fromkeys(DUAL_CLASSES)), "dot-dual", "item-dual")

    section_divider()

    # ══════════════════════════════════════════════════════════════════════════
    # 7. RÉFÉRENCE vs CARD
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("## 🔄 Bactéricides Stricts : Référence Littérature vs CARD")
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
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown(
            '<div class="section-card" style="border-top:4px solid #64748b;"><h4 style="color:#64748b;margin-top:0;">📚 Bactéricides Stricts (Référence littérature)</h4></div>',
            unsafe_allow_html=True,
        )
        _list_grid(ref_list, "dot-bacteriostatic", "item-bacteriostatic")
    with col2:
        st.markdown(
            '<div class="section-card" style="border-top:4px solid #1a56db;"><h4 style="color:#1a56db;margin-top:0;">🗄️ Bactéricides Stricts (CARD – noms officiels)</h4></div>',
            unsafe_allow_html=True,
        )
        _list_grid(BACTERICIDAL_CLASSES, "dot-bactericide", "item-bactericide")

    section_divider()

    # ══════════════════════════════════════════════════════════════════════════
    # 8. RÉSULTATS FINAUX CARD
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("## 🏆 Résultats Finaux CARD – Distribution des Classes")

    # ── Donut + compteurs ──
    st.markdown("### 🥧 Distribution Globale des 46 Classes CARD")
    col_d1, col_d2 = st.columns([1.3, 1], gap="large")
    with col_d1:
        _pc(_donut_distribution())
    with col_d2:
        st.markdown(
            """
        <div class="section-card" style="margin-top:16px;">
          <h4 style="color:#1e3a5f;margin-top:0;">📊 Répartition sur 46 classes</h4>
          <div style="display:flex;flex-direction:column;gap:10px;margin-top:12px;">
            <div class="stat-inline" style="background:#eff6ff;border-left:4px solid #1a56db;">
              <span style="font-size:1.6rem;font-weight:900;color:#1a56db;min-width:36px;">8</span>
              <div><strong style="color:#1a56db;font-size:0.85rem;">Bactéricides Stricts</strong><br>
              <span style="color:#64748b;font-size:0.78rem;">17 % des 46 classes CARD</span></div>
            </div>
            <div class="stat-inline" style="background:#f0f9ff;border-left:4px solid #0ea5e9;">
              <span style="font-size:1.6rem;font-weight:900;color:#0ea5e9;min-width:36px;">2</span>
              <div><strong style="color:#0369a1;font-size:0.85rem;">Double Activité</strong><br>
              <span style="color:#64748b;font-size:0.78rem;">4 % — aminoglycosides + fluoroquinolones</span></div>
            </div>
            <div class="stat-inline" style="background:#f8fafc;border-left:4px solid #64748b;">
              <span style="font-size:1.6rem;font-weight:900;color:#64748b;min-width:36px;">9</span>
              <div><strong style="color:#64748b;font-size:0.85rem;">Bactériostatiques</strong><br>
              <span style="color:#64748b;font-size:0.78rem;">20 % des classes</span></div>
            </div>
            <div class="stat-inline" style="background:#f8fafc;border-left:4px solid #e2e8f0;">
              <span style="font-size:1.6rem;font-weight:900;color:#94a3b8;min-width:36px;">27</span>
              <div><strong style="color:#94a3b8;font-size:0.85rem;">Non déterminés</strong><br>
              <span style="color:#64748b;font-size:0.78rem;">59 % — activité non établie</span></div>
            </div>
          </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── 2 blocs listes ──
    st.markdown("### 🗂️ Détail par Catégorie CARD")
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown(
            """
        <div class="card-result-block" style="background:#eff6ff;border-color:#1a56db;">
          <h4 style="color:#1a56db;margin-top:0;">🗄️ Bactéricides CARD — 10 classes</h4>
          <p style="color:#475569;font-size:0.84rem;margin-bottom:14px;">
          Toutes les classes bactéricides identifiées, incluant les classes à double activité
          (aminoglycosides, fluoroquinolones).
          </p>
        </div>
        """,
            unsafe_allow_html=True,
        )
        _list_grid(CARD_BACTERICIDE_LIST, "dot-bactericide", "item-bactericide")

    with col2:
        st.markdown(
            """
        <div class="card-result-block" style="background:#fef3c7;border-color:#d97706;">
          <h4 style="color:#92400e;margin-top:0;">⭐ Bactéricides Stricts CARD — 8 classes</h4>
          <p style="color:#475569;font-size:0.84rem;margin-bottom:14px;">
          Sous-ensemble dont l'activité bactéricide est systématique et confirmée.
          Exclut aminoglycosides et fluoroquinolones (double activité).
          </p>
        </div>
        """,
            unsafe_allow_html=True,
        )
        _list_grid(CARD_BACTERICIDE_STRICT_LIST, "dot-bactericide", "item-bactericide")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Histogramme global ARO (toutes classes) ──
    st.markdown("### 📊 Distribution Complète des Gènes ARO par Classe (CARD)")
    _pc(_bar_aro_all())

    # ── Triangle discussion ──
    st.markdown(
        """
    <div class="warn-triangle">
      <h4>⚠️ Discussion – Importance Clinique & Classes CARD</h4>
      <p style="margin:0 0 12px;">
      <strong>1. Importance clinique des bactéricides stricts :</strong>
      Les 8 classes bactéricides strictes (carbapénèmes, céphalosporines, glycopeptides, nitroimidazoles,
      pénicillines β-lactamines, acide phosphonique, rifamycines, monobactams) constituent la
      <strong>première ligne de défense</strong> dans les infections sévères et chez les patients immunodéprimés.
      Leur effet létal direct et irréversible est indispensable lorsque le système immunitaire ne peut
      suppléer à l'arrêt du traitement.
      </p>
      <p style="margin:0 0 12px;">
      <strong>2. Rôle crucial des classes à double activité dans CARD :</strong>
      Les <strong>aminoglycosides</strong> (303 gènes ARO) et les <strong>fluoroquinolones</strong>
      (307 gènes ARO) — classées à double activité — sont parmi les plus représentées dans CARD.
      Bactéricides à fortes concentrations, elles génèrent une pression de sélection majeure et
      une résistance étendue documentée dans le résistome bactérien mondial.
      </p>
      <p style="margin:0;">
      <strong>→ Conclusion :</strong> La distinction bactéricide strict vs double activité est fondamentale
      pour la pratique clinique et l'analyse de la résistance : elle guide le choix thérapeutique et
      éclaire la pression de sélection exercée sur le résistome bactérien.
      </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # ══════════════════════════════════════════════════════════════════════════
    # CLASSIFICATION COMPLÈTE
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("## Classification Complete des Classes Antibiotiques")

    for uid, color, border, bg, t_icon, t_str, items in [
        (
            "fcb",
            _P["bact"],
            _P["bact_m"],
            _P["bact_l"],
            "☠️",
            "Bactericides Stricts",
            BACTERICIDAL_CLASSES,
        ),
        (
            "fcs",
            _P["stat"],
            _P["stat_m"],
            _P["stat_l"],
            "⏸️",
            "Bacteriostatiques",
            BACTERIOSTATIC_CLASSES,
        ),
        (
            "fcd",
            _P["dual"],
            _P["dual_m"],
            _P["dual_l"],
            "⚡",
            "Double Activite",
            list(dict.fromkeys(DUAL_CLASSES)),
        ),
    ]:
        st.markdown(
            f"""
        <div style="background:{bg};border:1.5px solid {border};border-radius:14px;
                    padding:16px 20px 10px;margin-bottom:6px;">
          <h4 style="color:{color};margin:0;">{t_icon} {t_str}</h4>
        </div>""",
            unsafe_allow_html=True,
        )
        _toggle(
            f"{uid}_l",
            f"   Afficher les classes — {t_str}",
            f"   Masquer les classes — {t_str}",
            lambda c=color, b=border, bg_=bg, it=items: _big_list(it, c, b, bg_),
        )
        st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    section_divider()

    # ══════════════════════════════════════════════════════════════════════════
    # RÉFÉRENCE vs CARD
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("## Bactericides Stricts : Reference Litterature vs CARD")
    ref_list = [
        "Penicillines",
        "Cephalosporines",
        "Carbapenemes",
        "Quinolones",
        "Glycopeptides",
        "Lipopeptides",
        "Nitroimidazoles",
        "Polymyxines",
        "Phosphonic acid antibiotics",
        "Rifamycines",
        "Monobactam",
    ]
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown(
            f"""
        <div style="background:{_P['stat_l']};border:1.5px solid {_P['stat_m']};
                    border-radius:14px;padding:16px 20px 10px;margin-bottom:6px;">
          <h4 style="color:{_P['stat']};margin:0;">Reference litterature</h4>
        </div>""",
            unsafe_allow_html=True,
        )
        _toggle(
            "rl",
            "   Afficher la liste litterature",
            "   Masquer la liste litterature",
            lambda: _big_list(ref_list, _P["stat"], _P["stat_m"], _P["stat_l"]),
        )
    with col2:
        st.markdown(
            f"""
        <div style="background:{_P['bact_l']};border:1.5px solid {_P['bact_m']};
                    border-radius:14px;padding:16px 20px 10px;margin-bottom:6px;">
          <h4 style="color:{_P['bact']};margin:0;">CARD (noms officiels)</h4>
        </div>""",
            unsafe_allow_html=True,
        )
        _toggle(
            "rc",
            "   Afficher la liste CARD",
            "   Masquer la liste CARD",
            lambda: _big_list(
                BACTERICIDAL_CLASSES, _P["bact"], _P["bact_m"], _P["bact_l"]
            ),
        )

    section_divider()

    # ══════════════════════════════════════════════════════════════════════════
    # RÉSULTATS FINAUX CARD
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("## Resultats Finaux CARD – Distribution des Classes")
    st.markdown("### Distribution Globale des 46 Classes CARD")

    col_d1, col_d2 = st.columns([1.3, 1], gap="large")
    with col_d1:
        _toggle(
            "donut",
            "   Afficher le graphique de distribution",
            "   Masquer le graphique",
            lambda: _pc(_donut_distribution()),
        )
    with col_d2:
        st.markdown(
            f"""
        <div class="section-card" style="margin-top:8px;">
          <h4 style="color:{_P['txt']};margin-top:0;">Repartition sur 46 classes</h4>
          <div style="margin-top:14px;">
            <div class="stat-inline"
                 style="background:{_P['bact_l']};border-color:{_P['bact']};">
              <span class="stat-val" style="color:{_P['bact']};">8</span>
              <div>
                <div class="stat-lbl" style="color:{_P['bact']};">Bactericides Stricts</div>
                <div class="stat-sub">17 % des 46 classes CARD</div>
              </div>
            </div>
            <div class="stat-inline"
                 style="background:{_P['dual_l']};border-color:{_P['dual']};">
              <span class="stat-val" style="color:{_P['dual']};">2</span>
              <div>
                <div class="stat-lbl" style="color:{_P['dual']};">Double Activite</div>
                <div class="stat-sub">4 % — aminoglycosides + fluoroquinolones</div>
              </div>
            </div>
            <div class="stat-inline"
                 style="background:{_P['stat_l']};border-color:{_P['stat']};">
              <span class="stat-val" style="color:{_P['stat']};">9</span>
              <div>
                <div class="stat-lbl" style="color:{_P['stat']};">Bacteriostatiques</div>
                <div class="stat-sub">20 % des classes</div>
              </div>
            </div>
            <div class="stat-inline"
                 style="background:#f8fafc;border-color:#e2e8f0;">
              <span class="stat-val" style="color:{_P['und']};">27</span>
              <div>
                <div class="stat-lbl" style="color:{_P['und']};">Non determines</div>
                <div class="stat-sub">59 % — activite non etablie</div>
              </div>
            </div>
          </div>
        </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Detail par Categorie CARD")

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown(
            f"""
        <div class="card-result-block"
             style="background:{_P['bact_l']};border-color:{_P['bact']};">
          <h4 style="color:{_P['bact']};margin-top:0;">Bactericides CARD — 10 classes</h4>
          <p style="color:{_P['txt_m']};font-size:0.84rem;margin-bottom:6px;">
            Incluant les classes a double activite (aminoglycosides, fluoroquinolones).
          </p>
        </div>""",
            unsafe_allow_html=True,
        )
        _toggle(
            "c10",
            "   Afficher les 10 classes",
            "   Masquer",
            lambda: _big_list(
                CARD_BACTERICIDE_LIST, _P["bact"], _P["bact_m"], _P["bact_l"]
            ),
        )
    with col2:
        st.markdown(
            f"""
        <div class="card-result-block"
             style="background:{_P['strict_l']};border-color:{_P['strict']};">
          <h4 style="color:{_P['strict']};margin-top:0;">Bactericides Stricts CARD — 8 classes</h4>
          <p style="color:{_P['txt_m']};font-size:0.84rem;margin-bottom:6px;">
            Sous-ensemble confirme — exclut aminoglycosides et fluoroquinolones.
          </p>
        </div>""",
            unsafe_allow_html=True,
        )
        _toggle(
            "c8",
            "   Afficher les 8 classes",
            "   Masquer",
            lambda: _big_list(
                CARD_BACTERICIDE_STRICT_LIST,
                _P["strict"],
                _P["strict_m"],
                _P["strict_l"],
            ),
        )

    st.markdown("<br>", unsafe_allow_html=True)
