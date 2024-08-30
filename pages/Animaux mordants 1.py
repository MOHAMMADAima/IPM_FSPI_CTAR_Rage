import streamlit as st
import pandas as pd
import plotly.graph_objects as go


st.set_page_config(page_title="Animal Bite Analysis", page_icon="🐾")
# Streamlit page
st.title("Espèce responsable de la morsure des patients IPM.")

# Check if dataframes are available in session state
if 'dataframes' in st.session_state:
    dataframes = st.session_state['dataframes']
    
    # Select a file to analyze from the uploaded files
    selected_file = st.selectbox("Sélectionnez un fichier pour l'analyse", options=list(dataframes.keys()))

    # Load the selected dataframe
    if selected_file:
        ipm = dataframes[selected_file]

        # Step 1: Count occurrences of each 'animal'
        animal_counts = ipm['animal'].value_counts().reset_index()
        animal_counts.columns = ['animal', 'count']

        # Calculate the number of non-null rows in the 'animal' column
        non_null_count = ipm['animal'].notnull().sum()

        # Step 2: Create the donut pie chart
        fig = go.Figure(go.Pie(
            labels=animal_counts['animal'],
            values=animal_counts['count'],
            hole=0.6,  # Adjust the size of the hole to make the donut bigger
            textinfo='label+percent',  # Show label and percentage
            textposition='inside',  # Position text inside the slices
        ))

        # Update layout for better visualization
        fig.update_layout(
            title_text=f"Espèce responsable de la morsure des patients IPM (parmis {non_null_count} animaux).",
            annotations=[
                dict(text='Animaux mordeurs', x=0.5, y=0.5, font_size=15, showarrow=False),
            ],
            margin=dict(t=30, l=30, r=30, b=30),  # Adjust margins to make the chart bigger
        )

        # Add custom annotation
        fig.add_annotation(
            text="Text below the pie chart",
            x=0.6, y=-0.25,  # Adjust y to position the text below the chart
            showarrow=False,
            font=dict(size=12),
        )

        # Show the plot
        st.plotly_chart(fig)

else:
    st.error("Aucun fichier n'a été téléchargé. Veuillez retourner à la page d'accueil pour télécharger un fichier.")

# Sidebar container with fixed width
with st.sidebar.container():
    st.image("Logo-CORAMAD.jpg", use_column_width=True, width=250, caption="FSPI Rage")