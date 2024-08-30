import streamlit as st
import pandas as pd
import plotly.graph_objects as go




# Set page title
st.set_page_config(page_title="Nombre moyen de lésions, avec variance et médiane par groupe d'âge sur les différentes parties du corps.", page_icon="📊")

# Check if dataframes are available in session state
if 'dataframes' in st.session_state:
    dataframes = st.session_state['dataframes']
    
    # Select a file to analyze from the uploaded files
    selected_file = st.selectbox("Sélectionnez un fichier pour l'analyse", options=list(dataframes.keys()))

    # Load the selected dataframe
    if selected_file:
        ipm = dataframes[selected_file]

        # Define age groups with 5-year intervals from 0 to 100, with the last group being 100+
        bins = list(range(0, 105, 5)) + [float('inf')]
        labels = [f'{i}-{i+4}' for i in bins[:-2]] + ['100+']
        
        # Categorize ages into defined bins
        age_groups = pd.cut(ipm['age'], bins=bins, labels=labels, right=False)
        
        # Ensure all lesion columns are integers
        lesion_columns = ['nbtet', 'nb_sup', 'nb_extr_s', 'nb_inf', 'nb_extr_i', 'nb_abdo', 'nb_dos', 'nb_genit']
        for col in lesion_columns:
            ipm[col] = ipm[col].dropna().astype(int)

        # Add the age group to the DataFrame
        ipm['Age Group'] = age_groups

        # Group by age group and calculate mean and median lesions for each body part
        grouped = ipm.groupby('Age Group').agg({col: ['mean', 'median', 'var'] for col in lesion_columns}).reset_index()

        # Flatten multi-index columns
        grouped.columns = ['Age Group'] + [f'{col}_{stat}' for col, stat in grouped.columns[1:]]

        # Rename columns for better readability
        grouped.rename(columns={
            'nbtet_mean': 'Tête_mean', 'nbtet_median': 'Tête_median', 'nbtet_var': 'Tête_var',
            'nb_sup_mean': 'Bras et avant-bras_mean', 'nb_sup_median': 'Bras et avant-bras_median', 'nb_sup_var': 'Bras et avant-bras_var',
            'nb_extr_s_mean': 'Main_mean', 'nb_extr_s_median': 'Main_median', 'nb_extr_s_var': 'Main_var',
            'nb_inf_mean': 'Cuisse et Jambe_mean', 'nb_inf_median': 'Cuisse et Jambe_median', 'nb_inf_var': 'Cuisse et Jambe_var',
            'nb_extr_i_mean': 'Pied_mean', 'nb_extr_i_median': 'Pied_median', 'nb_extr_i_var': 'Pied_var',
            'nb_abdo_mean': 'Abdomen_mean', 'nb_abdo_median': 'Abdomen_median', 'nb_abdo_var': 'Abdomen_var',
            'nb_dos_mean': 'Dos_mean', 'nb_dos_median': 'Dos_median', 'nb_dos_var': 'Dos_var',
            'nb_genit_mean': 'Parties génitales_mean', 'nb_genit_median': 'Parties génitales_median', 'nb_genit_var': 'Parties génitales_var'
        }, inplace=True)

        # Fill NaN values with 0
        # Convert all categorical columns to strings before filling NaNs
        for col in grouped.select_dtypes(include='category').columns:
            grouped[col] = grouped[col].astype(str)
        
        grouped.fillna(0, inplace=True)
        
        # Convert back to categorical if needed
        # (Optional, based on your use case)

        # Create a combined plot
        fig = go.Figure()

        # Add bubbles for each body part lesions
        body_parts = [
            ('Tête', 'blue'),
            ('Bras et avant-bras', 'green'),
            ('Main', 'red'),
            ('Cuisse et Jambe', 'purple'),
            ('Pied', 'orange'),
            ('Abdomen', 'brown'),
            ('Dos', 'pink'),
            ('Parties génitales', 'cyan')
        ]

        sizeref = 70 * max(grouped[f'{part}_mean'].max() for part, _ in body_parts) / (100. ** 2)

        for part, color in body_parts:
            # Add markers for mean values
            fig.add_trace(go.Scatter(
                x=grouped['Age Group'], y=grouped[f'{part}_mean'], mode='markers', name=f'{part} Moyenne',
                marker=dict(size=grouped[f'{part}_mean'] * 4, sizemode='area', sizeref=sizeref, sizemin=1, color=color),
                showlegend=True
            ))

            # Add variance lines alongside mean and median lines
            variance_val = grouped[f'{part}_var']
            fig.add_trace(go.Scatter(
                x=grouped['Age Group'], y=variance_val, mode='lines',
                line=dict(color=color, width=2, dash='dot'), name=f'{part} Variance', showlegend=True, visible='legendonly'
            ))

            median_val = grouped[f'{part}_median']
            fig.add_trace(go.Scatter(
                x=grouped['Age Group'], y=median_val, mode='lines',
                line=dict(color=color, width=2, dash='dash'), name=f'{part} Médiane', showlegend=True, visible='legendonly'
            ))

        # Update layout
        fig.update_layout(
            title="Nombre moyen de lésions, avec variance et médiane par groupe d'âge sur les différentes parties du corps",
            xaxis=dict(title="Groupe d'âge", tickangle=-45),  # Adjust tickangle for better readability
            yaxis=dict(title='Nombre de lésions '),
            legend=dict(title="Légende", orientation="v", yanchor="top", y=0.95, xanchor="right", x=1.35,
                        traceorder="normal", tracegroupgap=20),
            height=850,  # Increase figure height
            width=1000,
            margin=dict(b=250)  # Add margin at the bottom for title and legend
        )

        # Display the figure
        st.plotly_chart(fig)

else:
    st.error("Aucun fichier n'a été téléchargé. Veuillez retourner à la page d'accueil pour télécharger un fichier.")

# Sidebar container with fixed width
with st.sidebar.container():
    st.image("Logo-CORAMAD.jpg", use_column_width=True, width=250, caption="FSPI Rage")
