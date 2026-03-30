# definitions.py
import streamlit as st
from utils.helpers import info_box
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

_ACT_MAP = {
    "Cephalosporin": "Bactericide strict",
    "Penicillin beta-lactam": "Bactericide strict",
    "Carbapenem": "Bactericide strict",
    "Monobactam": "Bactericide strict",
    "Glycopeptide": "Bactericide strict",
    "Rifamycin": "Bactericide strict",
    "Phosphonic acid": "Bactericide strict",
    "Nitroimidazole": "Bactericide strict",
    "Fluoroquinolone": "Double activite",
    "Aminoglycoside": "Double activite",
    "Glycylcycline": "Double activite",
    "Macrolide": "Bacteriostatique",
    "Tetracycline": "Bacteriostatique",
    "Phenicol": "Bacteriostatique",
    "Lincosamide": "Bacteriostatique",
    "Streptogramin": "Bacteriostatique",
    "Oxazolidinone": "Bacteriostatique",
    "Sulfonamide": "Bacteriostatique",
    "Peptide": "Non determine",
}

# ── Palette harmonisée ──
_P = {
    "bact": "#1d4ed8",
    "bact_l": "#eff6ff",
    "bact_m": "#bfdbfe",
    "dual": "#0891b2",
    "dual_l": "#ecfeff",
    "dual_m": "#a5f3fc",
    "stat": "#475569",
    "stat_l": "#f8fafc",
    "stat_m": "#e2e8f0",
    "strict": "#7c3aed",
    "strict_l": "#f5f3ff",
    "strict_m": "#ddd6fe",
    "und": "#94a3b8",
    "green": "#059669",
    "red": "#dc2626",
    "amber": "#d97706",
    "txt": "#0f172a",
    "txt_m": "#334155",
    "txt_l": "#64748b",
    "border": "#e2e8f0",
    "surface": "#ffffff",
}

_COLOR_MAP = {
    "Bactericide strict": _P["bact"],
    "Double activite": _P["dual"],
    "Bacteriostatique": _P["stat"],
    "Non determine": _P["und"],
}

PLOTLY_LAYOUT = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10, r=10, t=40, b=10),
    font=dict(family="DM Sans, sans-serif", color=_P["txt_m"]),
)


# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────


