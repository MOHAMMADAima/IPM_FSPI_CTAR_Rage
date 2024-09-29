import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.colors as pc

# Set page title
st.set_page_config(page_title="MT", page_icon="")
st.title("Morsure Transdermique")


def plot_MT_ipm(ipm):
    
    # Get the first dataframe uploaded
    ipm=ipm.drop_duplicates(subset=['ref_mordu'])
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
    fig2 = px.bar(
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
    fig2.update_layout(
            title="Facteurs de risque des morsures transdermiques (MT) : âge, partie du corps, sexe et type d'animal",
            xaxis=dict(title="Groupe d'âge", tickfont=dict(size=10)),
            yaxis=dict(title="Nombre de MT", tickfont=dict(size=10)),
            legend=dict(title="Partie du corps :", orientation="h", yanchor="bottom", y=1.01, xanchor="auto", x=0.5),
            height=1900,  # Adjust the height as needed
            width=1000,
            margin=dict(b=400,t=500)  # Add margin at the bottom for the legend
        )

        # Zoom into individual subplots
    fig2.update_yaxes(matches=None)  # Allow individual zooming for subplots

        # Reduce the size of the 'typanim' value labels
    fig2.for_each_annotation(lambda a: a.update(text=a.text.split('=')[-1]))

        # Set the same size for all x and y labels
    fig2.update_xaxes(tickfont=dict(size=10))
    fig2.update_yaxes(tickfont=dict(size=10))

        # Align y-axis labels on the left
    fig2.update_yaxes(automargin=True)

        # Display the figure
    st.plotly_chart(fig2)



def plot_MT_peripheral(df):

    bins = list(range(0, 105, 5)) + [float('inf')]
    labels = [f'{i}-{i+4}' for i in bins[:-2]] + ['100+']

        # Categorize ages into defined bins
    age_groups = pd.cut(df['age'], bins=bins, labels=labels, right=False)
    df['Age Group'] = age_groups

        # Define body parts and columns to check for 'LPS' values
    body_parts = {
            'Tête et Cou': 'singes_des_legions___1',
            'Bras et Avant-bras': 'singes_des_legions___2',
            'Main': 'singes_des_legions___3',
            'Cuisse et Jambe': 'singes_des_legions___4',
            'Pied': 'singes_des_legions___5',
            'Autres': 'singes_des_legions___9',
            'Dos et Torse': 'singes_des_legions___6',
            'Parties génitales': 'singes_des_legions___7'
        }

    mt_counts = pd.DataFrame(columns=['Age Group', 'Body Part', 'Gender', 'MT Count'])

        # Count the number of 'MT' values for each body part, age group, and gender
    for part, column in body_parts.items():
            for gender in df['sexe'].dropna().unique():
                part_counts = df[(df[column] == 1) & (df.type_contact___5== 1)& (df['sexe'] == gender)].groupby('Age Group').size().reset_index(name='MT Count')
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
            height=900,  # Adjust the height as needed
            width=1000,
            margin=dict(b=100)  # Add margin at the bottom for the legend
        )

        # Display the figure
    st.plotly_chart(fig)




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
            plot_MT_ipm(df)

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
                    plot_MT_peripheral(df)
            elif all_ctars_selected:  
                plot_MT_peripheral(df)
           


