# 🧬 Résistance ATB – Dashboard

Application Streamlit de classification des antibiotiques bactéricides dans la base CARD.

## Auteure
**Eya Amri** – Projet IA Biomédicale

## Structure
```
BACTERICIDAL_DASHBOARD/
├── app.py                    # Point d'entrée principal
├── requirements.txt
├── .streamlit/
│   └── config.toml          # Thème clair personnalisé
├── utils/
│   ├── load_data.py         # Données et DataFrames
│   ├── charts.py            # Graphiques Plotly
│   └── helpers.py           # CSS, composants UI
└── pages/
    ├── home.py              # 🏠 Accueil
    ├── definitions.py       # 📖 Définitions
    ├── visualisation.py     # 📊 Visualisation
    ├── approches.py         # 🧪 Approches de Validation
    ├── resultats.py         # ✅ Résultats Finaux
    └── discussion.py        # 💬 Discussion
```

## Installation & Lancement
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Pages
1. **Accueil** – Contexte CARD, problématique AMR, objectifs
2. **Définitions** – Bactéricide/bactériostatique, mécanismes, CMB/CMI
3. **Visualisation** – Graphiques interactifs, distribution des classes
4. **Approches** – 4 méthodes de validation + LLMs (BioGPT, BioMedLM)
5. **Résultats** – 8 classes validées, comparaison LLM vs littérature
6. **Discussion** – Limites, classes discordantes, travaux futurs