def _inject_def_css():
    st.markdown(
        """
    <style>
    /* ── BLOC PRINCIPAL ── */
    .def-block {
        background: #ffffff;
        border-radius: 20px;
        border: 1.5px solid #e2e8f0;
        overflow: hidden;
        box-shadow: 0 4px 24px rgba(15,23,42,0.07);
        margin-bottom: 12px;
    }

    /* ── HEADER DU BLOC ── */
    .def-block-header {
        display: flex;
        align-items: center;
        gap: 20px;
        padding: 28px 32px 24px;
        border-bottom: 1.5px solid #e2e8f0;
    }
    .def-block-icon {
        width: 60px; height: 60px;
        border-radius: 16px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.8rem;
        flex-shrink: 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }
    .def-block-title h2 {
        margin: 0 0 5px;
        font-size: 1.35rem;
        font-weight: 800;
        letter-spacing: -0.3px;
    }
    .def-block-title p {
        margin: 0;
        font-size: 0.88rem;
        color: #64748b;
        font-style: italic;
    }

    /* ── CORPS DU BLOC ── */
    .def-block-body {
        padding: 22px 32px 24px;
    }

    /* ── MÉCANISMES ── */
    .mech-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin-bottom: 18px;
    }
    .mech-item {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 13px 16px;
        border-radius: 12px;
        border: 1.5px solid;
        font-size: 0.88rem;
        color: #334155;
        line-height: 1.6;
    }
    .mech-num {
        width: 26px; height: 26px;
        border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.75rem; font-weight: 800;
        color: white; flex-shrink: 0; margin-top: 1px;
    }

    /* ── CRITÈRE ── */
    .def-criterion {
        display: flex;
        align-items: center;
        gap: 12px;
        border-radius: 12px;
        padding: 14px 18px;
        font-size: 0.88rem;
        font-weight: 600;
        border: 1.5px solid;
    }

    /* ── LISTE GRANDE ET CLAIRE ── */
    .big-list {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 10px;
        padding: 16px 0 8px;
        animation: fadeInList .25s ease;
    }
    .big-list-item {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 14px 18px;
        border-radius: 14px;
        border: 1.5px solid;
        background: #ffffff;
        font-size: 0.92rem;
        font-weight: 600;
        color: #0f172a;
        transition: transform .18s, box-shadow .18s;
        cursor: default;
    }
    .big-list-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.10);
    }
    .big-list-dot {
        width: 12px; height: 12px;
        border-radius: 50%;
        flex-shrink: 0;
    }
    @keyframes fadeInList {
        from { opacity: 0; transform: translateY(-6px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* ── RATIO CARDS ── */
    .ratio-card {
        border-radius: 14px;
        padding: 22px 20px;
        text-align: center;
        border-width: 2px;
        border-style: solid;
    }
    .ratio-pill {
        display: inline-block; color: white;
        font-size: 1rem; font-weight: 800;
        border-radius: 8px; padding: 8px 16px;
        margin-bottom: 12px; width: 100%;
    }

    /* ── STAT INLINE ── */
    .stat-inline {
        display: flex; align-items: center; gap: 14px;
        padding: 12px 16px; border-radius: 12px;
        margin-bottom: 10px; border-left: 4px solid;
    }
    .stat-val { font-size: 1.8rem; font-weight: 900; min-width: 40px; line-height: 1; }
    .stat-lbl { font-size: 0.85rem; font-weight: 700; }
    .stat-sub { font-size: 0.77rem; margin-top: 2px; color: #64748b; }

    /* ── CARD RESULT ── */
    .card-result-block {
        border-radius: 16px; padding: 22px 24px;
        border: 2px solid; margin-bottom: 10px;
    }

    /* ── MODAL LLM ── */
    .modal-bg {
        display: none; position: fixed; inset: 0; z-index: 9999;
        background: rgba(2,30,70,.55); backdrop-filter: blur(6px);
        align-items: center; justify-content: center;
    }
    .modal-bg.open { display: flex; }
    .modal-inner {
        background: #fff; border-radius: 20px; padding: 32px 36px;
        max-width: 640px; width: 94%; max-height: 85vh; overflow-y: auto;
        box-shadow: 0 24px 80px rgba(2,62,138,.28);
        position: relative; animation: fadeInList .25s ease;
    }
    .modal-close-btn {
        position: absolute; top: 14px; right: 18px;
        background: none; border: none; font-size: 1.2rem;
        cursor: pointer; color: #64748b; transition: color .2s;
    }
    .modal-close-btn:hover { color: #dc2626; }

    /* ── VIZ BTN ── */
    .viz-btn {
        display: inline-flex; align-items: center; gap: 8px;
        background: linear-gradient(135deg, #1d4ed8, #0891b2);
        color: #fff; border: none; border-radius: 30px; padding: 9px 20px;
        font-size: 0.83rem; font-weight: 600; cursor: pointer; margin-top: 12px;
        box-shadow: 0 4px 14px rgba(29,78,216,.22);
        transition: transform .2s, box-shadow .2s;
    }
    .viz-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 22px rgba(29,78,216,.32); }

    /* ── WARN TRIANGLE ── */
    .warn-triangle {
        background: linear-gradient(135deg, #fff7ed, #fef3c7);
        border-left: 5px solid #f97316; border-radius: 14px;
        padding: 20px 24px; margin-top: 20px;
        font-size: 0.9rem; color: #78350f; line-height: 1.8;
    }
    .warn-triangle h4 { margin: 0 0 10px; color: #c2410c; font-size: 1rem; }
    </style>
    """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS INTERNES
# ─────────────────────────────────────────────────────────────────────────────


def _pc(fig):
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _big_list(items, color, border_color, bg_color):
    html = "".join(
        f'<div class="big-list-item" style="border-color:{border_color};background:{bg_color};">'
        f'<span class="big-list-dot" style="background:{color};box-shadow:0 0 0 3px {border_color};"></span>'
        f"<span>{item}</span>"
        f"</div>"
        for item in items
    )
    st.markdown(f'<div class="big-list">{html}</div>', unsafe_allow_html=True)


def _toggle(uid, label_show, label_hide, render_fn):
    key = f"tgl_{uid}"
    if key not in st.session_state:
        st.session_state[key] = False
    label = label_hide if st.session_state[key] else label_show
    if st.button(label, key=f"btn_{uid}", use_container_width=True):
        st.session_state[key] = not st.session_state[key]
        st.rerun()
    if st.session_state[key]:
        render_fn()


# ─────────────────────────────────────────────────────────────────────────────
# CHARTS
# ─────────────────────────────────────────────────────────────────────────────


def _bar_bactericide_only():
    keys = [
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
    bact = {k: v for k, v in CARD_ARO_GENES.items() if k in keys}
    classes = list(bact.keys())
    genes = list(bact.values())
    colors = [
        _P["dual"] if c in ["Aminoglycoside", "Fluoroquinolone"] else _P["bact"]
        for c in classes
    ]
    fig = go.Figure(
        go.Bar(
            x=classes,
            y=genes,
            marker=dict(color=colors, line=dict(color="white", width=1.5)),
            text=[f"{g:,}" for g in genes],
            textposition="outside",
            textfont=dict(size=11, color=_P["txt_m"]),
            hovertemplate="<b>%{x}</b><br>ARO : <b>%{y:,}</b><extra></extra>",
        )
    )
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(
            text="Classes Bactéricides CARD — Gènes ARO",
            font=dict(size=14, color=_P["bact"]),
        ),
        xaxis=dict(tickangle=-25, tickfont=dict(size=11), showgrid=False),
        yaxis=dict(
            showgrid=True,
            gridcolor="#f0f4f8",
            title="Gènes ARO",
            tickfont=dict(size=11),
        ),
        height=380,
        showlegend=False,
    )
    return fig


def _bar_bactericide_strict():
    keys = [
        "Cephalosporin",
        "Penicillin beta-lactam",
        "Carbapenem",
        "Monobactam",
        "Glycopeptide",
        "Rifamycin",
        "Phosphonic acid",
        "Nitroimidazole",
    ]
    strict = {k: v for k, v in CARD_ARO_GENES.items() if k in keys}
    fig = go.Figure(
        go.Bar(
            x=list(strict.keys()),
            y=list(strict.values()),
            marker=dict(
                color=_P["strict"], opacity=0.87, line=dict(color="white", width=1.5)
            ),
            text=[f"{g:,}" for g in strict.values()],
            textposition="outside",
            textfont=dict(size=11, color=_P["txt_m"]),
            hovertemplate="<b>%{x}</b><br>ARO : <b>%{y:,}</b><extra></extra>",
        )
    )
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(
            text="Bactéricides Stricts CARD — Gènes ARO",
            font=dict(size=14, color=_P["strict"]),
        ),
        xaxis=dict(tickangle=-20, tickfont=dict(size=11), showgrid=False),
        yaxis=dict(
            showgrid=True,
            gridcolor="#f0f4f8",
            title="Gènes ARO",
            tickfont=dict(size=11),
        ),
        height=360,
        showlegend=False,
    )
    return fig


