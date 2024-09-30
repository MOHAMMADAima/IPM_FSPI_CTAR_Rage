import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page title
st.set_page_config(page_title="Histogram Analysis", page_icon="⚧️")
st.title("Age et sexe des victimes.")


import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def age_sexe(df_clean):
    # Ensure 'age' column is numeric for proper sorting
    df_clean['age'] = pd.to_numeric(df_clean['age'], errors='coerce')
    df_clean=df_clean[df_clean['age']<=120]

    # Count not null pairs (age, sexe)
    not_null_pairs = df_clean[['age', 'sexe']].notnull().all(axis=1).sum()

    # Group by age and sex, and count occurrences
    age_sex_counts = df_clean.groupby(['age', 'sexe']).size().reset_index(name='count')

    # Sort by age (ensured to be numeric)
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
        width=1500,   # Adjust width of the plot (make it wider)
        height=600,   # Adjust height of the plot
        xaxis=dict(
            type='linear',  # Set x-axis to treat 'age' as numeric (linear scale)
            tickmode='linear',  # Ensure ticks are at consistent intervals
            tick0=age_sex_counts['age'].min(),  # Start the ticks at the minimum age
            dtick=1,  # Set tick interval to 1 (optional: adjust if you have many age groups)
        ),
        legend=dict(
            orientation='h',  # Horizontal legend
            x=0, y=1.1,  # Positioning of the legend
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
         # Convert 'age' column to numeric, coerce errors to NaN
        df['age'] = pd.to_numeric(df['age'], errors='coerce')
        # Drop rows with NaN in 'age' column
        df = df.dropna(subset=['age'])

        # If the selected file is the IPM dataset
        if selected_file == "CTAR_ipmdata20022024_cleaned.csv":
            df = df.drop_duplicates(subset=['ref_mordu'])
            age_sexe(df)

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
                    age_sexe(df)
            elif all_ctars_selected:  
                age_sexe(df)           

else:
    st.error("Aucun fichier n'a été téléchargé. Veuillez retourner à la page d'accueil pour télécharger un fichier.")




# Sidebar container with fixed width
with st.sidebar.container():
    st.image("Logo-CORAMAD.jpg", use_column_width=True, width=250, caption="FSPI Rage")
