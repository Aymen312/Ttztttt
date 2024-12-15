import streamlit as st
import pandas as pd

# Titre de l'application
st.title("Visualisation des données par date de livraison")

# 1. Permettre à l'utilisateur de télécharger un fichier CSV
uploaded_file = st.file_uploader("Téléchargez votre fichier CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Lire le fichier CSV avec un séparateur ';' (adaptable selon le fichier)
        data = pd.read_csv(uploaded_file, sep=';', encoding_errors='ignore')
        
        # Nettoyer les noms de colonnes en supprimant les espaces
        data.columns = data.columns.str.strip()
        
        # Vérifier si la colonne "datelivraison" existe
        if 'datelivraison' in data.columns:
            # 2. Extraire les dates uniques pour afficher dans une liste déroulante
            dates_uniques = data['datelivraison'].dropna().unique()
            
            # 3. Utiliser un sélecteur interactif pour choisir une date
            date_selectionnee = st.selectbox("Choisissez une date de livraison :", dates_uniques)
            
            # 4. Filtrer les données selon la date sélectionnée
            if date_selectionnee:
                filtered_data = data[data['datelivraison'] == date_selectionnee]
                
                if not filtered_data.empty:
                    st.write("Données correspondantes à la date sélectionnée :")
                    st.dataframe(filtered_data)  # Affichage des données filtrées
                else:
                    st.warning("Aucune donnée trouvée pour cette date de livraison.")
        else:
            st.error("La colonne 'datelivraison' n'existe pas dans le fichier CSV.")
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")
else:
    st.info("Veuillez télécharger un fichier CSV pour commencer.")
