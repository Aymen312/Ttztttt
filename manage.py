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
    </style>
    """,
    unsafe_allow_html=True,
)

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

        # Filtrer les lignes où 'qte_cde' n'est pas égal à 0
        if 'qte_cde' in data.columns:
            data = data[data['qte_cde'] != 0]

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
                        if 'fournisseur' in filtered_data.columns and 'val_rel' in filtered_data.columns:
                            somme_par_fournisseur = filtered_data.groupby('fournisseur', as_index=False)['val_rel'].sum()

                            # Ajouter la ligne de somme totale avec style bleu
                            total_val_rel = somme_par_fournisseur['val_rel'].sum()
                            nouvelle_ligne_fournisseur = pd.DataFrame({'fournisseur': ['Total'], 'val_rel': [total_val_rel]})
                            somme_par_fournisseur = pd.concat([somme_par_fournisseur, nouvelle_ligne_fournisseur], ignore_index=True)

                            # Formater la ligne du total en bleu
                            def highlight_total(s):
                                if s.iloc[0] == 'Total':  # Index 0 car 'fournisseur' est la première colonne
                                    return ['background-color: #ADD8E6'] * len(s)  # Bleu clair
                                return [''] * len(s)

                            # Formatter la colonne 'val_rel' pour afficher deux chiffres avant la décimale
                            styled_somme_fournisseur = somme_par_fournisseur.style.format({'val_rel': '{:02.2f}'}).apply(highlight_total, axis=1)

                            st.write("Somme des val_rel par fournisseur :")
                            st.dataframe(styled_somme_fournisseur)

                    with col2:
                        # Filtrer pour exclure qte_rel == 0
                        filtered_qte_rel = filtered_data[filtered_data['qte_rel'] != 0]

                        # Somme des qte_rel par designation
                        if 'designation' in filtered_qte_rel.columns and 'qte_rel' in filtered_qte_rel.columns:
                            somme_par_designation = filtered_qte_rel.groupby('designation', as_index=False)['qte_rel'].sum()

                            # Ajouter la ligne de somme totale pour la désignation
                            total_qte_rel = somme_par_designation['qte_rel'].sum()
                            nouvelle_ligne_designation = pd.DataFrame({'designation': ['Total'], 'qte_rel': [total_qte_rel]})
                            somme_par_designation = pd.concat([somme_par_designation, nouvelle_ligne_designation], ignore_index=True)

                            # Appliquer le même style bleu à la ligne du total
                            st.write("Somme des quantités réalisées par désignation :")
                            st.dataframe(somme_par_designation.style.apply(highlight_total, axis=1))

                else:
                    st.warning("Aucune donnée trouvée pour cette date de livraison.")

            # Nouvelle fonctionnalité : Recherche par designation
            st.write("---")  # Une ligne de séparation
            st.subheader("Recherche par désignation")

            # Zone de texte pour saisir une désignation
            st.markdown("<p style='color: var(--primary-color);'>Entrez une désignation pour voir les quantités commandées et les dates de livraison :</p>", unsafe_allow_html=True)
            designation_recherchee = st.text_input("")

            if designation_recherchee:
                # Filtrer les données pour la désignation spécifiée et exclure qte_rel == 0
                data_designation = data[(data['designation'].str.contains(designation_recherchee, case=False, na=False)) &
                                            (data['qte_rel'] != 0)]

                if not data_designation.empty:
                    # Grouper et afficher les quantités commandées par désignation et datelivraison
                    if 'qte_rel' in data_designation.columns and 'datelivraison' in data_designation.columns:
                        somme_qte_par_date = data_designation.groupby(['designation', 'datelivraison'], as_index=False)['qte_rel'].sum()

                        # Trier les résultats par date de livraison
                        somme_qte_par_date['datelivraison'] = pd.to_datetime(somme_qte_par_date['datelivraison'], dayfirst=True)
                        somme_qte_par_date = somme_qte_par_date.sort_values(by='datelivraison')

                        # Formater les dates pour l'affichage
                        somme_qte_par_date['datelivraison'] = somme_qte_par_date['datelivraison'].dt.strftime("%d/%m/%Y")

                        st.write(f"Quantités commandées pour la désignation '{designation_recherchee}' :")
                        st.dataframe(somme_qte_par_date)
                else:
                    st.warning("Aucune donnée trouvée pour cette désignation.")
        else:
            st.error("La colonne 'datelivraison' n'existe pas dans le fichier CSV.")
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")
else:
    st.info("Veuillez télécharger un fichier CSV pour commencer.")
