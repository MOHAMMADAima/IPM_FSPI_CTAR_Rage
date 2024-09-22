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

        # Function to create a pie chart
        def create_pie_chart(df, label_col, count_col, title):
            # Count occurrences
            counts = df[label_col].value_counts().reset_index()
            counts.columns = [label_col, count_col]

            # Create the pie chart
            fig = go.Figure(go.Pie(
                labels=counts[label_col],
                values=counts[count_col],
                textinfo='label+percent',
                marker=dict(colors=['rgb(48, 63, 159)', 'rgb(233, 30, 99)', 'rgb(76, 175, 80)'][:len(counts)]),
            ))

            # Update layout for better visualization
            fig.update_layout(
                title_text=title,
                margin=dict(t=40, l=40, r=40, b=40),
                showlegend=True,
            )

            return fig

        # If the selected file is the IPM dataset
        if selected_file == "CTAR_ipmdata20022024_cleaned.csv":
            df_clean = df.drop_duplicates(subset=['ref_mordu'])
            # Plot for animals
            fig_animals = create_pie_chart(df_clean, 'animal', 'count', "Répartition des espèces responsables de morsures (IPM)")
            st.plotly_chart(fig_animals)

            # Selection box for animals
            selected_animal = st.selectbox("Sélectionnez un animal pour voir le type d'animal", options=df_clean['typanim'].dropna().unique())

            # Filter DataFrame for the selected animal
            filtered_df = df_clean[df_clean['typanim'] == selected_animal]
            fig_typanim = create_pie_chart(filtered_df, 'typanim', 'count', f"Répartition des types d'animaux pour : {selected_animal} (IPM)")
            st.plotly_chart(fig_typanim)

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

            # Plot for animals
            fig_animals_ctar = create_pie_chart(filtered_df, 'espece', 'count', "Répartition des espèces responsables de morsures (CTAR)")
            st.plotly_chart(fig_animals_ctar)

            # Selection box for animals
            selected_animal_ctar = st.selectbox("Sélectionnez un animal pour voir le type d'animal", options=filtered_df['espece'].dropna().unique())

            # Filter DataFrame for the selected animal
            filtered_df_ctar = filtered_df[filtered_df['espece'] == selected_animal_ctar]
            fig_typanim_ctar = create_pie_chart(filtered_df_ctar, 'dev_carac', 'count', f"Répartition des types d'animaux pour : {selected_animal_ctar} (CTAR)")
            st.plotly_chart(fig_typanim_ctar)

            # Get unique animals excluding NaN
            unique_animals = filtered_df['espece'].dropna().unique()

            # Dropdown for selecting an animal for detailed view
            selected_animal_detail = st.selectbox("Sélectionnez un animal à analyser", options=unique_animals)

            if selected_animal_detail:
                # Filter DataFrame for the selected animal
                df_animal = filtered_df[filtered_df['espece'] == selected_animal_detail]
                
                # Count occurrences of each typeanimal for the selected animal
                typeanimal_counts = df_animal['dev_carac'].value_counts().reset_index()
                typeanimal_counts.columns = ['dev_carac', 'count']

                # Create the pie chart for the selected animal's typeanimal
                fig_animal = create_pie_chart(df_animal, 'dev_carac', 'count', f"Mode de vie de l'animal mordant : {selected_animal_detail}")

                # Display the figure
                st.plotly_chart(fig_animal)

else:
    st.error("Aucun fichier n'a été téléchargé. Veuillez retourner à la page d'accueil pour télécharger un fichier.")

# Sidebar container with fixed width
with st.sidebar.container():
    st.image("Logo-CORAMAD.jpg", use_column_width=True, width=250, caption="FSPI Rage")