def _bar_bacteriostatic():
    keys = [
        "Macrolide",
        "Tetracycline",
        "Phenicol",
        "Lincosamide",
        "Streptogramin",
        "Oxazolidinone",
        "Sulfonamide",
    ]
    bstatic = {k: v for k, v in CARD_ARO_GENES.items() if k in keys}
    fig = go.Figure(
        go.Bar(
            x=list(bstatic.keys()),
            y=list(bstatic.values()),
            marker=dict(
                color=_P["stat"], opacity=0.83, line=dict(color="white", width=1.5)
            ),
            text=[f"{g:,}" for g in bstatic.values()],
            textposition="outside",
            textfont=dict(size=11, color=_P["txt_m"]),
            hovertemplate="<b>%{x}</b><br>ARO : <b>%{y:,}</b><extra></extra>",
        )
    )
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(
            text="Bactériostatiques CARD — Gènes ARO",
            font=dict(size=14, color=_P["stat"]),
        ),
        xaxis=dict(tickangle=-20, tickfont=dict(size=11), showgrid=False),
        yaxis=dict(
            showgrid=True,
            gridcolor="#f0f4f8",
            title="Gènes ARO",
            tickfont=dict(size=11),
        ),
        height=340,
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
                color=_P["dual"], opacity=0.87, line=dict(color="white", width=1.5)
            ),
            text=[f"{g:,}" for g in dual_aro.values()],
            textposition="outside",
            textfont=dict(size=11, color=_P["txt_m"]),
            hovertemplate="<b>%{x}</b><br>ARO : <b>%{y:,}</b><extra></extra>",
        )
    )
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(
            text="Classes Double Activité — Gènes ARO",
            font=dict(size=14, color=_P["dual"]),
        ),
        xaxis=dict(tickfont=dict(size=11), showgrid=False),
        yaxis=dict(
            showgrid=True,
            gridcolor="#f0f4f8",
            title="Gènes ARO",
            tickfont=dict(size=11),
        ),
        height=340,
        showlegend=False,
    )
    return fig


def _donut_distribution():
    labels = [
        "Bactéricide strict",
        "Double activité",
        "Bactériostatique",
        "Non déterminés",
    ]
    values = [8, 2, 9, 27]
    colors = [_P["bact"], _P["dual"], _P["stat"], "#e2e8f0"]
    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.55,
            marker=dict(colors=colors, line=dict(color="#fff", width=3)),
            textinfo="label+percent",
            textfont=dict(size=12, family="DM Sans", color=_P["txt"]),
            hovertemplate="<b>%{label}</b><br>%{value} classes (%{percent})<extra></extra>",
            pull=[0.05, 0.03, 0, 0],
        )
    )
    fig.add_annotation(
        text="<b>46</b><br>classes CARD",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=14, color=_P["txt"], family="DM Sans"),
    )
    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=380,
        legend=dict(
            orientation="v",
            x=1.02,
            y=0.5,
            font=dict(size=12, color=_P["txt_m"], family="DM Sans"),
        ),
        margin=dict(l=0, r=10, t=20, b=0),
    )
    return fig


