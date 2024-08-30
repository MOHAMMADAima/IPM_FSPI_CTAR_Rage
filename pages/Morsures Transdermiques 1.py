import streamlit as st
import pandas as pd
import plotly.express as px

# Set Streamlit page configuration
st.set_page_config(page_title="Analyse des Morsures Transdermiques", page_icon="📊")

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

        # Define body parts and columns to check for 'MT' values
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

        # Create a DataFrame to store the counts of 'MT' values for each body part, age group, and gender
        mt_counts = pd.DataFrame(columns=['Age Group', 'Body Part', 'Gender', 'MT Count'])

        # Count the number of 'MT' values for each body part, age group, and gender
        for part, column in body_parts.items():
            for gender in ipm['sexe'].dropna().unique():
                part_counts = ipm[(ipm[column] == 'MT') & (ipm['sexe'] == gender)].groupby('Age Group').size().reset_index(name='MT Count')
                part_counts['Body Part'] = part
                part_counts['Gender'] = gender
                mt_counts = pd.concat([mt_counts, part_counts], ignore_index=True)

        # Create a multi-bar plot
        fig = px.bar(
            mt_counts,
            x='Age Group', 
            y='MT Count', 
            color='Body Part', 
            barmode='group',
            facet_col='Gender', 
            facet_col_wrap=2,
            title="Nombre de lésions 'MT' par groupe d'âge, partie du corps et sexe",
            labels={
                'MT Count': 'Nombre de MT', 
                'Age Group': "Groupe d'âge", 
                'Body Part': 'Partie du corps', 
                'Gender': 'Sexe'
            },
            category_orders={'Gender': ['M', 'F']}
        )

        # Update layout
        fig.update_layout(
            title="Facteurs de risque des morsures transdermiques (âge, partie du corps et genre)",
            xaxis=dict(title="Groupe d'âge"),
            yaxis=dict(title="Nombre de Morsure Transdermique"),
            legend=dict(title="Partie du corps", orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.6),
            height=700,  # Adjust the height as needed
            width=1000,
            margin=dict(b=100)  # Add margin at the bottom for the legend
        )

        # Display the figure
        st.plotly_chart(fig)

else:
    st.error("Aucun fichier n'a été téléchargé. Veuillez retourner à la page d'accueil pour télécharger un fichier.")

# Sidebar container with fixed width
with st.sidebar.container():
    st.image("Logo-CORAMAD.jpg", use_column_width=True, width=250, caption="FSPI Rage")