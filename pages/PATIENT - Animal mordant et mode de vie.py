import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page title
st.set_page_config(page_title="Espèce responsable pour la morsure", page_icon="🐕")
st.title("Espèce responsable pour la morsure des patients")

# Check if dataframes are available in session state
if 'dataframes' in st.session_state:
    dataframes = st.session_state['dataframes']

    # Select a file to analyze from the uploaded files
    selected_file = st.selectbox("Sélectionnez un fichier pour l'analyse", options=list(dataframes.keys()))

    # Load the selected dataframe and check if it's IPM or CTAR data
    if selected_file:
        df = dataframes[selected_file]

        # If the selected file is the IPM dataset
        if selected_file == "CTAR_ipmdata20022024_cleaned.csv":
            # Drop duplicates based on the 'ref_mordu' column to get unique entries
            df_clean = df.drop_duplicates(subset=['ref_mordu'])

            # Step 1: Count occurrences of each 'animal'
            animal_counts = df_clean['animal'].value_counts().reset_index()
            animal_counts.columns = ['animal', 'count']

            # Calculate the number of non-null rows in the 'animal' column
            non_null_count = df_clean['animal'].notnull().sum()

            # Step 2: Create the donut pie chart for IPM data
            fig = go.Figure(go.Pie(
                labels=animal_counts['animal'],
                values=animal_counts['count'],
                hole=0.6,  # Adjust the size of the hole to make the donut bigger
                textinfo='label+percent',  # Show label and percentage
                textposition='inside',  # Position text inside the slices
            ))

            # Update layout for better visualization
            fig.update_layout(
                title_text=f"Espèce responsable de la morsure des patients IPM (parmi {non_null_count} animaux).",
                annotations=[
                    dict(text='Animaux mordeurs', x=0.5, y=0.5, font_size=15, showarrow=False),
                ],
                margin=dict(t=30, l=30, r=30, b=30),  # Adjust margins to make the chart bigger
            )

            # Add custom annotation
            fig.add_annotation(
                text="Source des données : IPM",
                x=0.5, y=-0.2,  # Adjust y to position the text below the chart
                showarrow=False,
                font=dict(size=12),
            )

            # Show the plot
            st.plotly_chart(fig)

        # If the selected file is the CTAR peripheral dataset
        elif selected_file == "CTAR_peripheriquedata20022024_cleaned.csv":
            # Drop rows with NaN in the 'espece' column
            df_clean = df.dropna(subset=['espece'])

            # Step 1: Count occurrences of each 'espece'
            animal_counts = df_clean['espece'].value_counts().reset_index()
            animal_counts.columns = ['espece', 'count']

            # Calculate the number of non-null rows in the 'espece' column
            non_null_count = df_clean['espece'].notnull().sum()

            # Step 2: Create the donut pie chart for CTAR data
            fig = go.Figure(go.Pie(
                labels=animal_counts['espece'],
                values=animal_counts['count'],
                hole=0.6,  # Adjust the size of the hole to make the donut bigger
                textinfo='label+percent',  # Show label and percentage
                textposition='inside',  # Position text inside the slices
            ))

            # Update layout for better visualization
            fig.update_layout(
                title_text=f"Espèce responsable de la morsure des patients CTAR périphériques (parmi {non_null_count} animaux).",
                annotations=[
                    dict(text='Animaux mordeurs', x=0.5, y=0.5, font_size=15, showarrow=False),
                ],
                margin=dict(t=30, l=30, r=30, b=30),  # Adjust margins to make the chart bigger
            )

            # Add custom annotation below the pie chart
            fig.add_annotation(
                text="Source des données : CTAR périphériques",
                x=0.5, y=-0.2,  # Adjust y to position the text below the chart
                showarrow=False,
                font=dict(size=12),
            )

            # Show the pie chart
            st.plotly_chart(fig)

else:
    st.error("Aucun fichier n'a été téléchargé. Veuillez retourner à la page d'accueil pour télécharger un fichier.")

# Sidebar container with fixed width
with st.sidebar.container():
    st.image("Logo-CORAMAD.jpg", use_column_width=True, width=250, caption="FSPI Rage")
