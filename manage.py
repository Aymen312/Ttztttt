import streamlit as st
import pandas as pd

# Titre de l'application
st.title("TDR - Visualisation des données")

# 1. Permettre à l'utilisateur de télécharger un fichier CSV
uploaded_file = st.file_uploader("Téléchargez votre fichier CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Lire le fichier CSV avec un séparateur ';'
        data = pd.read_csv(uploaded_file, sep=';', encoding_errors='ignore')
        
        # Nettoyer les noms de colonnes en supprimant les espaces
        data.columns = data.columns.str.strip()
        
        # Vérifier si la colonne "datelivraison" existe
        if 'datelivraison' in data.columns:
            # Extraire les dates uniques et trier dans l'ordre croissant
            dates_uniques = sorted(pd.to_datetime(data['datelivraison'].dropna().unique(), dayfirst=True))
            dates_formatees = [date.strftime("%d/%m/%Y") for date in dates_uniques]
            
            # Sélecteur interactif pour choisir une date
            date_selectionnee = st.selectbox("Choisissez une date de livraison :", dates_formatees)
            
            # Filtrer par date sélectionnée
            if date_selectionnee:
                # Filtrer les données
                filtered_data = data[data['datelivraison'] == date_selectionnee]
                
                if not filtered_data.empty:
                    st.write("### Données filtrées pour la date sélectionnée :")
                    st.dataframe(filtered_data)
                    
                    # Tableau moderne avec la somme des qte_cde pour chaque designation
                    if 'designation' in filtered_data.columns and 'qte_cde' in filtered_data.columns:
                        somme_qte_par_designation = (
                            filtered_data.groupby('designation', as_index=False)['qte_cde'].sum()
                        )
                        
                        # Afficher un tableau moderne
                        st.write("### Somme des quantités commandées (qte_cde) par désignation :")
                        st.dataframe(
                            somme_qte_par_designation.style.format({'qte_cde': '{:.2f}'}).background_gradient(cmap='Blues')
                        )
                    else:
                        st.warning("Les colonnes 'designation' ou 'qte_cde' sont manquantes.")
                else:
                    st.warning("Aucune donnée trouvée pour cette date de livraison.")
        else:
            st.error("La colonne 'datelivraison' n'existe pas dans le fichier CSV.")
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")
else:
    st.info("Veuillez télécharger un fichier CSV pour commencer.")
