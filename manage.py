import streamlit as st
import pandas as pd

# Configuration de la page Streamlit pour un thème plus large
st.set_page_config(layout="wide")

# Personnalisation du thème Streamlit (bleu moderne)
st.markdown(
    """
    <style>
    :root {
        --primary-color: #007BFF;
        --secondary-background-color: #f0f8ff;
        --text-color: #333333;
        --font: sans-serif;
    }
    .stApp {
        background-color: var(--secondary-background-color);
        color: var(--text-color);
        font-family: var(--font);
    }
    h1, h2, h3, h4, h5, h6 {
        color: var(--primary-color);
    }
    .stButton>button {
        background-color: var(--primary-color);
        color: white;
        border: none;
        border-radius: 0.3rem;
        padding: 0.5em 1em;
    }
    .stTextInput>div>div>input {
        border: 1px solid var(--primary-color);
        border-radius: 0.3rem;
    }
    .stSelectbox>div>div>div>div {
        background-color: white;
        border: 1px solid var(--primary-color);
        border-radius: 0.3rem;
        color: var(--text-color);
    }
    .stDataFrame {
        border: 1px solid #ddd;
        border-radius: 0.3rem;
    }
    .stDataFrame table {
        background-color: white;
    }
    .metric-box {
        background-color: white;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-title {
        font-size: 1rem;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def display_metrics(title, df, value_col, name_col="name"):
    st.markdown(f"<div class='metric-box'><div class='metric-title'>{title}</div>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    for i, (name, value) in enumerate(zip(df[name_col], df[value_col])):
        if i < 3:  # Afficher maximum 3 métriques par ligne
            with cols[i % 3]:
                st.metric(name, f"€{value:.2f}" if value_col == 'val_rel' else f"{value}")
    
    # Afficher le total
    total = df[value_col].sum()
    st.markdown(f"<div style='margin-top: 1rem;'><b>Total :</b> {'€' if value_col == 'val_rel' else ''}{total:.2f}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Titre de l'application
st.title("TDR")

# [Le reste du code précédent jusqu'à la partie des tableaux côte à côte reste inchangé...]

if uploaded_file is not None:
    try:
        # [Lecture des données et filtrage comme avant...]
        
        if not filtered_data.empty:
            # [Réorganisation des colonnes comme avant...]

            # Afficher les données filtrées
            st.write("Données correspondantes à la date sélectionnée :")
            st.dataframe(filtered_data)

            # Deux sections de métriques au lieu de tableaux
            if 'fournisseur' in filtered_data.columns and 'val_rel' in filtered_data.columns:
                somme_par_fournisseur = filtered_data.groupby('fournisseur', as_index=False)['val_rel'].sum()
                display_metrics("Somme des val_rel par fournisseur", somme_par_fournisseur, 'val_rel', 'fournisseur')

            # Filtrer pour exclure qte_rel == 0
            filtered_qte_rel = filtered_data[filtered_data['qte_rel'] != 0]
            
            if 'designation' in filtered_qte_rel.columns and 'qte_rel' in filtered_qte_rel.columns:
                somme_par_designation = filtered_qte_rel.groupby('designation', as_index=False)['qte_rel'].sum()
                display_metrics("Somme des quantités réalisées par désignation", somme_par_designation, 'qte_rel', 'designation')

        # [Le reste du code (recherche par désignation, taille, fournisseur) reste inchangé...]
