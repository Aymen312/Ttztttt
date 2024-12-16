import streamlit as st
import pandas as pd

# Titre de l'application
st.title("TDR")

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
            # 2. Extraire les dates uniques et trier dans l'ordre croissant
            dates_uniques = sorted(pd.to_datetime(data['datelivraison'].dropna().unique(), dayfirst=True))
            dates_formatees = [date.strftime("%d/%m/%Y") for date in dates_uniques]
            
            # 3. Utiliser un sélecteur interactif pour choisir une date
            date_selectionnee = st.selectbox("Choisissez une date de livraison :", dates_formatees)
            
            # Filtrer par date sélectionnée
            if date_selectionnee:
                filtered_data = data[data['datelivraison'] == date_selectionnee]
                
                if not filtered_data.empty:
                    # Réorganiser les colonnes
                    colonnes_ordre = [
                        'datelivraison', 'fournisseur', 'designation', 'taille', 'barcode', 'couleur',
                        'famille', 'ssfamille', 'prixachat', 'qte_cde', 'val_cde', 
                        'qte_rel', 'val_rel', 'qte_liv', 'val_liv'
                    ]
                    colonnes_existantes = [col for col in colonnes_ordre if col in filtered_data.columns]
                    filtered_data = filtered_data[colonnes_existantes]
                    
                    # Afficher les données filtrées
                    st.write("Données correspondantes à la date sélectionnée :")
                    st.dataframe(filtered_data)
                    
                    # Deux tableaux côte à côte
                    col1, col2 = st.columns(2)
                    with col1:
                        # Somme des prixachat par fournisseur
                        if 'fournisseur' in filtered_data.columns and 'prixachat' in filtered_data.columns:
                            somme_par_fournisseur = filtered_data.groupby('fournisseur', as_index=False)['prixachat'].sum()
                            st.write("Somme des prix d'achat par fournisseur :")
                            st.dataframe(somme_par_fournisseur)
                    with col2:
                        # Somme des qte_cde par designation
                        if 'designation' in filtered_data.columns and 'qte_cde' in filtered_data.columns:
                            somme_par_designation = filtered_data.groupby('designation', as_index=False)['qte_cde'].sum()
                            st.write("Somme des quantités commandées par désignation :")
                            st.dataframe(somme_par_designation)
                
                else:
                    st.warning("Aucune donnée trouvée pour cette date de livraison.")

            st.write("---")  # Une ligne de séparation
st.subheader("Recherche par désignation")

# Zone de texte pour saisir une désignation
designation_recherchee = st.text_input("Entrez une désignation pour voir les dates de livraison et quantités commandées :")

if designation_recherchee:
    # Filtrer les données pour la désignation spécifiée
    data_designation = data[data['designation'].str.contains(designation_recherchee, case=False, na=False)]
    
    if not data_designation.empty:
        # Convertir la colonne 'datelivraison' en datetime si nécessaire
        data_designation['datelivraison'] = pd.to_datetime(data_designation['datelivraison'], dayfirst=True, errors='coerce')
        
        # Regrouper les données par 'designation' et 'datelivraison' pour calculer la somme des quantités
        resultat_agrégé = (
            data_designation
            .groupby(['designation', 'datelivraison'], as_index=False)['qte_cde']
            .sum()
            .dropna()
        )
        
        # Trier les résultats par date de livraison
        resultat_agrégé = resultat_agrégé.sort_values(by='datelivraison')

        # Formater les dates pour l'affichage
        resultat_agrégé['datelivraison'] = resultat_agrégé['datelivraison'].dt.strftime("%d/%m/%Y")
        
        # Afficher les résultats dans un tableau
        st.write(f"Somme des quantités commandées pour la désignation '{designation_recherchee}' :")
        st.dataframe(resultat_agrégé)
    else:
        st.warning("Aucune donnée trouvée pour cette désignation.")
else:
    st.info("Veuillez entrer une désignation pour commencer la recherche.")
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")
else:
    st.info("Veuillez télécharger un fichier CSV pour commencer.")
