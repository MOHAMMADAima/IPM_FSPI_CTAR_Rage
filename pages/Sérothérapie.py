import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Set Streamlit page configuration
st.set_page_config(page_title="Analyse de la Sérothérapie", page_icon="💉", layout="wide")

st.title("Analyse de la Sérothérapie par Catégorie de Poids")

# Check if dataframes are available in session state
if 'dataframes' in st.session_state:
    dataframes = st.session_state['dataframes']

    # Select a file to analyze from the uploaded files
    selected_file = st.selectbox("Sélectionnez un fichier pour l'analyse", options=list(dataframes.keys()))

    # Load the selected dataframe
    if selected_file:
        df = dataframes[selected_file]

        # Convert 'poids' to numeric (in case there are any non-numeric values)
        df['poids'] = pd.to_numeric(df['poids'], errors='coerce')

        # Discretize 'poids' into bins of width 10
        df['weight_bin'] = pd.cut(df['poids'], bins=np.arange(0, df['poids'].max() + 10, 10), right=False)

        # Aggregate data to calculate count of OUI and NON in each weight bin
        df_agg = df.groupby(['serother', 'weight_bin']).size().reset_index(name='count')

        # Calculate number of occurrences of 'OUI' and 'NON'
        oui_count = df[df['serother'] == 'OUI'].shape[0]
        non_count = df[df['serother'] == 'NON'].shape[0]

        # Create sunburst plot
        fig = px.sunburst(
            df_agg,
            path=['serother', 'weight_bin'],
            values='count',
            title="Proportion de patients venus au CTAR IPM pour une sérothérapie",
            labels={'serother': 'Sérothérapie', 'weight_bin': 'Catégorie de poids', 'count': 'Nombre'},
        )

        # Update layout with color settings and title
        fig.update_layout(
            margin=dict(t=40, l=0, r=0, b=0),
            sunburstcolorway=["#636efa", "#ef553b"],
            title="Proportion de patients venus au CTAR IPM pour une sérothérapie",
        )

        # Display the figure
        st.plotly_chart(fig)

else:
    st.error("Aucun fichier n'a été téléchargé. Veuillez retourner à la page d'accueil pour télécharger un fichier.")
