# Nouvelle fonctionnalité : Recherche par taille
st.write("---")  # Une ligne de séparation
st.subheader("Recherche par taille")

# Zone de texte pour saisir une taille
st.markdown("<p style='color: var(--primary-color);'>Entrez une taille pour voir les quantités réalisées et les désignations correspondantes :</p>", unsafe_allow_html=True)
taille_recherchee = st.text_input("Taille")

if taille_recherchee:
    # Filtrer les données pour la taille spécifiée et exclure qte_rel == 0
    data_taille = data[(data['taille'].astype(str).str.contains(taille_recherchee, case=False, na=False)) &
                       (data['qte_rel'] != 0)]

    if not data_taille.empty:
        # Afficher les résultats (designation, qte_rel, et datelivraison)
        resultats_taille = data_taille[['designation', 'qte_rel', 'datelivraison']]
        st.write(f"Résultats pour la taille '{taille_recherchee}' :")
        st.dataframe(resultats_taille)
    else:
        st.warning("Aucune donnée trouvée pour cette taille.")
