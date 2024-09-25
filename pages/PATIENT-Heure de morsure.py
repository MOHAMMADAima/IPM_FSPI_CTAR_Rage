import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page title
st.set_page_config(page_title="Histogram Analysis", page_icon="📊")
st.title("Heure de morsure des patients.")


def plot_hourly_sex_counts(df, selected_ctars):
    """Plots the hourly count of bites per gender."""
    
    # If "Tous les CTAR" is selected, use all CTARs
    if 'Tous les CTAR' in selected_ctars:
        selected_ctars = df['id_ctar'].unique()
    
    # Filter the dataframe by the selected CTARs
    df_filtered = df[df['id_ctar'].isin(selected_ctars)]

    if df_filtered.empty:
        st.warning("Veuillez selectionnez au moins un CTAR.")
        return

    # Extract hours and minutes for plotting
    df_filtered[['Hour', 'Minute']] = df_filtered['heure_du_contact_cleaned'].str.split(':', expand=True)
    
    # Handle NaN values before conversion
    df_filtered['Hour'] = pd.to_numeric(df_filtered['Hour'], errors='coerce').astype(int)
    df_filtered['Minute'] = pd.to_numeric(df_filtered['Minute'], errors='coerce').fillna(0).astype(int)

    # Group by time and sex to count occurrences
    hourly_sex_counts = df_filtered.groupby(['Hour', 'sexe']).size().reset_index(name='count')

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
        title='Heure de morsure par sexe pour les patients des CTARs périphériques',
        xaxis=dict(
            title='Heures',
            tickvals=hourly_sex_counts['Hour'].unique(),  # Ensure correct x-axis ticks
            tickangle=0  # Optional: Adjust angle for better readability
        ),
        yaxis=dict(title='Nombre de morsures'),
        legend_title='Sexe'
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
        if selected_file == "CTAR_ipmdata20022024_cleaned.csv" and 'ref_mordu' in df.columns:
            st.warning("Donnée de l'heure de morsure non disponible pour CTAR IPM.")

        # If the selected file is the peripheral CTAR dataset
        elif selected_file == "CTAR_peripheriquedata20022024_cleaned.csv" and 'id_ctar' in df.columns:
            # Drop rows with NaN in 'id_ctar' column
            df = df.dropna(subset=['id_ctar'])

            # Drop rows where 'heure_du_contact_cleaned' contains '00:00' (midnight)
            df = df[~df['heure_du_contact_cleaned'].astype(str).str.contains('00:00')]

            # Get the unique CTARs
            unique_ctars = df['id_ctar'].unique()

            # Add a "Select All" option to the multiselect
            selected_ctars = st.multiselect(
                "Sélectionnez un ou plusieurs CTARs (ou sélectionnez 'Tous les CTAR')",
                options=['Tous les CTAR'] + list(unique_ctars),  # Add "Tous" (All) option
                default='Tous les CTAR'  # Default to selecting "Tous"
            )

            # Show a warning if no CTAR is selected
            if not selected_ctars:
                st.warning("Veuillez sélectionner au moins un CTAR pour afficher l'analyse.")
            else:
                # Call the plotting function
                plot_hourly_sex_counts(df, selected_ctars)

else:
    st.error("Aucun fichier n'a été téléchargé. Veuillez retourner à la page d'accueil pour télécharger un fichier.")

# Sidebar container with fixed width
with st.sidebar.container():
    st.image("Logo-CORAMAD.jpg", use_column_width=True, width=250, caption="FSPI Rage")
