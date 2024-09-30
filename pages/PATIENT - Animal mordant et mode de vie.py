import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page title
st.set_page_config(page_title="Espèce responsable pour la morsure", page_icon="🐕")
st.title("Espèce responsable pour la morsure des patients")

# Label mapping for typanim values
label_mapping = {
    'A': 'Sauvage',
    'B': 'Errant disparu',
    'C': 'Errant vivant',
    'D': 'Domestique propriétaire connu',
    'E': 'Domestique disparu',
    'F': 'Domestique abbatu',
    'G': 'Domestique mort'
}
# Function to create a donut chart with conditional margin
def create_donut_chart(df, label_col, count_col, title, is_peripherique=False):
            counts = df[label_col].value_counts().reset_index()
            counts.columns = [label_col, count_col]

            # Create the donut chart
            fig = go.Figure(go.Pie(
                labels=counts[label_col],
                values=counts[count_col],
                hole=0.6,
                textinfo='label+percent',
                marker=dict(colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0'][:len(counts)]),
                direction='clockwise'
            ))

            # Update layout for better visualization, reduce top margin if CSV is peripherique
            top_margin = 50 if is_peripherique else 100  # Adjust top margin here
            fig.update_layout(
                title_text=title,
                margin=dict(t=top_margin, l=70, r=70, b=40),  # Adjust margins
                height=800,
                width=1000,
                showlegend=True,
            )

            return fig

        # Function to create a pie chart with conditional margin
def create_pie_chart(df, label_col, count_col, title, is_peripherique=False):
            counts = df[label_col].value_counts().reset_index()
            counts.columns = [label_col, count_col]

            # Create the pie chart
            fig = go.Figure(go.Pie(
                labels=counts[label_col],
                values=counts[count_col],
                textinfo='label+percent',
                marker=dict(colors=['#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'][:len(counts)]),
            ))

            # Update layout for better visualization, reduce top margin if CSV is peripherique
            top_margin = 50 if is_peripherique else 100  # Adjust top margin here
            fig.update_layout(
                title_text=title,
                margin=dict(t=top_margin, l=80, r=70, b=40),  # Adjust margins
                height=500,
                width=600,
                showlegend=True,
            )

            return fig


        
        
def anim_mord(df):
                df_clean = df.drop_duplicates(subset=['ref_mordu'])

                # Selection box for animals
                selected_animal = st.selectbox("Sélectionnez un animal pour voir le type d'animal", options=df_clean['animal'].dropna().unique())

                # Filter DataFrame for the selected animal
                filtered_df = df_clean[df_clean['animal'] == selected_animal]

                # Replace typanim labels with mapped values
                filtered_df['typanim'] = filtered_df['typanim'].map(label_mapping)

                # Plot for typanim (donut chart) first
                fig_typanim = create_donut_chart(filtered_df, 'typanim', 'count', f"Répartition des types d'animaux pour : {selected_animal} (IPM)")
                st.plotly_chart(fig_typanim, use_container_width=True)

                # Allow user to select additional animals
                additional_animals = df_clean['animal'].value_counts().index.tolist()
                selected_additional = st.multiselect("Sélectionnez d'autres animaux à afficher", options=additional_animals, default=additional_animals[:4])

                # Filter for selected additional animals
                if selected_additional:
                    filtered_additional = df_clean[df_clean['animal'].isin(selected_additional)]
                    fig_additional_animals = create_pie_chart(filtered_additional, 'animal', 'count', "Répartition des espèces responsables de morsures (Animaux Sélectionnés)")
                    st.plotly_chart(fig_additional_animals, use_container_width=True)

def anim_mord_perif(df):
            df = df.dropna(subset=['espece'])
            selected_animal = st.selectbox("Sélectionnez un animal pour voir le type d'animal", options=df['espece'].dropna().unique())


            df = df[~df['dev_carac'].astype(str).str.contains('nan-nan|nan-|nan-|-nan', regex=True)]
            # Allow user to select additional animals
            additional_animals = df['espece'].value_counts().index.tolist()


            fig_typanim_ctar = create_donut_chart(df, 'dev_carac', 'count', f"Répartition du mode de vie de l'animal pour : {len(df[df.espece==selected_animal])}  {selected_animal}s ", is_peripherique=True)
            st.plotly_chart(fig_typanim_ctar, use_container_width=True)

            selected_additional = st.multiselect("Sélectionnez d'autres animaux à afficher", options=additional_animals, default=additional_animals[:4])


            
            # Filter for selected additional animals
            if selected_additional:
                filtered_additional = df[df['espece'].isin(selected_additional)]
            fig_additional_animals = create_pie_chart(filtered_additional, 'espece', 'count', f"Répartition des espèces responsables de morsures ({len(filtered_additional)} animaux)", is_peripherique=True)
            st.plotly_chart(fig_additional_animals, use_container_width=True)
            



# Main Streamlit logic
if 'dataframes' in st.session_state:
    dataframes = st.session_state['dataframes']

    # Select a file to analyze from the uploaded files
    selected_file = st.selectbox("Sélectionnez un fichier pour l'analyse", options=list(dataframes.keys()))

    # Load the selected dataframe
    if selected_file:
        df = dataframes[selected_file]

        # If the selected file is the IPM dataset
        if selected_file == "CTAR_ipmdata20022024_cleaned.csv":
            anim_mord(df)

        # If the selected file is the peripheral CTAR dataset
        elif selected_file == "CTAR_peripheriquedata20022024_cleaned.csv":
            # Drop rows with NaN in 'id_ctar' column
            df = df.dropna(subset=['id_ctar'])

            # Get the unique CTARs
            unique_ctars = df['id_ctar'].unique()

            # Separate the "Tous les CTAR" option from the multiselect
            all_ctars_selected = st.checkbox("Sélectionnez tous les CTARs")

            if not all_ctars_selected:
                selected_ctars = st.multiselect(
                    "Sélectionnez un ou plusieurs CTARs",
                    options=list(unique_ctars))
                if not selected_ctars:
                    st.warning("Veuillez sélectionner au moins un CTAR pour afficher l'analyse.")
                else:
                    df= df[df['id_ctar'].isin(selected_ctars)]
                    anim_mord_perif(df)
            elif all_ctars_selected:  
                anim_mord_perif(df)
           

else:
    st.error("Aucun fichier n'a été téléchargé. Veuillez retourner à la page d'accueil pour télécharger un fichier.")

# Sidebar container with fixed width
with st.sidebar.container():
    st.image("Logo-CORAMAD.jpg", use_column_width=True, width=250, caption="FSPI Rage")

