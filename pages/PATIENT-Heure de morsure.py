import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page title
st.set_page_config(page_title="Histogram Analysis", page_icon="📊")
st.title("Heure de morsure des patients.")

# Check if dataframes are available in session state
if 'dataframes' in st.session_state:
    dataframes = st.session_state['dataframes']

    # Select a file to analyze from the uploaded files
    selected_file = st.selectbox("Sélectionnez un fichier pour l'analyse", options=list(dataframes.keys()))

    # Load the selected dataframe
    if selected_file:
        df = dataframes[selected_file]

        # If the selected file is the IPM dataset
        if selected_file == "CTAR_ipmdata20022024_cleaned.csv" and 'ref_mordu' in df.columns:
            st.warning("Donnée de l'heure de morsure non disponible pour CTAR IPM.")

        # If the selected file is the peripheral CTAR dataset
        elif selected_file == "CTAR_peripheriquedata20022024_cleaned.csv" and 'id_ctar' in df.columns:
            # Drop rows with NaN in 'id_ctar' column
            df = df.dropna(subset=['id_ctar'])
            df = df[~df['heure_du_contact_cleaned'].astype(str).str.contains('00:00', regex=True)]

            

            # Get the unique CTARs
            unique_ctars = df['id_ctar'].unique()

            # Add a "Select All" option to the multiselect
            selected_ctars = st.multiselect(
                "Sélectionnez un ou plusieurs CTARs (ou sélectionnez 'Tous')",
                options=['Tous'] + list(unique_ctars),  # Add "Tous" (All) option
                default='Tous les CTAR'  # Default to selecting "Tous"
            )

            # If "Tous" is selected, use all CTARs
            if 'Tous' in selected_ctars:
                selected_ctars = unique_ctars

            # Filter the dataframe by the selected CTARs
            df = df[df['id_ctar'].isin(selected_ctars)]

        # Heure de morsure CTAR périphériques

        # Extract hours and minutes for plotting
            df[['Hour', 'Minute']] = df['heure_du_contact_cleaned'].str.split(':', expand=True)
        # Handle NaN values before conversion
            df['Hour'] = pd.to_numeric(df['Hour'], errors='coerce').fillna(0).astype(int)
            df['Minute'] = pd.to_numeric(df['Minute'], errors='coerce').fillna(0).astype(int)

        # Combine hours and minutes into a single time string for precise plotting
            df['Time'] = df['heure_du_contact_cleaned'].fillna('00:00')

        # Group by time and sex to count occurrences
            hourly_sex_counts = df.groupby(['Hour', 'sexe']).size().reset_index(name='count')

        # Create a scatter plot with lines for each gender
            fig = go.Figure()

        # Define color scales for male and female
            male_color = 'blue'
            female_color = 'pink'

        # Add traces for each gender
            for sex, color in [('M', male_color), ('F', female_color)]:
                df_sex = hourly_sex_counts[hourly_sex_counts['sexe'] == sex]

                fig.add_trace(go.Scatter(
                    x=df_sex['Hour'],
                    y=df_sex['count'],
                    mode='lines+markers',
                    name='Homme' if sex == 'M' else 'Femme',
                    marker=dict(size=8, color=color),
                    line=dict(width=2)
                ))

            # Update layout
            fig.update_layout(
                title='Heure de morsure par sexe',
                xaxis=dict(title='Heure', tickvals=df_sex['Hour']),
                yaxis=dict(title='Nombre de morsures'),
                legend_title='Sexe'
        )


            # Update layout with proper labels
            fig.update_layout(
                title='Heure de morsure par sexe pour les patients des CTARs périphériques',
                xaxis=dict(
                    title='Heures',
                    tickvals=df_sex['Hour'],  # Ensure correct x-axis ticks
                    tickangle=0  # Optional: Adjust angle for better readability
                ),
                yaxis=dict(title='Nombre de morsures'),
                legend_title='Sexe'
            )



                # Show the plot
            st.plotly_chart(fig)

else:
    st.error("Aucun fichier n'a été téléchargé. Veuillez retourner à la page d'accueil pour télécharger un fichier.")

# Sidebar container with fixed width
with st.sidebar.container():
    st.image("Logo-CORAMAD.jpg", use_column_width=True, width=250, caption="FSPI Rage")
