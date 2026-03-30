import sys, os

sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from utils.helpers import page_config, inject_global_css, render_sidebar, render_footer

# ── Doit être le PREMIER appel Streamlit ────────────────────────
page_config("Résistance ATB – Dashboard")

# ── CSS injecté AVANT le rendu de la sidebar ────────────────────
inject_global_css()

# ── Sidebar + récupération de la page active ────────────────────
selected_page = render_sidebar()

# ── Routing — noms identiques à ceux définis dans render_sidebar() ──
if selected_page == "🏠  Présentation du Projet":
    from page_modules import home

    home.render()

elif selected_page == "🔬  Classification Bactéricide / Bactériostatique":
    from page_modules import definitions

    definitions.render()

elif selected_page == "🧪  Approches de Validation":
    from page_modules import approches

    approches.render()

elif selected_page == "📊  Résultats Finaux":
    from page_modules import resultats

    resultats.render()

elif selected_page == "💬  Références":
    from page_modules import references

    references.render()

render_footer()
