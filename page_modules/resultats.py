import streamlit as st
import pandas as pd
from utils.helpers import section_divider, info_box
from utils.load_data import (
    CARD_BACTERICIDE,
    get_llm_comparison_data,
    get_validated_results,
)


def render():
    st.markdown("# ✅ Résultats Finaux")
    st.markdown(
        '<p style="color:#64748b; font-size:1.05rem; margin-bottom:28px;">Synthèse des classes antibiotiques bactéricides validées par croisement des 3 approches et confirmation littérature.</p>',
        unsafe_allow_html=True,
    )

    # Hero
    st.markdown(
        """
    <div style="background:linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
                border:2px solid #86efac; border-radius:18px; padding:32px 36px; margin-bottom:28px;">
        <div style="display:flex; align-items:center; gap:14px; margin-bottom:20px;">
            <div style="font-size:2.2rem;">🏆</div>
            <div>
                <h2 style="margin:0; color:#16a34a !important;">10 Classes Bactéricides Validées dans CARD</h2>
                <p style="margin:4px 0 0; color:#4ade80; font-size:0.9rem;">
                    Croisement 3 approches + littérature CMB/CMI · Ratio CMB/CMI ≤ 4 confirmé
                </p>
            </div>
        </div>
        <div style="display:flex; flex-wrap:wrap; gap:10px;">
    """
        + "".join(
            [f'<span class="badge-validated">✓ {c}</span>' for c in CARD_BACTERICIDE]
        )
        + """
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
