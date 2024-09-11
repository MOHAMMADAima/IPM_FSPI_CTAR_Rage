import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.colors as pc

# Streamlit page
st.title("Affluence des patients (H/F) venus au CTAR IPM sur période saisonnière d'une année.")

# Check if any dataframes have been uploaded in the session state
if 'dataframes' in st.session_state and st.session_state['dataframes']:
    # Get the first dataframe uploaded
    df_name, ipm = next(iter(st.session_state['dataframes'].items()))

    # Display main page content
    st.header(f"Contenu du fichier avant nettoyage: {list(ipm.keys())[0]}")
    st.dataframe(ipm.head(10))
