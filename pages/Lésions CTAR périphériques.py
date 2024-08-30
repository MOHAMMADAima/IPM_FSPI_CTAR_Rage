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

        # Fill NaNs with -1 and convert to int
        ctar['nb_lesion_filled'] = ctar['nb_lesion'].fillna(-1).astype(int)

        # Calculate statistics, ignoring the marker value for NaNs
        mean_lesions = ctar[ctar['nb_lesion_filled'] != -1]['nb_lesion_filled'].mean()
        median_lesions = ctar[ctar['nb_lesion_filled'] != -1]['nb_lesion_filled'].median()
        variance_lesions = ctar[ctar['nb_lesion_filled'] != -1]['nb_lesion_filled'].var()

        # Count the values including NaNs
        value_counts = ctar['nb_lesion_filled'].value_counts().sort_index()

        # Convert the index to a list of strings for x-axis labeling, converting -1 back to 'NaN'
        x_labels = [str(x) if x != -1 else 'NaN' for x in value_counts.index]

        # Create color scale based on counts
        dark_oranges = px.colors.sequential.Oranges[::-1]  # Reverse the Oranges scale to get darker shades
        color_scale = [dark_oranges[int((i) * (len(dark_oranges) - 1) / (len(value_counts) - 1))] for i in range(len(value_counts))]

        # Create the bar plot
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=x_labels,
            y=value_counts.values,
            marker_color=color_scale,
            name='Nombre de patients'
        ))

        # Add mean and median lines
        fig.add_trace(go.Scatter(
            x=x_labels,
            y=[mean_lesions] * len(x_labels),
            mode='lines',
            line=dict(color='red', dash='dash'),
            name=f'Moyenne: {mean_lesions:.2f}'
        ))

        fig.add_trace(go.Scatter(
            x=x_labels,
            y=[median_lesions] * len(x_labels),
            mode='lines',
            line=dict(color='green', dash='solid'),
            name=f'Médiane: {median_lesions:.2f}'
        ))

        # Update layout
        fig.update_layout(
            title='Distribution du nombre de lésions des patients des CTAR périf',
            xaxis_title='Nombre de lésions',
            yaxis_title='Nombre de patients',
            xaxis=dict(tickmode='array', tickvals=x_labels, ticktext=x_labels),
            template='plotly_white'
        )

        # Add annotations for mean, median, and variance
        fig.add_annotation(
            x=len(x_labels) - 1,
            y=max(value_counts.values),
            text=f'Variance: {variance_lesions:.2f}',
            showarrow=False,
            yshift=10,
            xshift=-10,
            font=dict(color='black', size=12)
        )

        # Streamlit App
        st.title('Analyse des lésions des patients CTAR')
        st.plotly_chart(fig, use_container_width=True)

        # Display statistics
        st.subheader('Statistiques:')
        st.write(f'Moyenne des lésions: {mean_lesions:.2f}')
        st.write(f'Médiane des lésions: {median_lesions:.2f}')
        st.write(f'Variance des lésions: {variance_lesions:.2f}')

else:
    st.warning("Veuillez d'abord télécharger les fichiers CSV sur la page d'accueil.")
