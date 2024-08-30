import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page title
st.set_page_config(page_title="Animal Lifestyle Analysis", page_icon="🐾")

# Streamlit page
st.title("Mode de vie de l'espèce responsable de la morsure des patients IPM.")

# Check if dataframes are available in session state
if 'dataframes' in st.session_state:
    dataframes = st.session_state['dataframes']
    
    # Select a file to analyze from the uploaded files
    selected_file = st.selectbox("Sélectionnez un fichier pour l'analyse", options=list(dataframes.keys()))

    # Load the selected dataframe
    if selected_file:
        ipm = dataframes[selected_file]

        # Get unique animals excluding NaN
        unique_animals = ipm['animal'].dropna().unique()

        # Define a modern color palette (using RGB values)
        modern_colors = [
            'rgb(48, 63, 159)',    # Indigo
            'rgb(233, 30, 99)',    # Pink
            'rgb(76, 175, 80)',    # Green
            'rgb(255, 152, 0)',    # Orange
            'rgb(121, 85, 72)',    # Brown
            'rgb(63, 81, 181)',    # Blue
            'rgb(255, 87, 34)',    # Deep Orange
            'rgb(0, 188, 212)',    # Cyan
            'rgb(255, 193, 7)',    # Amber
            'rgb(255, 235, 59)',   # Yellow
        ]

        # Mapping for label replacement
        label_mapping = {
            'A': 'Sauvage',
            'B': 'Errant disparu',
            'C': 'Errant vivant',
            'D': 'Domestique propriétaire connu',
            'E': 'Domestique disparu',
            'F': 'Domestique abbatu',
            'G': 'Domestique mort'
        }

        # Dropdown for selecting an animal
        selected_animal = st.selectbox("Sélectionnez un animal à analyser", options=unique_animals)

        if selected_animal:
            # Filter DataFrame for the selected animal
            df_animal = ipm[ipm['animal'] == selected_animal]
            
            # Count unique categories of typeanimal for the selected animal
            unique_categories = df_animal['typanim'].nunique()
            
            if unique_categories == 1:
                # Create a simple pie chart for single category
                fig = go.Figure(go.Pie(
                    labels=[label_mapping[df_animal['typanim'].iloc[0]]],  # Replace label according to mapping
                    values=[len(df_animal)],
                    name=selected_animal,  # Set legend name
                    marker=dict(colors=[modern_colors[0]]),  # Set color using the modern color palette
                ))
                
                # Update layout for better visualization
                fig.update_layout(
                    title_text=f"Mode de vie de l'animal mordant : {selected_animal}",
                    margin=dict(t=40, l=40, r=40, b=40),  # Adjust margins
                    showlegend=True,
                )
            else:
                # Count occurrences of each typeanimal for the selected animal
                typeanimal_counts = df_animal['typanim'].value_counts().reset_index()
                typeanimal_counts.columns = ['typanim', 'count']
                
                # Replace labels according to mapping
                typeanimal_counts['typanim'] = typeanimal_counts['typanim'].replace(label_mapping)
                
                # Create the pie chart for multiple categories
                fig = go.Figure(go.Pie(
                    labels=typeanimal_counts['typanim'],
                    name=selected_animal,
                    values=typeanimal_counts['count'],
                    marker=dict(colors=modern_colors[:len(typeanimal_counts)]),  # Use modern colors
                ))
                
                # Update layout for better visualization
                fig.update_layout(
                    title_text=f"Mode de vie de l'animal mordant : {selected_animal}",
                    margin=dict(t=40, l=40, r=40, b=40),  # Adjust margins
                    showlegend=True,
                )

            # Display the figure
            st.plotly_chart(fig)

else:
    st.error("Aucun fichier n'a été téléchargé. Veuillez retourner à la page d'accueil pour télécharger un fichier.")

# Sidebar container with fixed width
with st.sidebar.container():
    st.image("Logo-CORAMAD.jpg", use_column_width=True, width=250, caption="FSPI Rage")
