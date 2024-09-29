import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.colors as pc

# Set page title
st.set_page_config(page_title="Saison Morsure", page_icon="")
st.title("Exposition catégorie 1 (léchage sur peau saine LPS)")


def plot_cat1_ipm(ipm):
    
    # Get the first dataframe uploaded
    ipm=ipm.drop_duplicates(subset=['ref_mordu'])
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

    # Show the plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)

def plot_cat1_peripheral(df):

    bins = list(range(0, 105, 5)) + [float('inf')]
    labels = [f'{i}-{i+4}' for i in bins[:-2]] + ['100+']

        # Categorize ages into defined bins
    age_groups = pd.cut(df['age'], bins=bins, labels=labels, right=False)
    df['Age Group'] = age_groups

        # Define body parts and columns to check for 'LPS' values
    body_parts = {
            'Tête et Cou': 'singes_des_legions__1',
            'Bras et Avant-bras': 'singes_des_legions__2',
            'Main': 'singes_des_legions__3',
            'Cuisse et Jambe': 'singes_des_legions__4',
            'Pied': 'singes_des_legions__5',
            'Autres': 'singes_des_legions__9',
            'Dos et Torse': 'singes_des_legions__6',
            'Parties génitales': 'singes_des_legions__7'
        }

        # Create a DataFrame to store the counts of 'LPS' values for each body part and age group
    lps_counts = pd.DataFrame(columns=['Age Group', 'Body Part', 'LPS Count'])

        # Count the number of 'LPS' values for each body part and age group
    for part, column in body_parts.items():
            part_counts = df[df[column] == '1'].groupby('Age Group').size().reset_index(name='LPS Count')
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


    # Show the plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)

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
            plot_cat1_ipm(df)

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
                    plot_cat1_peripheral(df)
            elif all_ctars_selected:  
                plot_cat1_peripheral(df)
           


