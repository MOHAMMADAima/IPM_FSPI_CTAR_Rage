import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page title
st.set_page_config(page_title="Animal Lifestyle Analysis", page_icon="🐾")

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

        label_mapping = {
            'A': 'Sauvage',
            'B': 'Errant disparu',
            'C': 'Errant vivant',
            'D': 'Domestique propriétaire connu',
            'E': 'Domestique disparu',
            'F': 'Domestique abbatu',
            'G': 'Domestique mort'
        }

        figures = []
        for animal in unique_animals:
            df_animal = ipm[ipm['animal'] == animal]
            
            unique_categories = df_animal['typanim'].nunique()
            
            if unique_categories == 1:

                fig = go.Figure(go.Pie(
                    labels=[label_mapping[df_animal['typanim'].iloc[0]]],  
                    values=[len(df_animal)],
                    name=animal,  
                    marker=dict(colors=[modern_colors[0]]),  
                ))

                fig.update_layout(
                    title_text=f"Mode de vie de l'animal mordant : {animal}",
                    margin=dict(t=40, l=40, r=40, b=40),  # Adjust margins
                    showlegend=True,
                )
            else:
                # Count occurrences of each typeanimal for the current animal
                typeanimal_counts = df_animal['typanim'].value_counts().reset_index()
                typeanimal_counts.columns = ['typanim', 'count']
                
                # Replace labels according to mapping
                typeanimal_counts['typanim'] = typeanimal_counts['typanim'].replace(label_mapping)
                
                # Create the pie chart
                fig = go.Figure(go.Pie(
                    labels=typeanimal_counts['typanim'],
                    name=animal,
                    values=typeanimal_counts['count'],
                    marker=dict(colors=modern_colors[:len(typeanimal_counts)]),  # Use modern colors
                ))
                
                # Update layout for better visualization
                fig.update_layout(
                    title_text=f"Mode de vie de l'animal mordant : {animal}",
                    margin=dict(t=40, l=40, r=40, b=40),  # Adjust margins
                    showlegend=True,
                )
            
            # Add the figure to the list
            figures.append(fig)

        # Display the figures
        for idx, fig in enumerate(figures):
            st.plotly_chart(fig)
            st.markdown("<hr>", unsafe_allow_html=True)

else:
    st.error("Aucun fichier n'a été téléchargé. Veuillez retourner à la page d'accueil pour télécharger un fichier.")
