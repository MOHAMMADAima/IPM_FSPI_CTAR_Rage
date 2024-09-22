import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page title
st.set_page_config(page_title="Age et sexe des victimes", page_icon="📊")
st.title("Age et sexe des victimes.")

# Function to check data columns and display preview
def check_data_and_display(df, file_name):
    st.write(f"### Aperçu du fichier : {file_name}")
    st.write(df.head())  # Show the first few rows of the dataframe
    if 'age' not in df.columns or 'sexe' not in df.columns:
        st.error(f"Les colonnes 'age' ou 'sexe' ne sont pas présentes dans le fichier {file_name}.")
        return False
    return True

# Check if dataframes are available in session state
if 'dataframes' in st.session_state:
    dataframes = st.session_state['dataframes']

    # Select a file to analyze from the uploaded files
    selected_file = st.selectbox("Sélectionnez un fichier pour l'analyse", options=list(dataframes.keys()))

    # Load the selected dataframe
    if selected_file == "CTAR_ipmdata20022024_cleaned.csv":
        ipm = dataframes[selected_file]

        # Check if necessary columns are present
        if check_data_and_display(ipm, selected_file):

            # Convert 'age' column to numeric, coerce errors to NaN
            ipm['age'] = pd.to_numeric(ipm['age'], errors='coerce')

            # Drop rows with NaN in 'age' column
            ipmm = ipm.dropna(subset=['age'])

            # Count not null pairs (age, sexe)
            not_null_pairs = ipmm[['age', 'sexe']].notnull().all(axis=1).sum()

            # Group by age and sex, and count occurrences
            age_sex_counts = ipmm.groupby(['age', 'sexe']).size().reset_index(name='count')

            # Sort by age
            age_sex_counts = age_sex_counts.sort_values(by='age')

            # Create the grouped bar chart using Plotly
            fig = go.Figure()

            # Iterate over each sex (M and F)
            for sex in age_sex_counts['sexe'].unique():
                data = age_sex_counts[age_sex_counts['sexe'] == sex]
                fig.add_trace(go.Bar(
                    x=data['age'],
                    y=data['count'],
                    name=f'{sex}',  # Add 'F' or 'M' to legend name
                ))

            # Update layout for better visualization
            fig.update_layout(
                barmode='group',  # Use 'group' mode for grouped bars
                title_text=f'Distribution des patients par Âge et Genre (sur {not_null_pairs} patients IPM)',
                xaxis_title='Âge',
                yaxis_title='Nombre de patients',
                legend_title='Genre',
                width=1000,  # Adjust width of the plot (make it wider)
                height=600,  # Adjust height of the plot
                xaxis={'type': 'category'},  # Ensure x-axis treats 'age' as categorical labels
                legend=dict(
                    orientation='h',  # Horizontal legend
                    x=0, y=1.1,  # Positioning of the legend
                )
            )

            # Show the plot
            st.plotly_chart(fig)

    elif selected_file == "CTAR_peripheriquedata20022024_cleaned.csv":
        ctar = dataframes[selected_file]

        # Check if necessary columns are present
        if check_data_and_display(ctar, selected_file):

            # Convert 'age' column to numeric, coerce errors to NaN
            ctar['age'] = pd.to_numeric(ctar['age'], errors='coerce')

            # Drop rows with NaN in 'age' column
            ctarr = ctar.dropna(subset=['age'])

            # Count not null pairs (age, sexe)
            not_null_pairs = ctarr[['age', 'sexe']].notnull().all(axis=1).sum()

            # Group by age and sex, and count occurrences
            age_sex_counts = ctarr.groupby(['age', 'sexe']).size().reset_index(name='count')

            # Sort by age
            age_sex_counts = age_sex_counts.sort_values(by='age')

            # Create the grouped bar chart using Plotly
            fig = go.Figure()

            # Iterate over each sex (M and F)
            for sex in age_sex_counts['sexe'].unique():
                data = age_sex_counts[age_sex_counts['sexe'] == sex]
                fig.add_trace(go.Bar(
                    x=data['age'],
                    y=data['count'],
                    name=f'{sex}',  # Add 'F' or 'M' to legend name
                ))

            # Update layout for better visualization
            fig.update_layout(
                barmode='group',  # Use 'group' mode for grouped bars
                title_text=f'Distribution des patients par Âge et Genre (sur {not_null_pairs} patients des CTARs périphériques)',
                xaxis_title='Âge',
                yaxis_title='Nombre de patients',
                legend_title='Genre',
                width=1000,  # Adjust width of the plot (make it wider)
                height=600,  # Adjust height of the plot
                xaxis={'type': 'category'},  # Ensure x-axis treats 'age' as categorical labels
                legend=dict(
                    orientation='h',  # Horizontal legend
                    x=0, y=1.1,  # Positioning of the legend
                )
            )

            # Show the plot
            st.plotly_chart(fig)

else:
    st.error("Aucun fichier n'a été téléchargé. Veuillez retourner à la page d'accueil pour télécharger un fichier.")

# Sidebar container with fixed width
with st.sidebar.container():
    st.image("Logo-CORAMAD.jpg", use_column_width=True, width=250, caption="FSPI Rage")
