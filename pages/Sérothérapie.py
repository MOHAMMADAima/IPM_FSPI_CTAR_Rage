import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Set Streamlit page configuration
st.set_page_config(page_title="Analyse de la Dose de Sérothérapie", page_icon="💉", layout="wide")

st.title("Analyse de la Dose de Sérothérapie par Groupe d'Âge et Catégorie")

# Check if dataframes are available in session state
if 'dataframes' in st.session_state:
    dataframes = st.session_state['dataframes']

    # Select a file to analyze from the uploaded files
    selected_file = st.selectbox("Sélectionnez un fichier pour l'analyse", options=list(dataframes.keys()))

    # Load the selected dataframe
    if selected_file:
        df = dataframes[selected_file]

        # gardzr que serotherapie décision a été faite
        df=df.dropna(['serother'])

        # Define age bins and labels with specific bins for 90-99 and 100+
        age_bins = [0, 18, 30, 40, 50, 60, 70, 80, 90, 100, float('inf')]
        age_labels = ['0-17', '18-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-99', '100+']

        # Create age_bin column
        df['age_bin'] = pd.cut(df['age'], bins=age_bins, labels=age_labels, right=False)

        # Calculate dose_ML as 0.2 times poids
        df['dose_ML'] = round(0.2 * df['poids'], 2)

        # Aggregate data to calculate min and max dose_ML for each serother and age_bin
        df_agg_range = df.groupby(['serother', 'age_bin'], group_keys=False).agg({
            'dose_ML': ['min', 'max'],
            'poids': 'count',
            'categorie': lambda x: x.dropna().value_counts(normalize=True).to_dict() if x.notnull().any() else {}
        }).reset_index()

        # Flatten columns for ease of use in sunburst plot
        df_agg_range.columns = ['serother', 'age_bin', 'dose_min', 'dose_max', 'count', 'categorie']

        # Create a single layer sunburst plot with concatenated dose_min and dose_max
        df_agg_range['dose_range'] = df_agg_range.apply(lambda x: f"[{x['dose_min']} mL, {x['dose_max']} mL]", axis=1)

        # Convert categorie column to string for sunburst plotting
        df_agg_range['categorie_str'] = df_agg_range['categorie'].apply(lambda x: ', '.join([f"{k}: {v*100:.2f}%" for k, v in x.items()]) if isinstance(x, dict) else '')

        # Create sunburst plot for count of patients, age range, dose range, and categorie proportion
        fig = px.sunburst(
            df_agg_range,
            path=['serother', 'age_bin', 'dose_range', 'categorie_str'],
            values='count',  # Use 'count' to define the levels of the sunburst
            title="Proportion de patients venus au CTAR IPM pour une sérothérapie",
            labels={'serother': 'Sérothérapie', 'age_bin': 'Groupe d\'âge', 'dose_range': 'Dose Range', 'categorie_str': 'Catégories', 'count': 'Nombre patients'},
            branchvalues='total'  # Maintain labels for all layers
        )

        # Update layout with color settings and title
        fig.update_layout(
            margin=dict(t=50, l=0, r=0, b=0),
            sunburstcolorway=["#636efa", "#ef553b"],
            title="Proportion de patients venus au CTAR IPM pour une sérothérapie",
        )

        # Display the figure
        st.plotly_chart(fig)

else:
    st.error("Aucun fichier n'a été téléchargé. Veuillez retourner à la page d'accueil pour télécharger un fichier.")

# Sidebar container with fixed width
with st.sidebar.container():
    st.image("Logo-CORAMAD.jpg", use_column_width=True, width=250, caption="FSPI Rage")
