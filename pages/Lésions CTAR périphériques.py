import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Check if dataframes are available in session state
if 'dataframes' in st.session_state:
    dataframes = st.session_state['dataframes']
    
    # Select a file to analyze from the uploaded files
    selected_file = st.selectbox("Sélectionnez un fichier pour l'analyse", options=list(dataframes.keys()))

    # Load the selected dataframe
    if selected_file:
        ctar = dataframes[selected_file]

        # Apply preprocessing
        ctar['nb_lesion'] = ctar['nb_lesion'].replace({
            '01': '1', '02': '2', '03': '3', '04': '4', '05': '5', 
            '06': '6', '07': '7', '08': '8', '09': '9', '022': '22', 
            '052': '52', '002': '2', '021': '21'
        })

        # Replace NaN values for specific rows and columns
        ctar.at[26659, 'ctar'] = 'Antsohihy'
        ctar.at[36582, 'ctar'] = 'Morondava'
        ctar.at[38479, 'ctar'] = 'Vangaindrano'
        ctar.at[42574, 'ctar'] = 'Fianarantsoa'
        ctar.at[42575, 'ctar'] = 'Fianarantsoa'

        non_rempli_cols = ['lavage_savon', 'sat', 'vat', 'vaccin_antirabique', 'antibiotique']
        non_rempli_rows = [76734, 76902, 76994]
        for col in non_rempli_cols:
            for row in non_rempli_rows:
                ctar.at[row, col] = 'Non rempli'

        # Process 'nb_lesion' column
        ctar['nb_lesion_filled'] = ctar['nb_lesion'].fillna(-1).astype(int)

        # Calculate statistics for lesions
        mean_lesions = ctar[ctar['nb_lesion_filled'] != -1]['nb_lesion_filled'].mean()
        median_lesions = ctar[ctar['nb_lesion_filled'] != -1]['nb_lesion_filled'].median()
        variance_lesions = ctar[ctar['nb_lesion_filled'] != -1]['nb_lesion_filled'].var()

        # Count the values for lesions
        lesion_value_counts = ctar['nb_lesion_filled'].value_counts().sort_index()

        # Create color scale based on counts for the bar chart
        dark_oranges = px.colors.sequential.Oranges[::-1]
        color_scale = [dark_oranges[int((i) * (len(dark_oranges) - 1) / (len(lesion_value_counts) - 1))] for i in range(len(lesion_value_counts))]

        # Create the bar plot for lesion count
        fig_lesion = go.Figure()

        fig_lesion.add_trace(go.Bar(
            x=[str(x) if x != -1 else 'NaN' for x in lesion_value_counts.index],
            y=lesion_value_counts.values,
            marker_color=color_scale,
            name='Nombre de patients'
        ))

        fig_lesion.add_trace(go.Scatter(
            x=[str(x) if x != -1 else 'NaN' for x in lesion_value_counts.index],
            y=[mean_lesions] * len(lesion_value_counts),
            mode='lines',
            line=dict(color='red', dash='dash'),
            name=f'Moyenne: {mean_lesions:.2f}'
        ))

        fig_lesion.add_trace(go.Scatter(
            x=[str(x) if x != -1 else 'NaN' for x in lesion_value_counts.index],
            y=[median_lesions] * len(lesion_value_counts),
            mode='lines',
            line=dict(color='green', dash='solid'),
            name=f'Médiane: {median_lesions:.2f}'
        ))

        fig_lesion.update_layout(
            title='Distribution du nombre de lésions des patients des CTAR périf',
            xaxis_title='Nombre de lésions',
            yaxis_title='Nombre de patients',
            xaxis=dict(tickmode='array', tickvals=[str(x) if x != -1 else 'NaN' for x in lesion_value_counts.index], ticktext=[str(x) if x != -1 else 'NaN' for x in lesion_value_counts.index]),
            template='plotly_white'
        )

        fig_lesion.add_annotation(
            x=len(lesion_value_counts) - 1,
            y=max(lesion_value_counts.values),
            text=f'Variance: {variance_lesions:.2f}',
            showarrow=False,
            yshift=10,
            xshift=-10,
            font=dict(color='black', size=12)
        )

        # Process age data
        ctar['age'] = ctar['age'].fillna(-1).astype(int)
        age_value_counts = ctar['age'].value_counts().sort_index()
        top_10_age_value_counts = age_value_counts.nlargest(10)
        top_10_age_labels = [str(x) if x != -1 else 'NaN' for x in top_10_age_value_counts.index]

        # Create the pie chart for age distribution
        fig_age = px.pie(
            values=top_10_age_value_counts.values,
            names=top_10_age_labels,
            color=top_10_age_labels,
            color_discrete_sequence=px.colors.sequential.Oranges[::-1]
        )

        fig_age.update_layout(
            title='Top 10 Répartition de l\'âge parmi les patients',
            template='plotly_white',
            legend_title_text='Âge'
        )

        # Streamlit App
        st.title('Analyse des lésions et âges des patients CTAR')
        
        st.subheader('Distribution du nombre de lésions')
        st.plotly_chart(fig_lesion, use_container_width=True)
        
        st.subheader('Top 10 Répartition de l\'âge parmi les patients')
        st.plotly_chart(fig_age, use_container_width=True)

        # Display statistics for lesions
        st.subheader('Statistiques pour les lésions:')
        st.write(f'Moyenne des lésions: {mean_lesions:.2f}')
        st.write(f'Médiane des lésions: {median_lesions:.2f}')
        st.write(f'Variance des lésions: {variance_lesions:.2f}')

else:
    st.warning("Veuillez d'abord télécharger les fichiers CSV sur la page d'accueil.")
