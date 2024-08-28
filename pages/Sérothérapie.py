import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Set Streamlit page configuration
st.set_page_config(page_title="Analyse de Sérothérapie", page_icon="💉", layout="wide")

st.title("Analyse de la Dose de Sérothérapie par Groupe d'Âge et Catégorie")

# Check if dataframes are available in session state
if 'dataframes' in st.session_state:
    dataframes = st.session_state['dataframes']

    # Select a file to analyze from the uploaded files
    selected_file = st.selectbox("Sélectionnez un fichier pour l'analyse", options=list(dataframes.keys()))

    # Load the selected dataframe
    if selected_file:
        df = dataframes[selected_file]

        # Define age bins and labels with specific bins for 90-99 and 100+
        age_bins = [0, 18, 30, 40, 50, 60, 70, 80, 90, 100, float('inf')]
        age_labels = ['0-17', '18-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-99', '100+']

        # Create age_bin column
        df['age_bin'] = pd.cut(df['age'], bins=age_bins, labels=age_labels, right=False)

        # Calculate dose_ML as 0.2 times poids
        df['dose_ML'] = round(0.2 * df['poids'], 2)

        # Create dose_bin column if it does not exist or overwrite if it does
        df['dose_bin'] = pd.cut(df['dose_ML'], bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, float('inf')], right=False)

        # Aggregate data to calculate min and max dose_ML for each serother, age_bin, dose_bin, and categorie
        df_agg_range = df.groupby(['serother', 'age_bin', 'dose_bin', 'categorie'], group_keys=False).agg({
            'dose_ML': ['min', 'max'],
            'poids': 'count'
        }).reset_index()

        # Flatten columns for ease of use
        df_agg_range.columns = ['serother', 'age_bin', 'dose_bin', 'categorie', 'dose_min', 'dose_max', 'count']

        # Create dose range column
        df_agg_range['dose_range'] = df_agg_range.apply(lambda x: f"[{x['dose_min']} mL, {x['dose_max']} mL]", axis=1)

        # Aggregate data to get category proportions for each serother, age_bin, and dose_bin
        df_category_prop = df.groupby(['serother', 'age_bin', 'dose_bin', 'categorie']).size().groupby(level=[0,1,2]).apply(lambda x: x / x.sum()).reset_index(name='proportion')

        # Pivot to make 'categorie' columns
        df_category_prop_pivot = df_category_prop.pivot_table(index=['serother', 'age_bin', 'dose_bin'], columns='categorie', values='proportion', fill_value=0).reset_index()

        # Merge aggregated range with category proportions
        df_agg_range = pd.merge(df_agg_range, df_category_prop_pivot, on=['serother', 'age_bin', 'dose_bin'])

        # Convert category proportions to string format
        df_agg_range['categorie_str'] = df_agg_range.apply(lambda x: ', '.join([f"{cat}: {x[cat]*100:.1f}%" for cat in ['N', 'T', 'R']]), axis=1)

        # Create Sunburst plot
        fig = px.sunburst(
            df_agg_range,
            path=['serother', 'age_bin', 'dose_range', 'categorie'],
            values='count',
            title="Proportion de patients venus au CTAR IPM pour une sérothérapie",
            labels={'serother': 'Sero', 'age_bin': 'Age Group', 'dose_range': 'Dose Range', 'categorie': 'Category', 'count': 'Nombre patients'},
            branchvalues='total'
        )

        # Update layout with color settings, title, and increased font size
        fig.update_layout(
            margin=dict(t=50, l=0, r=0, b=0),
            sunburstcolorway=["#636efa", "#ef553b", "#00cc96"],  # Add more colors if needed
            title="Proportion de patients venus au CTAR IPM pour une sérothérapie",
            height=800,  # Adjust the height of the figure
            width=800,   # Adjust the width of the figure
            font=dict(size=16)  # Increase the font size for labels
        )

        # Customize hovertemplate to show relevant information
        fig.update_traces(
            hovertemplate="<br>".join([
                "Nombre de patients: %{value}",
                "Dose Range: %{customdata[0]}",
                "Categories: %{customdata[1]}"
            ]),
            customdata=df_agg_range[['dose_range', 'categorie_str']].values
        )

        # Display the figure
        st.plotly_chart(fig)

else:
    st.error("Aucun fichier n'a été téléchargé. Veuillez retourner à la page d'accueil pour télécharger un fichier.")
