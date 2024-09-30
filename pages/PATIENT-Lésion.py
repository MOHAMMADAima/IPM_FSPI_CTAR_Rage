import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.colors as pc

# Set page title
st.set_page_config(page_title="Saison Morsure", page_icon="")
st.title("Nombre de lésions par patient.")


def plot_cat1_ipm(ipm):
    
    # Get the first dataframe uploaded
    ipm=ipm.drop_duplicates(subset=['ref_mordu'])
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

  
    st.plotly_chart(fig, use_container_width=True)

def plot_cat1_peripheral(ctar):
    # Apply preprocessing
    ctar['nb_lesion'] = ctar['nb_lesion'].replace({
            '01': '1', '02': '2', '03': '3', '04': '4', '05': '5', 
            '06': '6', '07': '7', '08': '8', '09': '9', '022': '22', 
            '052': '52', '002': '2', '021': '21'
        })
    
    ctar=ctar.dropna(subset=['nb_lesion'])

        # Replace NaN values for specific rows and columns
    ctar.at[26659, 'ctar'] = 'Antsohihy'
    ctar.at[36582, 'ctar'] = 'Morondava'
    ctar.at[38479, 'ctar'] = 'Vangaindrano'
    ctar.at[42574, 'ctar'] = 'Fianarantsoa'
    ctar.at[42575, 'ctar'] = 'Fianarantsoa'

   
        # Fill NaNs with -1 and convert to int
    #ctar['nb_lesion_filled'] = ctar['nb_lesion'].fillna(-1).astype(int)

        # Calculate statistics, ignoring the marker value for NaNs
    mean_lesions = ctar[ctar['nb_lesion'] != -1]['nb_lesion'].mean()
    median_lesions = ctar[ctar['nb_lesion'] != -1]['nb_lesion'].median()
    variance_lesions = ctar[ctar['nb_lesion'] != -1]['nb_lesion'].var()

        # Count the values including NaNs
    value_counts = ctar['nb_lesion'].value_counts().sort_index()

        # Convert the index to a list of strings for x-axis labeling, converting -1 back to 'NaN'
    x_labels = [int(x) if x != -1 else 'NaN' for x in value_counts.index]

        # Create color scale based on counts
    dark_oranges = px.colors.sequential.Oranges[::-1]  # Reverse the Oranges scale to get darker shades
    color_scale = [dark_oranges[int((i) * (len(dark_oranges) - 1) / (len(value_counts) - 1))] for i in range(len(value_counts))]

        # Create the bar plot
    fig = go.Figure()

    fig.add_trace(go.Bar(
            x=(x_labels),
            y=value_counts.values,
            marker_color=color_scale,
            name='Nombre de patients'
        ))

        # Add mean and median lines
    fig.add_trace(go.Scatter(
            x=(x_labels),
            y=[mean_lesions] * len(x_labels),
            mode='lines',
            line=dict(color='red', dash='dash'),
            name=f'Moyenne: {mean_lesions:.2f}'
        ))

    fig.add_trace(go.Scatter(
            x=(x_labels),
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

    

# Main Streamlit logic
if 'dataframes' in st.session_state:
    dataframes = st.session_state['dataframes']

    # Select a file to analyze from the uploaded files
    selected_file = st.selectbox("Sélectionnez un fichier pour l'analyse", options=list(dataframes.keys()))

    # Load the selected dataframe
    if selected_file:
        df = dataframes[selected_file]

        # If the selected file is the IPM dataset
        if selected_file == "CTAR_ipmdata20022024_cleaned.csv":
            plot_cat1_ipm(df)

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
                    plot_cat1_peripheral(df)
            elif all_ctars_selected:  
                plot_cat1_peripheral(df)
           


# Sidebar container with fixed width
with st.sidebar.container():
    st.image("Logo-CORAMAD.jpg", use_column_width=True, width=250, caption="FSPI Rage")
