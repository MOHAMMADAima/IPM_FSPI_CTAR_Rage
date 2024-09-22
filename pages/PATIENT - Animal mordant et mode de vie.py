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

        # Function to create a double-layer pie chart
        def create_double_pie_chart(df, animal_col, count_col, type_col, title, source):
            # Count occurrences
            animal_counts = df[animal_col].value_counts().reset_index()
            animal_counts.columns = [animal_col, count_col]

            type_counts = df[type_col].value_counts().reset_index()
            type_counts.columns = [type_col, f'{type_col}_count']

            # Calculate the number of non-null rows
            non_null_count = df[animal_col].notnull().sum()

            # Create the double-layer pie chart
            fig = go.Figure()

            # Outer layer
            fig.add_trace(go.Pie(
                labels=animal_counts[animal_col],
                values=animal_counts[count_col],
                hole=0.4,
                textinfo='label+percent',
                textposition='inside',
                name='Animaux'
            ))

            # Inner layer
            fig.add_trace(go.Pie(
                labels=type_counts[type_col],
                values=type_counts[f'{type_col}_count'],
                hole=0.7,
                textinfo='label+percent',
                textposition='inside',
                name='Type d\'animal'
            ))

            # Update layout for better visualization
            fig.update_layout(
                title_text=f"{title} (parmi {non_null_count} animaux).",
                annotations=[dict(text='Animaux mordeurs', x=0.5, y=0.5, font_size=15, showarrow=False)],
                margin=dict(t=30, l=30, r=30, b=30),
            )

            # Add custom annotation
            fig.add_annotation(
                text=f"Source des données : {source}",
                x=0.5, y=-0.2,
                showarrow=False,
                font=dict(size=12),
            )

            return fig

        # If the selected file is the IPM dataset
        if selected_file == "CTAR_ipmdata20022024_cleaned.csv":
            df_clean = df.drop_duplicates(subset=['ref_mordu'])
            fig = create_double_pie_chart(df_clean, 'animal', 'count', 'typanim', "Espèce responsable de la morsure des patients IPM", "IPM")
            st.plotly_chart(fig)

        # If the selected file is the CTAR peripheral dataset
        elif selected_file == "CTAR_peripheriquedata20022024_cleaned.csv":
            df_clean = df.dropna(subset=['espece'])

            # Multi-select for CTAR centers
            unique_ctar_centers = df_clean['id_ctar'].unique().tolist()
            unique_ctar_centers.insert(0, "Tous les CTAR")
            selected_ctars = st.multiselect("Sélectionnez les CTAR", options=unique_ctar_centers, default="Tous les CTAR")

            if "Tous les CTAR" in selected_ctars:
                filtered_df = df_clean
            else:
                filtered_df = df_clean[df_clean['id_ctar'].isin(selected_ctars)]

            fig = create_double_pie_chart(filtered_df, 'espece', 'count', 'caracteristique', "Espèce responsable de la morsure des patients CTAR périphériques", "CTAR périphériques")
            st.plotly_chart(fig)

            # Get unique animals excluding NaN
            unique_animals = filtered_df['espece'].dropna().unique()

            # Dropdown for selecting an animal
            selected_animal = st.selectbox("Sélectionnez un animal à analyser", options=unique_animals)

            if selected_animal:
                # Filter DataFrame for the selected animal
                df_animal = filtered_df[filtered_df['espece'] == selected_animal]
                
                # Count occurrences of each typeanimal for the selected animal
                typeanimal_counts = df_animal['catacteristique'].value_counts().reset_index()
                typeanimal_counts.columns = ['catacteristique', 'count']

                # Create the pie chart for the selected animal's typeanimal
                fig_animal = go.Figure(go.Pie(
                    labels=typeanimal_counts['catacteristique'],
                    values=typeanimal_counts['count'],
                    name=selected_animal,
                    textinfo='label+percent',
                    marker=dict(colors=['rgb(48, 63, 159)', 'rgb(233, 30, 99)', 'rgb(76, 175, 80)'][:len(typeanimal_counts)]),
                ))

                # Update layout for better visualization
                fig_animal.update_layout(
                    title_text=f"Mode de vie de l'animal mordant : {selected_animal}",
                    margin=dict(t=40, l=40, r=40, b=40),
                    showlegend=True,
                )

                # Display the figure
                st.plotly_chart(fig_animal)

else:
    st.error("Aucun fichier n'a été téléchargé. Veuillez retourner à la page d'accueil pour télécharger un fichier.")

# Sidebar container with fixed width
with st.sidebar.container():
    st.image("Logo-CORAMAD.jpg", use_column_width=True, width=250, caption="FSPI Rage")
