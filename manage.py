import streamlit as st
import pandas as pd

# Titre de l'application
st.title("Visualisation des données par date de livraison")

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
            
            # Convertir les dates en format chaîne pour affichage
            dates_formatees = [date.strftime("%d/%m/%Y") for date in dates_uniques]
            
            # 3. Utiliser un sélecteur interactif pour choisir une date
            date_selectionnee = st.selectbox("Choisissez une date de livraison :", dates_formatees)
            
            # 4. Filtrer les données selon la date sélectionnée
            if date_selectionnee:
                # Convertir la date sélectionnée au format original
                filtered_data = data[data['datelivraison'] == date_selectionnee]
                
                if not filtered_data.empty:
                    # 5. Réorganiser les colonnes dans l'ordre souhaité
                    colonnes_ordre = [
                        'datelivraison', 'fournisseur', 'designation', 'taille', 'barcode', 'couleur',
                        'famille', 'ssfamille', 'prixachat', 'qte_cde', 'val_cde', 
                        'qte_rel', 'val_rel', 'qte_liv', 'val_liv'
                    ]
                    
                    # S'assurer que seules les colonnes existantes sont sélectionnées
                    colonnes_existantes = [col for col in colonnes_ordre if col in filtered_data.columns]
                    filtered_data = filtered_data[colonnes_existantes]
                    
                    # Afficher les données filtrées et les autres tableaux en colonnes
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("Données correspondantes à la date sélectionnée :")
                        st.dataframe(filtered_data)
                    
                        # 6. Calculer la somme des prixachat par fournisseur
                        if 'fournisseur' in filtered_data.columns and 'prixachat' in filtered_data.columns:
                            somme_par_fournisseur = filtered_data.groupby('fournisseur', as_index=False)['prixachat'].sum()
                            st.write("Somme des prix d'achat par fournisseur :")
                            st.dataframe(somme_par_fournisseur)
                        else:
                            st.warning("Les colonnes 'fournisseur' ou 'prixachat' sont manquantes.")
                    
                    with col2:
                        # 7. Calculer la somme des qte_cde par designation
                        if 'designation' in filtered_data.columns and 'qte_cde' in filtered_data.columns:
                            somme_par_designation = filtered_data.groupby('designation', as_index=False)['qte_cde'].sum()
                            st.write("Somme des quantités commandées par désignation :")
                            st.dataframe(somme_par_designation)
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
