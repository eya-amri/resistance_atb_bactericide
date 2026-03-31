# 🧬 Résistance ATB – Dashboard

Application Streamlit de classification des antibiotiques bactéricides dans la base CARD.


## Structure
```
BACTERICIDAL_DASHBOARD/
├── app.py                   
├── requirements.txt
├── .streamlit/
│   └── config.toml         
├── utils/
│   ├── load_data.py         # Données et DataFrames
│   ├── charts.py            # Graphiques Plotly
│   └── helpers.py           # CSS, composants UI
└── pages/
    ├── home.py              # 🏠 Accueil
    ├── definitions.py       # 📖 Definitions et Classification bactéricide
    ├── approches.py         # 🧪 Approches de Validation
    ├── resultats.py         # ✅ Résultats Finaux
    └── references.py        # 💬 Références
```

## Installation & Lancement
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Pages
1. **Accueil** – Contexte CARD, problématique AMR, objectifs
2. **Définitions** – Bactéricide/bactériostatique, Double activité, CMB/CMI
4. **Approches** – 3 méthodes de validation 
5. **Résultats** – 10 classes bactéricides validées,
6. **Références** 