import streamlit as st


# ───────────────── CONFIG PAGE ─────────────────
def page_config(title: str = "Résistance ATB"):
    st.set_page_config(
        page_title=title,
        page_icon="🧬",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": None,
            "Report a bug": None,
            "About": None,
        },
    )


# ───────────────── GLOBAL CSS ─────────────────
@st.cache_resource
def inject_global_css():
    # if "css_injected" in st.session_state:
    #     return
    # st.session_state["css_injected"] = True

    st.markdown(
        """
        <style>
        /* ══════════════════════════════════════════════════
           CACHE-CACHE : navigation automatique Streamlit
           On masque TOUT ce que Streamlit injecte dans la
           sidebar pour la navigation multi-pages.
        ══════════════════════════════════════════════════ */

        /* Lien de navigation natif (multi-pages classique) */
        [data-testid="stSidebarNav"],
        [data-testid="stSidebarNavItems"],
        [data-testid="stSidebarNavSeparator"],
        section[data-testid="stSidebar"] nav,
        section[data-testid="stSidebar"] ul,
        section[data-testid="stSidebar"] li {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            overflow: hidden !important;
        }

        /* Nouveau système st.navigation (Streamlit ≥ 1.36) */
        [data-testid="stSidebarNavLink"],
        [data-testid="stNavSectionHeader"] {
            display: none !important;
        }

        /* ══════════════════════════════════════════════════
           PALETTE & VARIABLES
        ══════════════════════════════════════════════════ */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

        :root {
            --navy:    #023e8a;
            --ocean:   #0077b6;
            --cerulean:#0096c7;
            --sky:     #00b4d8;
            --ice:     #caf0f8;
            --slate:   #468faf;
            --cobalt:  #2a6f97;
            --white:   #ffffff;
            --off:     #f0f8ff;
            --text:    #0d2137;
            --muted:   #4a7590;
            --border:  rgba(0,180,216,0.18);
            --glass:   rgba(255,255,255,0.72);
        }

        /* ══════════════════════════════════════════════════
           RESET & BASE
        ══════════════════════════════════════════════════ */
        * { box-sizing: border-box; }

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
        }
        code, pre { font-family: 'DM Mono', monospace !important; }

        .stApp { background: #f0f8ff; }

        .block-container {
            margin-top: 32px !important;
            padding: 2rem 2.5rem !important;
            max-width: 1400px;
        }

        /* ══════════════════════════════════════════════════
           SIDEBAR
        ══════════════════════════════════════════════════ */
        [data-testid="stSidebar"] {
            background: #ffffff !important;
            border-right: 1px solid #e0e7ef !important;
            box-shadow: 4px 0 20px rgba(0,0,0,0.06) !important;
            padding: 0 !important;
        }

        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
            gap: 0rem !important;
        }

        .sidebar-header {
            padding: 28px 20px 20px;
            border-bottom: 1px solid #f0f4f8;
            text-align: center;
        }
        .sidebar-logo {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 100px; height: 100px;
            font-size: 2rem;
            background: linear-gradient(135deg, var(--navy), var(--ocean));
            border-radius: 20px;
            box-shadow: 0 5px 18px rgba(2,62,138,0.28);
            margin-top: 8px;
        }
        .sidebar-logo:hover {
            background: linear-gradient(135deg, var(--ocean), var(--navy)); /* inversion des couleurs */
            transform: rotate(15deg); /* rotation sur hover */
            box-shadow: 0 8px 20px rgba(2,62,138,0.4); /* léger effet de profondeur */
        }
        .sidebar-header h1 {
            font-size: 2rem !important;
            font-weight: 700 !important;
            color: var(--navy) !important;
            margin: 0 0 6px 0 !important;
            letter-spacing: -0.2px;
        }
        .sidebar-subtitle {
            font-size: 1.25rem;
            color: var(--ocean);
            line-height: 1.4;
            padding: 0 8px;
        }
        .sidebar-divider {
            display: block !important;
            margin: 0 16px 8px;
            border: none;
            height: 1px;
            background: #e8edf3;
        }

        /* ── Boutons de navigation custom ── */
        [data-testid="stSidebar"] .stButton button {
            width: 100% !important;
            text-align: left !important;
            padding: 12px 16px !important;
            border-radius: 12px !important;
            font-size: 0.875rem !important;
            font-weight: 500 !important;
            border: none !important;
            transition: all 0.2s ease !important;
            cursor: pointer !important;
            position: relative !important;
            color: #4a6076 !important;
            background: transparent !important;
            margin: 0 !important;
        }
        [data-testid="stSidebar"] .stButton button:hover {
            background: #eef6ff !important;
            color: var(--navy) !important;
        }
        /* Bouton actif (type="primary") */
        [data-testid="stSidebar"] .stButton button[kind="primary"],
        [data-testid="stSidebar"] .stButton button[data-baseweb="button"][kind="primary"] {
            background: linear-gradient(135deg, #eef4ff, #e0efff) !important;
            color: var(--navy) !important;
            font-weight: 700 !important;
            border-left: 3px solid var(--ocean) !important;
        }

        /* ── Footer ── */
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            text-align: center;
            padding: 20px;
            font-size: 0.75rem;
            color: #6c757d;
            background: transparent;
            border-top: 1px solid #e9ecef;
            margin-top: 30px;
        }

        /* ══════════════════════════════════════════════════
           COMPOSANTS PARTAGÉS
        ══════════════════════════════════════════════════ */

        /* Divider horizontal */
        .custom-divider, .hdiv {
            border: none;
            height: 0px;
            background: linear-gradient(90deg, transparent, var(--border), transparent);
            margin: 0;
        }

        /* Info / success / warning boxes */
        .info-card {
            background: linear-gradient(135deg, #eff6ff, #e0f2fe);
            border-left: 4px solid var(--ocean);
            border-radius: 12px;
            padding: 16px 20px;
            font-size: 0.9rem;
            color: var(--navy);
            margin: 12px 0;
            line-height: 1.7;
        }
        .success-card {
            background: linear-gradient(135deg, #f0fdf4, #dcfce7);
            border-left: 4px solid #16a34a;
            border-radius: 12px;
            padding: 16px 20px;
            font-size: 0.9rem;
            color: #14532d;
            margin: 12px 0;
            line-height: 1.7;
        }
        .warning-card {
            background: linear-gradient(135deg, #fff7ed, #fef3c7);
            border-left: 4px solid #f97316;
            border-radius: 12px;
            padding: 16px 20px;
            font-size: 0.9rem;
            color: #78350f;
            margin: 12px 0;
            line-height: 1.7;
        }

        /* Badges */
        .badge-validated {
            display: inline-block;
            background: linear-gradient(135deg, #eff6ff, #dbeafe);
            color: var(--navy);
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 0.82rem;
            font-weight: 700;
            margin: 3px;
            border: 1px solid rgba(0,119,182,0.2);
        }
        .badge-bactericide {
            display: inline-block;
            background: linear-gradient(135deg, #eff6ff, #dbeafe);
            color: #1a56db;
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 0.82rem;
            font-weight: 700;
            margin: 3px;
            border-left: 3px solid #1a56db;
        }

        /* Section cards */
        .section-card {
            background: #ffffff;
            border-radius: 16px;
            padding: 24px;
            border: 1px solid #e8f0fe;
            box-shadow: 0 2px 12px rgba(0,100,180,0.06);
            margin-bottom: 16px;
        }

        /* Section headings */
        .sh-eyebrow {
            font-size: 0.72rem;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: #fff;
            font-weight: 700;
            margin-bottom: 6px;
        }
        .sh-title {
            font-size: 1.55rem;
            font-weight: 800;
            color: var(--navy);
            margin-bottom: 20px;
        }

        /* Banner info */
        .hbanner {
            background: linear-gradient(135deg, #f0f8ff, #e4f3fb);
            border: 1px solid var(--border);
            border-left: 4px solid var(--sky);
            border-radius: 14px;
            padding: 18px 24px;
            font-size: 0.92rem;
            color: var(--text);
            line-height: 1.8;
            margin-bottom: 24px;
        }

        /* Hero */
        .hero-wrap {
            position: relative;
            overflow: hidden;
            background: linear-gradient(135deg, #023e8a 0%, #0077b6 50%, #0096c7 100%);
            border-radius: 24px;
            padding: 48px 52px;
            margin-bottom: 36px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 32px;
            flex-wrap: wrap;
            box-shadow: 0 20px 60px rgba(2,62,138,0.28);
        }
        .hero-orb {
            position: absolute;
            border-radius: 50%;
            opacity: 0.12;
            filter: blur(40px);
        }
        .hero-orb.o1 { width:320px; height:320px; background:#caf0f8; top:-80px; right:80px; }
        .hero-orb.o2 { width:200px; height:200px; background:#fff;    bottom:-60px; left:40px; }
        .hero-orb.o3 { width:150px; height:150px; background:#00b4d8; top:20px; left:50%; }
        .hero-left { flex:1; min-width:260px; position:relative; z-index:1; }
        .hero-eyebrow {
            font-size:0.75rem; letter-spacing:2.5px; text-transform:uppercase;
            color:rgba(202,240,248,.85); font-weight:700; margin-bottom:14px;
            display:flex; align-items:center; gap:10px; flex-wrap:wrap;
        }
        .hero-pill {
            background:rgba(255,255,255,.15); border:1px solid rgba(255,255,255,.25);
            border-radius:30px; padding:3px 12px; font-size:0.7rem; color:#caf0f8;
        }
        .hero-title {
            font-size:2.8rem; font-weight:900; color:#fff; line-height:1.15;
            margin:0 0 12px; letter-spacing:-1px;
        }
        .hero-title .accent { color:var(--sky); }
        .hero-subtitle {
            font-size:1rem; color:rgba(255,255,255,.78);
            font-weight:400; margin:0;
        }
        .hero-imgs {
            display:flex; flex-direction:column; gap:12px;
            position:relative; z-index:1;
        }
        .img-card {
            display:flex; align-items:center; gap:12px;
            background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.18);
            border-radius:14px; padding:12px 18px; min-width:220px;
            backdrop-filter:blur(8px);
        }
        .img-ico { font-size:1.4rem; }
        .img-txt { font-weight:700; color:#fff; font-size:0.88rem; }
        .img-sub { font-size:0.72rem; color:rgba(202,240,248,.8); }

        /* Stat badges */
        .stat-badge {
            background: linear-gradient(135deg, var(--navy), var(--ocean));
            border-radius: 18px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 6px 20px rgba(2,62,138,0.22);
        }
        .stat-val {
            font-size: 2rem; font-weight: 900; color: #fff;
        }
        .stat-lbl {
            font-size: 0.75rem; color: var(--ice); margin-top: 4px;
        }

        /* Objective cards */
        .obj-card {
            display: flex; align-items: flex-start; gap: 14px;
            background: #fff; border-radius: 14px;
            padding: 16px 18px; margin-bottom: 12px;
            border: 1px solid var(--border);
            box-shadow: 0 2px 10px rgba(0,100,180,0.05);
        }
        .obj-num {
            min-width: 36px; height: 36px;
            background: linear-gradient(135deg, var(--navy), var(--ocean));
            border-radius: 10px; font-size: 0.78rem;
            font-weight: 800; color: #fff;
            display: flex; align-items: center; justify-content: center;
        }
        .obj-title {
            font-weight: 700; color: var(--navy);
            font-size: 0.9rem; margin-bottom: 4px;
        }
        .obj-desc { font-size: 0.82rem; color: var(--muted); line-height: 1.6; }

        /* Component chips */
        .comp-chip {
            display: flex; align-items: flex-start; gap: 14px;
            padding: 14px 0; border-bottom: 1px solid #f0f4f8;
        }
        .comp-chip:last-child { border-bottom: none; }
        .chip-ico {
            font-size: 1.3rem; min-width: 36px; height: 36px;
            background: linear-gradient(135deg, var(--ice), #e0f3fb);
            border-radius: 10px; display: flex;
            align-items: center; justify-content: center;
        }
        .chip-title { font-weight: 700; color: var(--navy); font-size: 0.88rem; }
        .chip-desc  { font-size: 0.78rem; color: var(--muted); margin-top: 2px; line-height: 1.5; }

        /* Modal */
        .modal-overlay {
            display: none; position: fixed; inset: 0; z-index: 9999;
            background: rgba(2,30,70,.55); backdrop-filter: blur(6px);
            align-items: center; justify-content: center;
        }
        .modal-overlay.open { display: flex; }
        .modal-box {
            background: #fff; border-radius: 24px;
            padding: 32px 36px; max-width: 720px; width: 94%;
            max-height: 82vh; overflow-y: auto;
            box-shadow: 0 24px 80px rgba(2,62,138,.28);
            position: relative;
        }
        .modal-close {
            position: absolute; top: 16px; right: 20px;
            background: none; border: none; font-size: 1.1rem;
            cursor: pointer; color: var(--muted);
        }
        .class-grid {
            display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px;
        }
        .class-item {
            display: flex; align-items: center; gap: 8px;
            font-size: 0.82rem; color: var(--text); padding: 6px 10px;
            border-radius: 8px; background: #f8fafc;
        }
        .class-dot {
            width: 8px; height: 8px; border-radius: 50%;
            background: var(--sky); flex-shrink: 0;
        }
        .open-modal-btn {
            background: linear-gradient(135deg, var(--ocean), var(--navy));
            color: #fff; border: none; border-radius: 40px;
            padding: 10px 22px; font-size: 0.84rem; font-weight: 600;
            cursor: pointer; box-shadow: 0 4px 14px rgba(0,119,182,.3);
            transition: transform .2s, box-shadow .2s;
        }
        .open-modal-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 22px rgba(0,119,182,.4);
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


# ───────────────── SIDEBAR ─────────────────
def render_sidebar() -> str:
    """
    Affiche la sidebar de navigation entièrement custom.
    Retourne la clé de page sélectionnée (str).

    NOTE : Pour que la navigation native Streamlit (dossier pages/)
    n'apparaisse PAS dans la sidebar, deux stratégies sont combinées :
      1. Le CSS ci-dessus cache tous les sélecteurs natifs.
      2. L'application doit être structurée en single-file (app.py)
         qui importe et appelle render() de chaque module page.
         → Supprimer le dossier pages/ ou le vider résout définitivement
           le problème sans dépendre du CSS.
    """
    pages = {
        "🏠  Présentation du Projet": "home",
        "🔬  Classification Bactéricide / Bactériostatique": "classification",
        "🧪  Approches de Validation": "approches",
        "📊  Résultats Finaux": "resultats",
        "💬  Références": "references",
    }

    with st.sidebar:
        # ── Header ──
        st.markdown(
            """
            <div class="sidebar-header">
                <div class="sidebar-logo">🧬</div>
                <h1>Résistance ATB</h1>
                <div class="sidebar-subtitle">
                    Système de prédiction de la résistance aux antibiotiques
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

        # ── Navigation ──
        if "selected_page" not in st.session_state:
            st.session_state.selected_page = list(pages.keys())[0]

        for page_name, page_key in pages.items():
            is_active = st.session_state.selected_page == page_name
            if st.button(
                page_name,
                key=f"nav_{page_key}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state.selected_page = page_name
                st.rerun()

        # ── Spacer + version ──
        st.markdown("<br>" * 2, unsafe_allow_html=True)
        st.markdown(
            """
            <div style="padding:0 16px; font-size:0.68rem; color:#a0aec0; line-height:1.6;">
                v1.0 · Eya Amri · 2026<br>
                Projet PFE · Bioinformatique &amp; IA
            </div>
            """,
            unsafe_allow_html=True,
        )

    return st.session_state.selected_page


# ───────────────── FOOTER ─────────────────
def render_footer():
    st.markdown(
        """
        <div class="footer">
            <strong>Résistance ATB</strong> 
        </div>
        """,
        unsafe_allow_html=True,
    )


# ───────────────── UTILS ─────────────────
def section_divider():
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)


def info_box(text: str, kind: str = "info"):
    cls = {
        "info": "info-card",
        "success": "success-card",
        "warning": "warning-card",
    }.get(kind, "info-card")
    st.markdown(f'<div class="{cls}">✨ {text}</div>', unsafe_allow_html=True)
