import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.colors as pc

# Streamlit page
st.title("Nettoyage automatique des données avant analyse.")

# Check if any dataframes have been uploaded in the session state
if 'dataframes' in st.session_state and st.session_state['dataframes']:
    # Get the first dataframe uploaded
    df_name, ipm = next(iter(st.session_state['dataframes'].items()))

    # Display main page content
    st.header(f"Contenu du fichier avant nettoyage: {list(ipm.keys())[0]}")
    st.dataframe(ipm.head(6))

    # Button to clean 'dat_consu'
    if st.button('Nettoyer la colonne dat_consu'):
        ipm['dat_consu'] = pd.to_datetime(ipm['dat_consu'], format='%d/%m/%Y', errors='coerce')
        ipm['vacc_vero_date'] = pd.to_datetime(ipm['vacc_vero_date'], format='%d/%m/%Y', errors='coerce')
        ipm['vacc_sour_date'] = pd.to_datetime(ipm['vacc_sour_date'], format='%d/%m/%Y', errors='coerce')
        ipm['dat_consu'] = ipm['dat_consu'].fillna(ipm['vacc_vero_date']).fillna(ipm['vacc_sour_date'])
        st.success("Colonne 'dat_consu' nettoyée avec succès.")

    # Button to clean 'sexe'
    if st.button('Nettoyer la colonne sexe'):
        ipm['sexe'] = ipm.groupby('ref_mordu')['sexe'].transform(lambda x: x.ffill().bfill())
        st.success("Colonne 'sexe' nettoyée avec succès.")

    # Button to clean 'nom'
    if st.button('Nettoyer la colonne nom'):
        ipm['nom'] = ipm.groupby('ref_mordu')['nom'].transform(lambda x: x.ffill().bfill())
        st.success("Colonne 'nom' nettoyée avec succès.")

    # Button to clean 'age'
    if st.button('Nettoyer la colonne age'):
        ipm['age'] = ipm.groupby('ref_mordu')['age'].transform(lambda x: x.ffill().bfill())
        st.success("Colonne 'age' nettoyée avec succès.")

    # Button to clean 'annee'
    if st.button('Nettoyer la colonne annee'):
        ipm['annee'] = ipm['dat_consu'].dt.year
        # Fill NaN values with a default value (e.g., 0) or you can choose a different approach
        ipm['annee'] = ipm['annee'].fillna(0).astype(int)
        st.success("Colonne 'annee' nettoyée avec succès.")

    # Display cleaned data
    st.header(f"Contenu du fichier après nettoyage: {list(ipm.keys())[0]}")
    st.dataframe(ipm.head(6))

else:
    st.warning("Veuillez d'abord télécharger les fichiers CSV sur la page d'accueil.")