def _bar_aro_all():
    classes = list(CARD_ARO_GENES.keys())
    genes = list(CARD_ARO_GENES.values())
    bar_colors = [_COLOR_MAP[_ACT_MAP[c]] for c in classes]
    fig = go.Figure()
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
            textfont=dict(size=10, color=_P["txt_m"]),
            hovertemplate="<b>%{y}</b><br>ARO : <b>%{x:,}</b><extra></extra>",
            showlegend=False,
        )
    )
    for act, col in _COLOR_MAP.items():
        fig.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                marker=dict(size=11, color=col, symbol="square"),
                name=act,
                showlegend=True,
            )
        )
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(
            text="Distribution des Gènes ARO par Classe (CARD – 19 classes documentées)",
            font=dict(size=14, color=_P["txt"]),
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="#f0f4f8",
            title="Nombre de gènes ARO",
            tickfont=dict(size=10),
        ),
        yaxis=dict(tickfont=dict(size=11, color=_P["txt"])),
        height=600,
        legend=dict(orientation="h", x=0, y=-0.08, font=dict(size=11)),
        margin=dict(l=10, r=90, t=40, b=10),
    )
    return fig


def _gauge_ratio(value, label, color):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={
                "text": label,
                "font": {"size": 11, "color": _P["txt"], "family": "DM Sans"},
            },
            number={
                "font": {"size": 20, "color": color, "family": "DM Sans"},
                "suffix": "x",
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
        margin=dict(l=10, r=10, t=44, b=10), paper_bgcolor="rgba(0,0,0,0)", height=200
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# MODAL LLM
# ─────────────────────────────────────────────────────────────────────────────


def _llm_modal_button(uid="a"):
    green = _P["green"]
    red = _P["red"]
    amber = _P["amber"]
    bact = _P["bact"]
    bm = _P["bact_m"]
    tm = _P["txt_m"]
    st.markdown(
        f"""
    <button class="viz-btn"
            onclick="document.getElementById('llmM_{uid}').classList.add('open')">
        Voir detail LLM
    </button>
    <div class="modal-bg" id="llmM_{uid}"
         onclick="if(event.target===this)this.classList.remove('open')">
      <div class="modal-inner">
        <button class="modal-close-btn"
                onclick="document.getElementById('llmM_{uid}').classList.remove('open')">X</button>
        <h3 style="color:{bact};margin-top:0;">LLMs Testes - Analyse Critique</h3>

        <div style="border:1.5px solid {bm};border-radius:12px;padding:16px;margin-bottom:12px;">
          <strong style="color:{bact};">BioGPT (Microsoft)</strong>
          <p style="color:{tm};font-size:0.85rem;margin:6px 0 8px;">
            Pre-entraine sur millions d'articles PubMed.
          </p>
          <div style="background:#fef2f2;border-radius:8px;padding:9px 12px;
               font-size:0.82rem;color:{red};border-left:3px solid {red};">
            Biais systematique : classe TOUT bactericide.<br>
            Hallucinations frequentes sur les classes rares.
          </div>
        </div>

        <div style="border:1.5px solid #ede9fe;border-radius:12px;padding:16px;margin-bottom:12px;">
          <strong style="color:#7c3aed;">BioMedLM (Stanford CRFM)</strong>
          <p style="color:{tm};font-size:0.85rem;margin:6px 0 8px;">
            Corpus medicaux et pharmacologiques dedies.
          </p>
          <div style="background:#fef2f2;border-radius:8px;padding:9px 12px;
               font-size:0.82rem;color:{red};border-left:3px solid {red};">
            Resultats incoherents : confusion entre classes similaires.
          </div>
        </div>

        <div style="border:1.5px solid #fde68a;border-radius:12px;padding:16px;margin-bottom:12px;">
          <strong style="color:{amber};">Mistral-7B-Instruct-v0.3</strong>
          <p style="color:{tm};font-size:0.85rem;margin:6px 0 8px;">
            Modele generaliste 7B parametres Mistral AI, mode instruction.
          </p>
          <div style="background:#fef2f2;border-radius:8px;padding:9px 12px;
               font-size:0.82rem;color:{red};border-left:3px solid {red};">
            NON PERFORMANT sur la classification fine.<br>
            Confusions frequentes entre sous-classes.
          </div>
        </div>

        <div style="background:#f0fdf4;border-radius:10px;padding:12px 16px;
             font-size:0.84rem;color:#14532d;border-left:4px solid {green};">
          <strong>Conclusion :</strong> Aucun LLM teste n'est suffisant seul.
          Validation basee sur le <strong>ratio CMB/CMI</strong>
          et la <strong>litterature biomedicale</strong>.
        </div>
      </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# BLOC DÉFINITION — affichage vertical
# ─────────────────────────────────────────────────────────────────────────────


def _def_block(
    uid,
    icon,
    title,
    subtitle,
    header_bg,
    header_border,
    icon_bg_start,
    icon_bg_end,
    color,
    mechs,
    crit_icon,
    crit_text,
    light_bg,
    mid_bg,
    list_items,
    chart_fn,
):
    """
    Full-width definition block with:
    - Visual header (icon + title)
    - 2x2 mechanism grid
    - Criterion bar
    - Button 1: toggle list
    - Button 2: toggle chart
    """
    # ── build mech items html ──
    mechs_html = ""
    for i, m in enumerate(mechs, 1):
        mechs_html += (
            f'<div class="mech-item" '
            f'style="background:{light_bg};border-color:{mid_bg};">'
            f'<div class="mech-num" style="background:{color};">{i}</div>'
            f"<span>{m}</span></div>"
        )

    st.markdown(
        f"""
    <div class="def-block">
      <div class="def-block-header"
           style="background:{header_bg};border-bottom-color:{header_border};">
        <div class="def-block-icon"
             style="background:linear-gradient(135deg,{icon_bg_start},{icon_bg_end});">
          {icon}
        </div>
        <div class="def-block-title">
          <h2 style="color:{color};">{title}</h2>
          <p>{subtitle}</p>
        </div>
      </div>
      <div class="def-block-body">
        <div class="mech-grid">{mechs_html}</div>
        <div class="def-criterion"
             style="background:{light_bg};border-color:{mid_bg};color:{color};">
          <span style="font-size:1.3rem;flex-shrink:0;">{crit_icon}</span>
          <span>{crit_text}</span>
        </div>
      </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # ── Bouton 1 : liste ──
    _toggle(
        f"{uid}_list",
        "   Afficher la liste des classes selon les références scientifiques",
        "   Masquer la liste des classes",
        lambda c=color, b=mid_bg, bg=light_bg, it=list_items: _big_list(it, c, b, bg),
    )

    st.markdown("<div style='height:0px;'></div>", unsafe_allow_html=True)

    # ── Bouton 2 : graphique ──
    _toggle(
        f"{uid}_chart",
        "   Afficher la distribution (graphique)",
        "   Masquer la distribution",
        lambda fn=chart_fn: _pc(fn()),
    )

    st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# RENDER PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────


def render():
    _inject_def_css()

    st.markdown("# Definitions et Classification")
    st.markdown(
        f'<p style="color:{_P["txt_l"]};font-size:1.05rem;margin-bottom:28px;">'
        "Cadre theorique de la classification bactericide/bacteriostatique, "
        "listes des classes par activite et visualisations CARD.</p>",
        unsafe_allow_html=True,
    )

    st.markdown("## Cadre Theorique")

    # ══════════════════════════════════════════════════════════════════════════
    # BLOC 1 — BACTÉRICIDE
    # ══════════════════════════════════════════════════════════════════════════
    _def_block(
        uid="bact",
        icon="☠️",
        title="BACTERICIDE",
        subtitle="Detruit les bacteries — effet letal direct et irreversible",
        header_bg=_P["bact_l"],
        header_border=_P["bact_m"],
        icon_bg_start=_P["bact"],
        icon_bg_end=_P["dual"],
        color=_P["bact"],
        mechs=[
            "Inhibition de la <strong>synthese de la paroi bacterienne</strong>",
            "Alteration de la <strong>membrane bacterienne</strong>",
            "Inhibition des <strong>enzymes bacteriennes essentielles</strong>",
            "Inhibition de la <strong>traduction des proteines</strong>",
        ],
        crit_icon="📐",
        crit_text="Reduction &ge; 3 log&#8321;&#8320; UFC/mL par rapport a l'inoculum initial",
        light_bg=_P["bact_l"],
        mid_bg=_P["bact_m"],
        list_items=BACTERICIDAL_CLASSES,
        chart_fn=_bar_bactericide_only,
    )

    # ══════════════════════════════════════════════════════════════════════════
    # BLOC 2 — BACTÉRIOSTATIQUE
    # ══════════════════════════════════════════════════════════════════════════
    _def_block(
        uid="stat",
        icon="⏸️",
        title="BACTERIOSTATIQUE",
        subtitle="Inhibe la croissance bacterienne — effet reversible, depend du systeme immunitaire",
        header_bg=_P["stat_l"],
        header_border=_P["stat_m"],
        icon_bg_start=_P["stat"],
        icon_bg_end="#64748b",
        color=_P["stat"],
        mechs=[
            "Inhibition de la <strong>synthese des proteines</strong>",
            "Inhibition au niveau du <strong>ribosome 50S</strong>",
            "Liaison au ribosome 50S → <strong>arret de la traduction</strong>",
            "Interference avec la <strong>replication de l'ADN</strong>",
        ],
        crit_icon="⚠️",
        crit_text="La croissance reprend a l'arret du traitement — depend du systeme immunitaire",
        light_bg=_P["stat_l"],
        mid_bg=_P["stat_m"],
        list_items=BACTERIOSTATIC_CLASSES,
        chart_fn=_bar_bacteriostatic,
    )

    # ══════════════════════════════════════════════════════════════════════════
    # BLOC 3 — DOUBLE ACTIVITÉ
    # ══════════════════════════════════════════════════════════════════════════
    _def_block(
        uid="dual",
        icon="⚡",
        title="DOUBLE ACTIVITE",
        subtitle="Bactericide ou bacteriostatique selon le contexte pharmacodynamique",
        header_bg=_P["dual_l"],
        header_border=_P["dual_m"],
        icon_bg_start=_P["dual"],
        icon_bg_end="#0e7490",
        color=_P["dual"],
        mechs=[
            "Depend de la <strong>concentration plasmatique</strong> de l'antibiotique",
            "Influence de la <strong>duree d'exposition</strong> des bacteries",
            "<strong>Nature et sensibilite intrinseque</strong> de la souche bacterienne",
            "Pharmacodynamique et <strong>cibles moleculaires specifiques</strong>",
        ],
        crit_icon="ℹ️",
        crit_text="L'effet bactericide necessite des concentrations superieures a la CMI",
        light_bg=_P["dual_l"],
        mid_bg=_P["dual_m"],
        list_items=list(dict.fromkeys(DUAL_CLASSES)),
        chart_fn=_bar_dual,
    )

    # ══════════════════════════════════════════════════════════════════════════
    # BLOC 4 — BACTÉRICIDES STRICTS
    # ══════════════════════════════════════════════════════════════════════════
    _def_block(
        uid="strict",
        icon="🏆",
        title="BACTERICIDES STRICTS",
        subtitle="Tuent systematiquement — independamment de la concentration et de la phase de croissance",
        header_bg=_P["strict_l"],
        header_border=_P["strict_m"],
        icon_bg_start=_P["strict"],
        icon_bg_end="#6d28d9",
        color=_P["strict"],
        mechs=[
            "Efficaces contre les bacteries en <strong>phase de croissance lente</strong>",
            "Indispensables pour les <strong>infections severes</strong>",
            "Cruciaux pour les <strong>patients immunodeprimes</strong>",
            "Effet letal <strong>direct et irreversible</strong> — sous-groupe des bactericides",
        ],
        crit_icon="🏅",
        crit_text="Exclut aminoglycosides et fluoroquinolones (double activite) — 8 classes confirmees",
        light_bg=_P["strict_l"],
        mid_bg=_P["strict_m"],
        list_items=CARD_BACTERICIDE_STRICT_LIST,
        chart_fn=_bar_bactericide_strict,
    )

    # graphe
    st.markdown(
        """
        <div style="margin-top: 16px;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
                <div style="width: 4px; height: 28px; background: linear-gradient(135deg, #0077b6, #0096c7); border-radius: 4px;"></div>
                <div style="font-size: 1rem; font-weight: 700; color: #023e8a;">Résultat : Classification des 46 classes CARD</div>
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 16px; justify-content: space-between;">
                <div style="flex: 1; min-width: 180px; background: linear-gradient(135deg, #fef2f2, #fee2e2);
                            border-radius: 20px; padding: 24px 20px; text-align: center; border-left: 4px solid #dc2626;">
                    <div style="font-size: 2rem; font-weight: 800; color: #dc2626; margin-bottom: 8px;">10</div>
                    <div style="font-size: 0.8rem; font-weight: 600; color: #7f1a1a;">Bactéricide</div>
                </div>
                <div style="flex: 1; min-width: 180px; background: linear-gradient(135deg, #f0fdf4, #dcfce7);
                            border-radius: 20px; padding: 24px 20px; text-align: center; border-left: 4px solid #16a34a;">
                    <div style="font-size: 2rem; font-weight: 800; color: #16a34a; margin-bottom: 8px;">9</div>
                    <div style="font-size: 0.8rem; font-weight: 600; color: #14532d;">Bactériostatique</div>
                </div>
                <div style="flex: 1; min-width: 180px; background: linear-gradient(135deg, #fffbeb, #fef3c7);
                            border-radius: 20px; padding: 24px 20px; text-align: center; border-left: 4px solid #f59e0b;">
                    <div style="font-size: 2rem; font-weight: 800; color: #f59e0b; margin-bottom: 8px;">6</div>
                    <div style="font-size: 0.8rem; font-weight: 600; color: #78350f;">Double activité</div>
                </div>
                <div style="flex: 1; min-width: 180px; background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
                            border-radius: 20px; padding: 24px 20px; text-align: center; border-left: 4px solid #64748b;">
                    <div style="font-size: 2rem; font-weight: 800; color: #475569; margin-bottom: 8px;">27</div>
                    <div style="font-size: 0.8rem; font-weight: 600; color: #1e293b;">Non déterminées</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # RATIO CMB/CMI
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("## Critere Quantitatif : Ratio CMB/CMI")
    info_box(
        "Le ratio CMB/CMI est le <strong>critere gold standard</strong> pour classer "
        "objectivement un antibiotique. <br> "
        "CMB = Concentration Minimale Bactericide <br> CMI = Concentration Minimale Inhibitrice.",
        kind="info",
    )

    col1, col2, col3 = st.columns(3, gap="medium")
    for col, (bg, color, ratio, label, desc, note) in zip(
        [col1, col2, col3],
        [
            (
                "#fef2f2",
                _P["red"],
                "CMB/CMI ≤ 4",
                "BACTERICIDE",
                "L'antibiotique tue 99,99 % de la population bacterienne.",
                "",
            ),
            (
                "#f0fdf4",
                _P["green"],
                "4 < CMB/CMI < 32",
                "BACTERIOSTATIQUE",
                "L'antibiotique inhibe la croissance sans tuer efficacement les bacteries.",
                "",
            ),
            (
                _P["bact_l"],
                _P["bact"],
                "CMB/CMI ≥ 32",
                "TOLERANCE",
                "Les bacteries resistent a la bactericidie malgre des concentrations elevees.",
                "CMB augmente fortement sans que CMI change.",
            ),
        ],
    ):
        with col:
            st.markdown(
                f"""
            <div class="ratio-card" style="background:{bg};border-color:{color};">
              <div class="ratio-pill" style="background:{color};">{ratio}</div>
              <div style="font-weight:700;color:{color};font-size:1.05rem;
                   margin-bottom:10px;">{label}</div>
              <p style="color:{_P['txt_m']};font-size:0.88rem;
                 line-height:1.7;margin:0;">{desc}</p>
              {"" if not note else
               f'<p style="color:{_P["txt_l"]};font-size:0.80rem;'
               f'font-style:italic;margin-top:10px;">{note}</p>'}
            </div>""",
                unsafe_allow_html=True,
            )

    # ══════════════════════════════════════════════════════════════════════════
    # LLMs
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("## Tests LLMs Specialises")
    info_box(
        "<strong>Resultats critiques :</strong> BioGPT : faux positifs systematiques. "
        "BioMedLM : resultats incoherents. Mistral-7B : non performant. "
        "Necessite de recourir a la litterature et au ratio CMB/CMI.",
        kind="warning",
    )

    _llm_modal_button("llm1")

    tab1, tab2, tab3 = st.tabs(
        [
            "BioGPT (Microsoft)",
            "BioMedLM (Stanford)",
            "Mistral-7B",
        ]
    )

    with tab1:
        col1, col2 = st.columns([3, 2], gap="large")
        with col1:
            st.markdown(
                f"""
            <div class="section-card">
              <h4 style="color:{_P['bact']};margin-top:0;">BioGPT Description</h4>
              <p style="color:{_P['txt_m']};line-height:1.8;">
                Pre-entraine sur <strong>millions d'articles PubMed</strong>.
              </p>
              <div style="background:#fef2f2;border-radius:8px;padding:14px;
                   margin-top:12px;border-left:4px solid {_P['red']};">
                <strong style="color:{_P['red']};">TAUX ELEVE DE FAUX POSITIFS</strong>
                → Biais systematique bactericide.
              </div>
            </div>""",
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f"""
            <div class="section-card" style="background:#f0fdf4;border:1px solid #bbf7d0;">
              <h4 style="color:{_P['green']};margin-top:0;">Avantages</h4>
              <ul style="color:{_P['txt_m']};line-height:1.9;margin:0;
                  padding-left:16px;font-size:0.88rem;">
                <li>Large couverture PubMed</li>
                <li>Rapidite</li>
                <li>Open source</li>
              </ul>
            </div>
            <div class="section-card" style="background:#fef2f2;border:1px solid #fca5a5;">
              <h4 style="color:{_P['red']};margin-top:0;">Limites</h4>
              <ul style="color:{_P['txt_m']};line-height:1.9;margin:0;
                  padding-left:16px;font-size:0.88rem;">
                <li>Biais systematique</li>
                <li>Hallucinations</li>
              </ul>
            </div>""",
                unsafe_allow_html=True,
            )

    with tab2:
        col1, col2 = st.columns([3, 2], gap="large")
        with col1:
            st.markdown(
                f"""
            <div class="section-card">
              <h4 style="color:#7c3aed;margin-top:0;">BioMedLM Description</h4>
              <p style="color:{_P['txt_m']};line-height:1.8;">
                Corpus <strong>medicaux et pharmacologiques</strong> (Stanford CRFM).
              </p>
              <div style="background:#fef2f2;border-radius:8px;padding:14px;
                   margin-top:12px;border-left:4px solid {_P['red']};">
                <strong style="color:{_P['red']};">Resultats incoherents</strong>
                → Confusion entre classes.
              </div>
            </div>""",
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f"""
            <div class="section-card" style="background:#f0fdf4;border:1px solid #bbf7d0;">
              <h4 style="color:{_P['green']};margin-top:0;">Avantages</h4>
              <ul style="color:{_P['txt_m']};line-height:1.9;margin:0;
                  padding-left:16px;font-size:0.88rem;">
                <li>Raisonnement clinique</li><li>Donnees pharma</li>
              </ul>
            </div>
            <div class="section-card" style="background:#fef2f2;border:1px solid #fca5a5;">
              <h4 style="color:{_P['red']};margin-top:0;">Limites</h4>
              <ul style="color:{_P['txt_m']};line-height:1.9;margin:0;
                  padding-left:16px;font-size:0.88rem;">
                <li>Incoherences</li><li>Confusion classes</li>
              </ul>
            </div>""",
                unsafe_allow_html=True,
            )

    with tab3:
        col1, col2 = st.columns([3, 2], gap="large")
        with col1:
            st.markdown(
                f"""
            <div class="section-card">
              <h4 style="color:{_P['amber']};margin-top:0;">Mistral-7B Description</h4>
              <p style="color:{_P['txt_m']};line-height:1.8;">
                Modele generaliste <strong>7B parametres</strong> Mistral AI, mode instruction.
              </p>
              <div style="background:#fef2f2;border-radius:8px;padding:14px;
                   margin-top:12px;border-left:4px solid {_P['red']};">
                <strong style="color:{_P['red']};">NON PERFORMANT</strong>
                sur la classification fine.
              </div>
            </div>""",
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f"""
            <div class="section-card" style="background:#f0fdf4;border:1px solid #bbf7d0;">
              <h4 style="color:{_P['green']};margin-top:0;">Avantages</h4>
              <ul style="color:{_P['txt_m']};line-height:1.9;margin:0;
                  padding-left:16px;font-size:0.88rem;">
                <li>General et polyvalent</li>
                <li>Suivi d'instructions</li>
                <li>Open source</li>
              </ul>
            </div>
            <div class="section-card" style="background:#fef2f2;border:1px solid #fca5a5;">
              <h4 style="color:{_P['red']};margin-top:0;">Limites</h4>
              <ul style="color:{_P['txt_m']};line-height:1.9;margin:0;
                  padding-left:16px;font-size:0.88rem;">
                <li>Non performant classification fine</li>
                <li>Connaissances biomédicales limitées</li>
              </ul>
            </div>""",
                unsafe_allow_html=True,
            )

    st.markdown(
        """
    <div class="warn-triangle">
      <h4>Discussion – Importance Clinique et Classes CARD</h4>
      <p style="margin:0 0 12px;">
        <strong>1. Importance clinique des bactericides stricts :</strong>
        Les 8 classes bactéricides strictes constituent la
        <strong>premiere ligne de defense</strong> dans les infections severes
        et chez les patients immunodeprimes. Leur effet letal direct et irreversible
        est indispensable lorsque le systeme immunitaire ne peut suppléer
        a l'arret du traitement.
      </p>
      <p style="margin:0 0 12px;">
        <strong>2. Role crucial des classes a double activite dans CARD :</strong>
        Les <strong>aminoglycosides</strong> (303 genes ARO) et les
        <strong>fluoroquinolones</strong> (307 genes ARO) generent une pression
        de selection majeure et une resistance etendue documentee.
      </p>
    </div>
    """,
        unsafe_allow_html=True,
    )
