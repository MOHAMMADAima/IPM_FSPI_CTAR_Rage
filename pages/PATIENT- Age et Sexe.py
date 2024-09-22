import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page title
st.set_page_config(page_title="Histogram Analysis", page_icon="📊")
st.title("Age et sexe des victimes.")

# Check if dataframes are available in session state
if 'dataframes' in st.session_state:
    dataframes = st.session_state['dataframes']

    # Select a file to analyze from the uploaded files
    selected_file = st.selectbox("Sélectionnez un fichier pour l'analyse", options=list(dataframes.keys()))

    # Load the selected dataframe
    if selected_file:
        df = dataframes[selected_file]

        # Convert 'age' column to numeric, coerce errors to NaN
        df['age'] = pd.to_numeric(df['age'], errors='coerce')

        # Drop rows with NaN in 'age' column
        df_clean = df.dropna(subset=['age'])

        # If the selected file is the IPM dataset
        if selected_file == "CTAR_ipmdata20022024_cleaned.csv" and 'ref_mordu' in df_clean.columns:
            # Drop duplicates based on 'ref_mordu'
            df_clean = df_clean.drop_duplicates(subset=['ref_mordu'])

        # If the selected file is the peripheral CTAR dataset
        elif selected_file == "CTAR_peripheriquedata20022024_cleaned.csv" and 'id_ctar' in df_clean.columns:
            # Drop rows with NaN in 'id_ctar' column
            df_clean = df_clean.dropna(subset=['id_ctar'])

            # Get the unique CTARs
            unique_ctars = df_clean['id_ctar'].unique()

            # Add a "Select All" option to the multiselect
            selected_ctars = st.multiselect(
                "Sélectionnez un ou plusieurs CTARs (ou sélectionnez 'Tous')",
                options=['Tous'] + list(unique_ctars),  # Add "Tous" (All) option
                default='Tous'  # Default to selecting "Tous"
            )

            # If "Tous" is selected, use all CTARs
            if 'Tous' in selected_ctars:
                selected_ctars = unique_ctars

            # Filter the dataframe by the selected CTARs
            df_clean = df_clean[df_clean['id_ctar'].isin(selected_ctars)]

        # Count not null pairs (age, sexe)
        not_null_pairs = df_clean[['age', 'sexe']].notnull().all(axis=1).sum()

        # Group by age and sex, and count occurrences
        age_sex_counts = df_clean.groupby(['age', 'sexe']).size().reset_index(name='count')

        # Sort by age
        age_sex_counts = age_sex_counts.sort_values(by='age')

        # Create the grouped bar chart using Plotly
        fig = go.Figure()

        # Iterate over each sex ('M' for male, 'F' for female)
        for sex in age_sex_counts['sexe'].unique():
            data = age_sex_counts[age_sex_counts['sexe'] == sex]
            # Use red color for women ('F'), default color for men ('M')
            color = 'red' if sex == 'F' else None
            fig.add_trace(go.Bar(
                x=data['age'],
                y=data['count'],
                name=f'{sex}',  # Add 'F' or 'M' to legend name
                marker_color=color  # Apply red color for female bars
            ))

        # Update layout for better visualization
        fig.update_layout(
            barmode='group',  # Use 'group' mode for grouped bars
            title_text=f'Distribution des patients par Âge et Genre (sur {not_null_pairs} patients)',
            xaxis_title='Âge',
            yaxis_title='Nombre de patients',
            legend_title='Genre',
            width=1000,   # Adjust width of the plot (make it wider)
            height=600,   # Adjust height of the plot
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
