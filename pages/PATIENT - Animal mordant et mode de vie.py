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

            # Step 2: Count occurrences of 'tyanim'
            typanim_counts = df_clean['typanim'].value_counts().reset_index()
            typanim_counts.columns = ['typanim', 'tyanim_count']

            # Calculate the number of non-null rows in the 'animal' column
            non_null_count = df_clean['animal'].notnull().sum()

            # Step 3: Create the double-layer pie chart for IPM data
            fig = go.Figure()

            # Outer layer (animal counts)
            fig.add_trace(go.Pie(
                labels=animal_counts['animal'],
                values=animal_counts['count'],
                hole=0.4,
                textinfo='label+percent',
                textposition='inside',
                name='Animaux'
            ))

            # Inner layer (tyanim counts)
            fig.add_trace(go.Pie(
                labels=typanim_counts['typanim'],
                values=typanim_counts['tyanim_count'],
                hole=0.7,
                textinfo='label+percent',
                textposition='inside',
                name='Type d\'animal'
            ))

            # Update layout for better visualization
            fig.update_layout(
                title_text=f"Espèce responsable de la morsure des patients IPM (parmi {non_null_count} animaux).",
                annotations=[dict(text='Animaux mordeurs', x=0.5, y=0.5, font_size=15, showarrow=False)],
                margin=dict(t=30, l=30, r=30, b=30),
            )

            # Add custom annotation
            fig.add_annotation(
                text="Source des données : IPM",
                x=0.5, y=-0.2,
                showarrow=False,
                font=dict(size=12),
            )

            # Show the plot
            st.plotly_chart(fig)

        # If the selected file is the CTAR peripheral dataset
        elif selected_file == "CTAR_peripheriquedata20022024_cleaned.csv":
            # Drop rows with NaN in the 'espece' column
            df_clean = df.dropna(subset=['espece'])

            # Create a unique list of CTAR centers from the dataframe
            unique_ctar_centers = df_clean['id_ctar'].unique().tolist()
            unique_ctar_centers.insert(0, "Tous les CTAR")  # Add option for all CTARs

            # Multi-select for CTAR centers
            selected_ctars = st.multiselect("Sélectionnez les CTAR", options=unique_ctar_centers, default="Tous les CTAR")

            # Filter the dataframe based on selected CTARs
            if "Tous les CTAR" in selected_ctars:
                filtered_df = df_clean
            else:
                filtered_df = df_clean[df_clean['id_ctar'].isin(selected_ctars)]

            # Step 1: Count occurrences of each 'espece'
            animal_counts = filtered_df['espece'].value_counts().reset_index()
            animal_counts.columns = ['espece', 'count']

            # Step 2: Count occurrences of 'devenir'
            devenir_counts = filtered_df['devenir'].value_counts().reset_index()
            devenir_counts.columns = ['devenir', 'devenir_count']

            # Calculate the number of non-null rows in the 'espece' column
            non_null_count = filtered_df['espece'].notnull().sum()

            # Step 3: Create the double-layer pie chart for CTAR data
            fig = go.Figure()

            # Outer layer (animal counts)
            fig.add_trace(go.Pie(
                labels=animal_counts['espece'],
                values=animal_counts['count'],
                hole=0.4,
                textinfo='label+percent',
                textposition='inside',
                name='Espèces'
            ))

            # Inner layer (devenir counts)
            fig.add_trace(go.Pie(
                labels=devenir_counts['devenir'],
                values=devenir_counts['devenir_count'],
                hole=0.7,
                textinfo='label+percent',
                textposition='inside',
                name='Devenir'
            ))

            # Update layout for better visualization
            fig.update_layout(
                title_text=f"Espèce responsable de la morsure des patients CTAR périphériques (parmi {non_null_count} animaux).",
                annotations=[dict(text='Animaux mordeurs', x=0.5, y=0.5, font_size=15, showarrow=False)],
                margin=dict(t=30, l=30, r=30, b=30),
            )

            # Add custom annotation below the pie chart
            fig.add_annotation(
                text="Source des données : CTAR périphériques",
                x=0.5, y=-0.2,
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
