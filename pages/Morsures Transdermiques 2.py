import streamlit as st
import pandas as pd
import plotly.express as px

# Set Streamlit page configuration
st.set_page_config(page_title="Analyse des Morsures Transdermiques par Type d'Animal", page_icon="🐾", layout="wide")

st.title("Analyse des Morsures Transdermiques par Groupe d'Âge, Partie du Corps, Sexe et Type d'Animal")

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

        # Map animal type letters to the corresponding labels
        animal_type_mapping = {
            'A': 'Sauvage', 
            'B': 'Errant disparu', 
            'C': 'Errant vivant', 
            'D': 'Domestique Propriétaire Connu', 
            'E': 'Domestique Disparu', 
            'F': 'Domestique Abbatu', 
            'G': 'Domestique Mort'
        }

        # Replace 'typanim' column values with the corresponding labels
        ipm['typanim'] = ipm['typanim'].map(animal_type_mapping)

        # Create a DataFrame to store the counts of 'MT' values for each body part, age group, gender, and animal type
        mt_counts = pd.DataFrame(columns=['Age Group', 'Body Part', 'Gender', 'Animal Type', 'MT Count'])

        # Count the number of 'MT' values for each body part, age group, gender, and animal type
        for part, column in body_parts.items():
            for gender in ipm['sexe'].dropna().unique():
                for animal_type in ipm['typanim'].dropna().unique():
                    part_counts = ipm[(ipm[column] == 'MT') & (ipm['sexe'] == gender) & (ipm['typanim'] == animal_type)].groupby('Age Group').size().reset_index(name='MT Count')
                    part_counts['Body Part'] = part
                    part_counts['Gender'] = gender
                    part_counts['Animal Type'] = animal_type
                    mt_counts = pd.concat([mt_counts, part_counts], ignore_index=True)

        # Replace 'M' and 'F' with male and female icons
        gender_icons = {'M': '♂', 'F': '♀'}
        mt_counts['Gender'] = mt_counts['Gender'].map(gender_icons)

        # Create a multi-bar plot
        fig = px.bar(
            mt_counts, 
            x='Age Group', 
            y='MT Count', 
            color='Body Part', 
            barmode='group',
            facet_col='Gender', 
            facet_col_wrap=2, 
            facet_row='Animal Type',
            title="Nombre de lésions 'MT' par groupe d'âge, partie du corps, sexe et type d'animal",
            labels={
                'MT Count': 'Nombre de MT', 
                'Age Group': "Groupe d'âge", 
                'Body Part': 'Partie du corps', 
                'Gender': 'Sexe', 
                'Animal Type': ''
            },
            category_orders={
                'Gender': ['♂', '♀'], 
                'Animal Type': sorted(animal_type_mapping.values())  # Use mapped values for sorting
            }
        )

        # Update layout
        fig.update_layout(
            title="Facteurs de risque des morsures transdermiques (MT) : âge, partie du corps, sexe et type d'animal",
            xaxis=dict(title="Groupe d'âge", tickfont=dict(size=10)),
            yaxis=dict(title="Nombre de MT", tickfont=dict(size=10)),
            legend=dict(title="Partie du corps :", orientation="h", yanchor="bottom", y=1.01, xanchor="auto", x=0.5),
            height=1600,  # Adjust the height as needed
            width=1000,
            margin=dict(b=250)  # Add margin at the bottom for the legend
        )

        # Zoom into individual subplots
        fig.update_yaxes(matches=None)  # Allow individual zooming for subplots

        # Reduce the size of the 'typanim' value labels
        fig.for_each_annotation(lambda a: a.update(text=a.text.split('=')[-1]))

        # Set the same size for all x and y labels
        fig.update_xaxes(tickfont=dict(size=10))
        fig.update_yaxes(tickfont=dict(size=10))

        # Align y-axis labels on the left
        fig.update_yaxes(automargin=True)

        # Display the figure
        st.plotly_chart(fig)

else:
    st.error("Aucun fichier n'a été téléchargé. Veuillez retourner à la page d'accueil pour télécharger un fichier.")


# Sidebar container with fixed width
with st.sidebar.container():
    st.image("Logo-CORAMAD.jpg", use_column_width=True, width=250, caption="FSPI Rage")
