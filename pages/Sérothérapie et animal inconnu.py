import streamlit as st
import pandas as pd
import plotly.express as px

# Set Streamlit page configuration
st.set_page_config(page_title="Analyse de Sérothérapie", page_icon="💉", layout="wide")

st.title("Analyse des Patients Mordus par Type d'Animal et Sérothérapie")

# Check if dataframes are available in session state
if 'dataframes' in st.session_state:
    dataframes = st.session_state['dataframes']

    # Select a file to analyze from the uploaded files
    selected_file = st.selectbox("Sélectionnez un fichier pour l'analyse", options=list(dataframes.keys()))

    # Load the selected dataframe
    if selected_file:
        df = dataframes[selected_file]

        # Step 1: Filter the DataFrame for specific animal types
        filtered_df = df[df['typanim'].isin(['A', 'B', 'C'])]

        # Step 2: Count the occurrences of 'OUI' and 'NON' in the 'vacc_ant' column, grouped by 'serother' column
        vacc_ant_serother_counts = filtered_df.groupby(['vacc_ant', 'serother']).size().reset_index(name='Count')

        # Step 3: Plot the result using Plotly
        fig = px.bar(
            vacc_ant_serother_counts,
            x='vacc_ant',
            y='Count',
            color='serother',
            labels={
                'vacc_ant': 'Antécédent vaccin antirabbique',
                'Count': 'Nombre de patients',
                'serother': 'Sérotherapie'
            },
            title='Patients mordus par un animal inconnu (Sauvage, Errant disparu, Errant vivant) ayant eu sérothérapie'
        )

        # Display the bar chart
        st.plotly_chart(fig)

        # Display the counts in Streamlit for better visibility
        st.write("Détails des comptes des patients par sérothérapie:")
        st.dataframe(vacc_ant_serother_counts)

else:
    st.error("Aucun fichier n'a été téléchargé. Veuillez retourner à la page d'accueil pour télécharger un fichier.")


# Sidebar container with fixed width
with st.sidebar.container():
    st.image("Logo-CORAMAD.jpg", use_column_width=True, width=250, caption="FSPI Rage")
