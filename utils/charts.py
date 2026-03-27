import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

COLORS = {
    "bactericide": "#1a56db",
    "bacteriostatique": "#64748b",
    "dual": "#0ea5e9",
    "undetermined": "#94a3b8",
    "validated": "#16a34a",
    "bg": "#f0f4ff",
}


def bar_chart_classes(df: pd.DataFrame) -> go.Figure:
    color_map = {
        "Bactéricide": "#1a56db",
        "Bactériostatique": "#64748b",
        "Double activité": "#0ea5e9",
        "Non déterminé": "#94a3b8",
    }
    colors = [color_map.get(a, "#999") for a in df["Activité"]]

    fig = go.Figure(
        go.Bar(
            x=df["Classe"],
            y=df["Gènes ARO"],
            marker_color=colors,
            text=df["Gènes ARO"],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Gènes ARO : %{y}<extra></extra>",
        )
    )
    fig.update_layout(
        title="Nombre de gènes ARO par classe antibiotique (CARD)",
        xaxis_title="",
        yaxis_title="Nombre de gènes ARO",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Inter, sans-serif", size=11, color="#1e293b"),
        xaxis=dict(tickangle=-38, showgrid=False),
        yaxis=dict(gridcolor="#e2e8f0"),
        margin=dict(t=50, b=140),
        showlegend=False,
    )
    return fig


def pie_chart_distribution_card() -> go.Figure:
    """Graphique en donut basé sur les 46 classes réelles de CARD (slide 16)."""
    labels = ["Non déterminé (57%)", "Bactéricide (22%)", "Bactériostatique (20%)", "Bactéricide strict (17%)"]
    values = [26, 10, 9, 8]
    colors = ["#94a3b8", "#3b82f6", "#64748b", "#1a56db"]

    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.48,
            marker_colors=colors,
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>%{value} classes<extra></extra>",
        )
    )
    fig.update_layout(
        title="Distribution des 46 classes CARD",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Inter, sans-serif", size=12, color="#1e293b"),
        margin=dict(t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        annotations=[dict(text="46 classes", x=0.5, y=0.5, font_size=15, showarrow=False, font_color="#1e293b")],
    )
    return fig


def mdr_bar_chart(df: pd.DataFrame) -> go.Figure:
    """Graphique MDR top classes (slide 43 données réelles)."""
    colors = ["#1a56db" if t else "#93c5fd" for t in df["Dans TOP genes (score=13)"]]
    fig = go.Figure(
        go.Bar(
            x=df["Gènes MDR (seuil≥2)"],
            y=df["Classe"],
            orientation="h",
            marker_color=colors,
            text=df["Gènes MDR (seuil≥2)"],
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Gènes MDR : %{x}<extra></extra>",
        )
    )
    fig.update_layout(
        title="Top classes – Distribution dans les gènes MULTI-RÉSISTANTS<br><sup>seuil ≥ 2 | n=3530 gènes | score max=13 (bleu foncé = présent dans TOP genes)</sup>",
        xaxis=dict(title="Nombre de gènes multi-résistants", showgrid=True, gridcolor="#e2e8f0"),
        yaxis=dict(showgrid=False, autorange="reversed"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Inter, sans-serif", size=11, color="#1e293b"),
        margin=dict(l=200, r=100, t=80, b=40),
    )
    return fig


def bar_aro_mechanisms() -> go.Figure:
    """Nombre de Drug Classes par mécanisme ARO (slide 25)."""
    mechanisms = ["antibiotic inactivation", "antibiotic target alteration", "antibiotic efflux",
                  "antibiotic target protection", "antibiotic target replacement"]
    counts = [22, 41, 33, 15, 8]
    colors_mech = ["#3b82f6", "#ef4444", "#22c55e", "#f97316", "#a855f7"]

    fig = go.Figure(
        go.Bar(
            x=mechanisms,
            y=counts,
            marker_color=colors_mech,
            text=counts,
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>%{y} Drug Classes distinctes<extra></extra>",
        )
    )
    fig.update_layout(
        title="Nombre de Drug Classes distinctes par mécanisme de résistance (ARO)",
        xaxis=dict(tickangle=-15, showgrid=False),
        yaxis=dict(gridcolor="#e2e8f0", title="Nb Drug Classes distinctes"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Inter, sans-serif", size=12, color="#1e293b"),
        margin=dict(t=50, b=100),
    )
    return fig


def pie_chart_distribution(df: pd.DataFrame) -> go.Figure:
    """Graphique basé sur le df filtré."""
    counts = df["Activité"].value_counts()
    color_map = {
        "Bactéricide": "#1a56db",
        "Bactériostatique": "#64748b",
        "Double activité": "#0ea5e9",
        "Non déterminé": "#94a3b8",
    }
    colors = [color_map.get(l, "#999") for l in counts.index]

    fig = go.Figure(
        go.Pie(
            labels=counts.index,
            values=counts.values,
            hole=0.45,
            marker_colors=colors,
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>%{value} classes<br>%{percent}<extra></extra>",
        )
    )
    fig.update_layout(
        title="Distribution des activités – classes CARD analysées",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Inter, sans-serif", size=13, color="#1e293b"),
        margin=dict(t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
    )
    return fig
