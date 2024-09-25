import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page title
st.set_page_config(page_title="Histogram Analysis", page_icon="📊")
st.title("Distribution des patients par Âge, Genre et Lavage au savon (IPM Dataset)")


def plot_age_sex_savon_distribution(ipm):
    """Plots the age, sex, and soap usage distribution in the IPM dataset."""
    
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
                base=0,
                offsetgroup=sex,
            ))
        
        # Create bar traces for 'NON' (No) soap usage
        if not data_non.empty:
            fig.add_trace(go.Bar(
                x=data_non['age'],
                y=data_non['percentage'],
                name=f'{sex} - Savon: NON',
                marker_color=color_palette[(sex, 'NON')],
                base=data_oui['percentage'] if not data_oui.empty else 0,
                offsetgroup=sex,
            ))

    # Update layout for better visualization
    fig.update_layout(
        barmode='relative',
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
            st.info("Chargement des données IPM...")
            # Call the IPM plot function
            plot_age_sex_savon_distribution(df)

        # If the selected file is the peripheral CTAR dataset
        elif selected_file == "CTAR_peripheriquedata20022024_cleaned.csv":
            st.warning("Données pour CTAR Périphérique. Analyse IPM non disponible pour ce fichier.")

else:
    st.error("Aucun fichier n'a été téléchargé. Veuillez retourner à la page d'accueil pour télécharger un fichier.")

# Sidebar container with fixed width
with st.sidebar.container():
    st.image("Logo-CORAMAD.jpg", use_column_width=True, width=250, caption="FSPI Rage")
