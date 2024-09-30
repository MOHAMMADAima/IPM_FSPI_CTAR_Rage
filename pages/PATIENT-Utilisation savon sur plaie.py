import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page title
st.set_page_config(page_title="Utilisation Savon", page_icon="🧼")
st.title("Lavage au savon sur plaie.")

def plot_age_sex_savon_distribution(ipm):
    
    ipm=ipm.drop_duplicates(subset=['ref_mordu'])
    # Convert 'age' column to numeric, coerce errors to NaN
    ipm['age'] = pd.to_numeric(ipm['age'], errors='coerce')

    # Drop rows with NaN in 'age' column
    ipmm = ipm.dropna(subset=['age'])

    # Count not null pairs (age, sexe, savon)
    not_null_pairs = ipmm[['age', 'sexe', 'savon']].notnull().all(axis=1).sum()

    # Group by age, sex, and soap, and count occurrences
    age_sex_savon_counts = ipmm.groupby(['age', 'sexe', 'savon']).size().reset_index(name='count')

    # Sort by age (now integers)
    age_sex_savon_counts = age_sex_savon_counts.sort_values(by='age')

    # Calculate total counts of 'OUI' and 'NON' for each sex
    total_counts = age_sex_savon_counts.groupby(['sexe', 'savon'])['count'].sum()

    # Calculate percentages within each age, sex, and soap group
    age_sex_savon_counts['percentage'] = age_sex_savon_counts.apply(
        lambda row: round((row['count'] / total_counts[row['sexe'], row['savon']]) * 100, 2)
        if total_counts[row['sexe'], row['savon']] != 0 else 0, axis=1
    )

    # Define color palette for bars
    color_palette = {
        ('M', 'OUI'): 'rgba(50, 171, 96, 0.6)',   # Green for 'M - Savon: OUI'
        ('M', 'NON'): 'rgba(50, 171, 96, 0.9)',   # Dark green for 'M - Savon: NON'
        ('F', 'OUI'): 'rgba(171, 50, 96, 0.6)',   # Red for 'F - Savon: OUI'
        ('F', 'NON'): 'rgba(171, 50, 96, 0.9)'    # Dark red for 'F - Savon: NON'
    }

    # Create the grouped bar chart using Plotly
    fig = go.Figure()

    # Iterate over each sex (M and F)
    for sex in age_sex_savon_counts['sexe'].unique():
        data_oui = age_sex_savon_counts[(age_sex_savon_counts['sexe'] == sex) & (age_sex_savon_counts['savon'] == 'OUI')]
        data_non = age_sex_savon_counts[(age_sex_savon_counts['sexe'] == sex) & (age_sex_savon_counts['savon'] == 'NON')]
        
        # Sort data by age
        data_oui = data_oui.sort_values(by='age')
        data_non = data_non.sort_values(by='age')
        
        # Create bar traces for 'OUI' (Yes) soap usage
        if not data_oui.empty:
            fig.add_trace(go.Bar(
                x=data_oui['age'],
                y=data_oui['percentage'],
                name=f'{sex} - Savon: OUI',
                marker_color=color_palette[(sex, 'OUI')],
                base=0,  # Start from y=0
                offsetgroup=sex,
            ))
        
        # Create bar traces for 'NON' (No) soap usage
        if not data_non.empty:
            fig.add_trace(go.Bar(
                x=data_non['age'],
                y=data_non['percentage'],
                name=f'{sex} - Savon: NON',
                marker_color=color_palette[(sex, 'NON')],
                base=0,  # Start from y=0 for "NON"
                offsetgroup=sex,
            ))

    # Update layout for better visualization
    fig.update_layout(
        barmode='stack',  # Change to 'stack' to stack the bars
        title_text=f'Distribution des patients par Âge, Genre et Lavage au savon (sur {not_null_pairs} patients IPM)',
        xaxis_title='Âge',
        yaxis_title='Pourcentage de patients',
        legend_title='Genre et Savon',
        width=1000,
        height=600,
        xaxis={'type': 'category'},
        legend=dict(
            orientation='h',
            x=0, y=1.1,
        )
    )

    # Show the plot
    st.plotly_chart(fig)

def plot_peripheral_data(df):
    
    # Select relevant columns
    peripheral_data = df[['sexe', 'age', 'lavage_savon']]

    # Drop rows where 'lavage_savon' is 'Non rempli'
    peripheral_data = peripheral_data[peripheral_data['lavage_savon'] != 'Non rempli']

    # Convert 'age' column to numeric, coerce errors to NaN
    peripheral_data['age'] = pd.to_numeric(peripheral_data['age'], errors='coerce')
    peripheral_data['lavage_savon']=peripheral_data['lavage_savon'].replace('0', 'NON')

    # Drop rows with NaN in 'age' column
    peripheral_data = peripheral_data.dropna(subset=['age'])

    # Count the number of patients
    num_patients = peripheral_data.shape[0]
    st.write(f"Nombre de patients: {num_patients}")

    # Group by age, sex, and soap, and count occurrences
    age_sex_savon_counts = peripheral_data.groupby(['age', 'sexe', 'lavage_savon']).size().reset_index(name='count')

    # Sort by age (now integers)
    age_sex_savon_counts = age_sex_savon_counts.sort_values(by='age')
    st.dataframe(age_sex_savon_counts.head())

    # Define color palette for bars
    color_palette = {
        ('M', 'OUI'): 'rgba(50, 171, 96, 0.6)',   # Green for 'M - Savon: OUI'
        ('M', 'NON'): 'rgba(50, 171, 96, 0.9)',   # Dark green for 'M - Savon: NON'
        ('F', 'OUI'): 'rgba(171, 50, 96, 0.6)',   # Red for 'F - Savon: OUI'
        ('F', 'NON'): 'rgba(171, 50, 96, 0.9)'    # Dark red for 'F - Savon: NON'
    }

    # Create the grouped bar chart using Plotly
    fig = go.Figure()

    # Iterate over each sex (M and F)
    for sex in age_sex_savon_counts['sexe'].unique():
        for savon in age_sex_savon_counts['lavage_savon'].unique():
            data = age_sex_savon_counts[(age_sex_savon_counts['sexe'] == sex) & (age_sex_savon_counts['lavage_savon'] == savon)]
            
            # Create bar traces for each sex and soap usage
            if not data.empty:
                fig.add_trace(go.Bar(
                    x=data['age'],
                    y=data['count'],
                    name=f'{sex} - Savon: {savon}',
                    marker_color=color_palette[(sex, savon)],
                    base=0,  # Start from y=0
                    offsetgroup=sex,
                ))

    # Update layout for better visualization
    fig.update_layout(
        barmode='stack',
        title_text=f'Distribution des patients par Âge, Genre et Lavage au savon (sur {num_patients} patients)',
        xaxis_title='Âge',
        yaxis_title='Nombre de patients',
        legend_title='Genre et Savon',
        width=1000,
        height=600,
        xaxis={'type': 'category'},
        legend=dict(
            orientation='h',
            x=0, y=1.1,
        )
    )

    # Show the plot
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
            plot_age_sex_savon_distribution(df)

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
                    plot_peripheral_data(df)
            elif all_ctars_selected:  
                plot_peripheral_data(df)
           



# Sidebar container with fixed width
with st.sidebar.container():
    st.image("Logo-CORAMAD.jpg", use_column_width=True, width=250, caption="FSPI Rage")