import streamlit as st
import pandas as pd
import plotly.express as px

# Set Streamlit page configuration
st.set_page_config(page_title="Analyse LPS par Groupe d'Âge", page_icon="📊")

# Check if dataframes are available in session state
if 'dataframes' in st.session_state:
    dataframes = st.session_state['dataframes']
    
    # Select a file to analyze from the uploaded files
    selected_file = st.selectbox("Sélectionnez un fichier pour l'analyse", options=list(dataframes.keys()))

    # Load the selected dataframe
    if selected_file:
        ipm = dataframes[selected_file]

        # Define age groups with 5-year intervals from 0 to 100, with the last group being 100+
        bins = list(range(0, 105, 5)) + [float('inf')]
        labels = [f'{i}-{i+4}' for i in bins[:-2]] + ['100+']

        # Categorize ages into defined bins
        age_groups = pd.cut(ipm['age'], bins=bins, labels=labels, right=False)
        ipm['Age Group'] = age_groups

        # Define body parts and columns to check for 'LPS' values
        body_parts = {
            'Tête': 'tet_cont',
            'Bras et avant-bras': 'm_sup_cont',
            'Main': 'ext_s_cont',
            'Cuisse et Jambe': 'm_inf_cont',
            'Pied': 'ext_i_cont',
            'Abdomen': 'abdo_cont',
            'Dos': 'dos_cont',
            'Parties génitales': 'geni_cont'
        }

        # Create a DataFrame to store the counts of 'LPS' values for each body part and age group
        lps_counts = pd.DataFrame(columns=['Age Group', 'Body Part', 'LPS Count'])

        # Count the number of 'LPS' values for each body part and age group
        for part, column in body_parts.items():
            part_counts = ipm[ipm[column] == 'LPS'].groupby('Age Group').size().reset_index(name='LPS Count')
            part_counts['Body Part'] = part
            lps_counts = pd.concat([lps_counts, part_counts], ignore_index=True)

        # Create a multi-bar plot
        fig = px.bar(
            lps_counts, 
            x='Age Group', 
            y='LPS Count', 
            color='Body Part', 
            barmode='group',
            title="Proportion des patients qui ont l'exposition de catégorie 1 (léchage de la peau saine 'LPS') par âge et partie du corps",
            labels={'LPS Count': 'Nombre de LPS', 'Age Group': 'Groupe d\'âge', 'Body Part': 'Partie du corps'}
        )

        # Display the figure
        st.plotly_chart(fig)

else:
    st.error("Aucun fichier n'a été téléchargé. Veuillez retourner à la page d'accueil pour télécharger un fichier.")

# Sidebar container with fixed width
with st.sidebar.container():
    st.image("Logo-CORAMAD.jpg", use_column_width=True, width=250, caption="FSPI Rage")
