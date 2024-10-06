import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Titre page
st.set_page_config(page_title="Heure de morsure", page_icon="🕒")
st.title("Heure de morsure des patients.")


def plot_hourly_sex_counts(df, selected_ctars): 

    # If "Tous les CTAR" is selected, use all CTARs
    if 'Tous les CTAR' in selected_ctars:
        selected_ctars = df['id_ctar'].unique()
    
    # Filter the dataframe by the selected CTARs
    df_filtered = df[df['id_ctar'].isin(selected_ctars)]

    if df_filtered.empty:
        st.warning("Aucune donnée disponible pour les CTARs sélectionnés.")
        return

    # Drop rows where 'heure_du_contact_cleaned' contains '00:00' (midnight)
    df_filtered = df_filtered[~df_filtered['heure_du_contact_cleaned'].astype(str).str.contains('00:00')]
    # Extract hours and minutes for plotting
    df_filtered[['Hour', 'Minute']] = df_filtered['heure_du_contact_cleaned'].str.split(':', expand=True)
    
    # Handle NaN values before conversion
    df_filtered = df_filtered.dropna(subset=['Hour'])
    df_filtered['Minute'] = pd.to_numeric(df_filtered['Minute'], errors='coerce').fillna(0).astype(int)

    # Group by time and sex to count occurrences
    hourly_sex_counts = df_filtered.groupby(['Hour', 'sexe']).size().reset_index(name='count')

    fig = go.Figure()

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

    fig.update_layout(
        title=f'Heure de morsure par sexe pour {len(df_filtered)} patient(s) des CTARs périphériques.',
        xaxis=dict(
            title='Heures',
            tickvals=hourly_sex_counts['Hour'].unique(), 
            tickangle=0 
        ),
        yaxis=dict(title='Nombre de morsures'),
        legend_title='Sexe'
    )
    st.plotly_chart(fig)


def plot_hourly_species_counts(df, selected_ctars):
    
    # If "Tous les CTAR" is selected, use all CTARs
    if 'Tous les CTAR' in selected_ctars:
        selected_ctars = df['id_ctar'].unique()
    
    # Filter the dataframe by the selected CTARs
    df_filtered = df[df['id_ctar'].isin(selected_ctars)]

    # Drop rows where 'heure_du_contact_cleaned' contains '00:00' (midnight)
    df_filtered = df_filtered[~df_filtered['heure_du_contact_cleaned'].astype(str).str.contains('00:00')]

    if df_filtered.empty:
        st.warning("Aucune donnée disponible pour les CTARs sélectionnés.")
        return

    # Extract hours and minutes for plotting
    df_filtered[['Hour', 'Minute']] = df_filtered['heure_du_contact_cleaned'].str.split(':', expand=True)
    
    # Handle NaN values before conversion
    df_filtered = df_filtered.dropna(subset=['Hour'])
    df_filtered['Minute'] = pd.to_numeric(df_filtered['Minute'], errors='coerce').fillna(0).astype(int)

    # Group by time and species to count occurrences
    hourly_species_counts = df_filtered.groupby(['Hour', 'espece']).size().reset_index(name='count')

    fig = go.Figure()

    colors = {
        'Chien': 'brown',
        'Chat': 'orange',
        'Autre': 'green'  
    }

    for species, color in colors.items():
        df_species = hourly_species_counts[hourly_species_counts['espece'] == species]

        fig.add_trace(go.Scatter(
            x=df_species['Hour'],
            y=df_species['count'],
            mode='lines+markers',
            name=species,
            marker=dict(size=8, color=color),
            line=dict(width=2)
        ))

    fig.update_layout(
        title=f'Heure de morsure par espèce pour {len(df_filtered)} patient(s) des CTARs périphériques.',
        xaxis=dict(
            title='Heures',
            tickvals=sorted(hourly_species_counts['Hour'].unique()),  
            tickangle=0  
        ),
        yaxis=dict(title='Nombre de morsures'),
        legend_title='Espèce'
    )

    st.plotly_chart(fig)


# Main 
if 'dataframes' in st.session_state:
    dataframes = st.session_state['dataframes']

    selected_file = st.selectbox("Sélectionnez un fichier pour l'analyse", options=list(dataframes.keys()))

    if selected_file:
        df = dataframes[selected_file]

        # BDD CTAR IPM
        if selected_file == "CTAR_ipmdata20022024_cleaned.csv":
            st.warning("Donnée de l'heure de morsure non disponible pour CTAR IPM.")

        # BDD CTAR périphériques
        elif selected_file == "CTAR_peripheriquedata20022024_cleaned.csv":
            #  Ne pas comptabiliser les lignes sans ID 'id_ctar' = CTAR périphériques inconnues 
            df = df.dropna(subset=['id_ctar'])

            # Liste des CTARs périphériques pour leur sélection
            unique_ctars = df['id_ctar'].unique()

            # Analyse de l'ensemble des CTAR périphériques
            all_ctars_selected = st.checkbox("Sélectionnez tous les CTARs")

            if not all_ctars_selected:
                selected_ctars = st.multiselect(
                    "Sélectionnez un ou plusieurs CTARs",
                    options=list(unique_ctars) )
            else:
                selected_ctars = ['Tous les CTAR']

            if not selected_ctars and not all_ctars_selected:
                st.warning("Veuillez sélectionner au moins un CTAR pour afficher l'analyse.")
            else:
                plot_hourly_sex_counts(df, selected_ctars)

                plot_hourly_species_counts(df, selected_ctars)
        else:
            st.warning('Veuillez sélectionner un fichier entre "CTAR_peripheriquedata20022024_cleaned.csv" et "CTAR_ipmdata20022024_cleaned.csv".')        
  
else:
    st.error("Aucun fichier n'a été téléchargé. Veuillez retourner à la page d'accueil pour télécharger un fichier.")

# Sidebar de la page
with st.sidebar.container():
    st.image("Logo-CORAMAD.jpg", use_column_width=True, width=250, caption="FSPI Rage")
