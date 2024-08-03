import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from io import BytesIO

# Your existing functions here...

# Streamlit Application
st.set_page_config(page_title="Application d'Analyse TDR", layout="wide")

# Custom CSS for futuristic design
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #1E1E1E, #2D2D2D);
            color: #F5F5F5;
            font-family: 'Arial', sans-serif;
        }
        .stButton>button {
            background-color: #007BFF;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 14px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #0056b3;
        }
        .stTextInput>div>input {
            border: 2px solid #007BFF;
            border-radius: 5px;
            padding: 10px;
            background-color: #1E1E1E;
            color: #F5F5F5;
        }
        .stTextInput>div>input:focus {
            border-color: #0056b3;
            outline: none;
        }
        .stMultiSelect>div>div {
            border: 2px solid #007BFF;
            border-radius: 5px;
            background-color: #1E1E1E;
            color: #F5F5F5;
        }
        .stMultiSelect>div>div>div>div {
            color: #F5F5F5;
        }
        .stExpander>div>div {
            background-color: #2D2D2D;
            color: #F5F5F5;
            border-radius: 5px;
            padding: 10px;
        }
        .stExpander>div>div>div {
            color: #F5F5F5;
        }
    </style>
    """, unsafe_allow_html=True)

st.title("Application d'Analyse TDR")

st.sidebar.markdown("### Menu")
st.sidebar.info("Téléchargez un fichier CSV ou Excel pour commencer l'analyse.")

# File upload
fichier_telecharge = st.file_uploader("Téléchargez un fichier CSV ou Excel", type=['csv', 'xlsx'])

if fichier_telecharge is not None:
    extension_fichier = fichier_telecharge.name.split('.')[-1]
    try:
        with st.spinner("Chargement des données..."):
            if extension_fichier == 'csv':
                # Read CSV with proper encoding and separator
                df = pd.read_csv(fichier_telecharge, encoding='ISO-8859-1', sep=';')
            elif extension_fichier == 'xlsx':
                df = pd.read_excel(fichier_telecharge)
            else:
                st.error("Format de fichier non supporté")
                df = None

        if df is not None:
            # Clean data
            df = clean_numeric_columns(df)
            df = clean_size_column(df)  # Clean size column

            # Separate data by gender
            df_homme = df[df['rayon'].str.upper() == 'HOMME']
            df_femme = df[df['rayon'].str.upper() == 'FEMME']
            df_unisexe = df[df['rayon'].str.upper() == 'UNISEXE']
            
            # Tab selection
            tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Analyse ANITA", "Analyse par Fournisseur", "Analyse par Désignation", "Stock Négatif", "Analyse SIDAS", "Valeur Totale du Stock par Fournisseur", "Visualisations"])
            
            with tab1:
                st.subheader("Quantités Disponibles pour chaque Taille - Fournisseur ANITA")
                try:
                    df_anita_sizes = display_anita_sizes(df)
                    if not df_anita_sizes.empty:
                        st.table(df_anita_sizes)
                    else:
                        st.write("Aucune information disponible pour le fournisseur ANITA.")
                except Exception as e:
                    st.error(f"Erreur lors de l'analyse des tailles pour ANITA: {e}")
            
            with tab2:
                # Ask for supplier name
                fournisseur = st.text_input("Entrez le nom du fournisseur:")
                
                if fournisseur:
                    try:
                        fournisseur = str(fournisseur).strip().upper()  # Convert user input supplier to uppercase
                        
                        # Filter DataFrame based on user input
                        df_homme_filtered = display_supplier_info(df_homme, fournisseur)
                        df_femme_filtered = display_supplier_info(df_femme, fournisseur)
                        df_unisexe_filtered = display_supplier_info(df_unisexe, fournisseur)
                        
                        # Sort sizes numerically
                        df_homme_filtered = sort_sizes(df_homme_filtered)
                        df_femme_filtered = sort_sizes(df_femme_filtered)
                        df_unisexe_filtered = sort_sizes(df_unisexe_filtered)
                        
                        # Display filtered information
                        st.subheader("Informations sur le Fournisseur pour Hommes")
                        if not df_homme_filtered.empty:
                            st.dataframe(df_homme_filtered)
                        else:
                            st.write("Aucune information disponible pour le fournisseur spécifié.")
                        
                        st.subheader("Informations sur le Fournisseur pour Femmes")
                        if not df_femme_filtered.empty:
                            st.dataframe(df_femme_filtered)
                        else:
                            st.write("Aucune information disponible pour le fournisseur spécifié.")
                        
                        st.subheader("Informations sur le Fournisseur Unisexe")
                        if not df_unisexe_filtered.empty:
                            st.dataframe(df_unisexe_filtered)
                        else:
                            st.write("Aucune information disponible pour le fournisseur spécifié.")
                    except Exception as e:
                        st.error(f"Erreur lors de l'affichage des informations pour le fournisseur: {e}")

            with tab3:
                # Ask for designation name
                designation = st.text_input("Entrez la désignation:")
                
                if designation:
                    try:
                        # Convert designation input to uppercase
                        designation = str(designation).strip().upper()
                        
                        # Filter DataFrame based on user input
                        df_homme_filtered = display_designation_info(df_homme, designation)
                        df_femme_filtered = display_designation_info(df_femme, designation)
                        df_unisexe_filtered = display_designation_info(df_unisexe, designation)
                        
                        # Sort sizes numerically
                        df_homme_filtered = sort_sizes(df_homme_filtered)
                        df_femme_filtered = sort_sizes(df_femme_filtered)
                        df_unisexe_filtered = sort_sizes(df_unisexe_filtered)
                        
                        # Display filtered information
                        st.subheader("Informations sur la Désignation pour Hommes")
                        if not df_homme_filtered.empty:
                            st.dataframe(df_homme_filtered)
                        else:
                            st.write("Aucune information disponible pour la désignation spécifiée.")
                        
                        st.subheader("Informations sur la Désignation pour Femmes")
                        if not df_femme_filtered.empty:
                            st.dataframe(df_femme_filtered)
                        else:
                            st.write("Aucune information disponible pour la désignation spécifiée.")
                        
                        st.subheader("Informations sur la Désignation Unisexe")
                        if not df_unisexe_filtered.empty:
                            st.dataframe(df_unisexe_filtered)
                        else:
                            st.write("Aucune information disponible pour la désignation spécifiée.")
                    except Exception as e:
                        st.error(f"Erreur lors de l'affichage des informations pour la désignation: {e}")

            with tab4:
                st.subheader("Stock Négatif")
                try:
                    df_negative_stock = filter_negative_stock(df)
                    if not df_negative_stock.empty:
                        # Display columns fournisseur, barcode, couleur, taille, Qté stock dispo
                        selected_columns = st.multiselect("Sélectionnez des colonnes supplémentaires à afficher:", df.columns.tolist(), default=['fournisseur', 'barcode', 'couleur', 'taille', 'Qté stock dispo'])
                        df_selected_columns = df_negative_stock[selected_columns]
                        st.dataframe(df_selected_columns)
                    else:
                        st.write("Aucun stock négatif trouvé.")
                except Exception as e:
                    st.error(f"Erreur lors de l'analyse du stock négatif: {e}")

            with tab5:
                st.subheader("Analyse des Niveaux SIDAS")
                try:
                    sidas_levels_results = display_sidas_levels(df)
                    if sidas_levels_results:
                        for level, df_sidas_level in sidas_levels_results.items():
                            st.subheader(f"Niveau {level}")
                            st.dataframe(df_sidas_level)
                    else:
                        st.write("Aucune information disponible pour les niveaux SIDAS.")
                except Exception as e:
                    st.error(f"Erreur lors de l'analyse des niveaux SIDAS: {e}")

            with tab6:
                st.subheader("Valeur Totale du Stock par Fournisseur")
                try:
                    total_stock_value = calculate_total_stock_value(df)
                    st.table(total_stock_value)
                except Exception as e:
                    st.error(f"Erreur lors de la calcul de la valeur totale du stock: {e}")

            with tab7:
                st.subheader("Visualisations")

                # Bar plot for stock value by supplier
                fig, ax = plt.subplots()
                stock_value_by_supplier = df.groupby('fournisseur')['valeur'].sum().reset_index()
                sns.barplot(data=stock_value_by_supplier, x='valeur', y='fournisseur', ax=ax)
                ax.set_title("Valeur Totale du Stock par Fournisseur")
                ax.set_xlabel("Valeur Totale")
                ax.set_ylabel("Fournisseur")
                st.pyplot(fig)

                # Line plot for quantity available over time
                if 'date' in df.columns:
                    df['date'] = pd.to_datetime(df['date'], errors='coerce')
                    fig, ax = plt.subplots()
                    quantity_over_time = df.groupby('date')['Qté stock dispo'].sum().reset_index()
                    sns.lineplot(data=quantity_over_time, x='date', y='Qté stock dispo', ax=ax)
                    ax.set_title("Quantité Disponible au Fil du Temps")
                    ax.set_xlabel("Date")
                    ax.set_ylabel("Quantité Disponible")
                    st.pyplot(fig)
                else:
                    st.write("La colonne 'date' n'est pas disponible dans les données.")

                # Pie chart for stock distribution by category
                fig, ax = plt.subplots()
                stock_distribution = df['rayon'].value_counts().reset_index()
                stock_distribution.columns = ['rayon', 'count']
                ax.pie(stock_distribution['count'], labels=stock_distribution['rayon'], autopct='%1.1f%%', startangle=90)
                ax.set_title("Répartition du Stock par Catégorie")
                st.pyplot(fig)

    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {e}")
else:
    st.write("Veuillez télécharger un fichier pour commencer l'analyse.")
