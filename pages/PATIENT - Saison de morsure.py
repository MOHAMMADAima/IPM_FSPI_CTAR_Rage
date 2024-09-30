import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.colors as pc

# Set page title
st.set_page_config(page_title="Saison Morsure", page_icon="☀️")
st.title("Affluence des patients par saison.")


 # Define a function to map dates to seasons
def get_season(date):
        if pd.isnull(date):
            return None
        if pd.Timestamp(year=date.year, month=9, day=15) <= date < pd.Timestamp(year=date.year, month=12, day=15):
            return 'Lohataona (été)'
        elif pd.Timestamp(year=date.year, month=12, day=15) <= date < pd.Timestamp(year=date.year+1, month=3, day=15):
            return 'Fahavratra (pluie)'
        elif pd.Timestamp(year=date.year, month=3, day=15) <= date < pd.Timestamp(year=date.year, month=6, day=15):
            return 'Fararano (automne)'
        else:
            return 'Ritinina (hiver)'

def plot_saison_morsure_ipm(ipm):
    
    # Get the first dataframe uploaded
    ipm=ipm.drop_duplicates(subset=['ref_mordu'])
    ipm['dat_consu'] = pd.to_datetime(ipm['dat_consu'], format='%d/%m/%Y', errors='coerce')

    # Apply the function to create the 'season' column
    ipm['season'] = ipm['dat_consu'].apply(get_season)

    # Group by month, year, and sexe to count the number of patients for each sex
    monthly_sex_counts = ipm.groupby(['mois', 'Annee', 'sexe']).size().reset_index(name='count')

    # Define the month order for consistent x-axis labeling (January to December)
    months = list(range(1, 13))  # January to December
    month_names = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
        'Sep', 'Oct', 'Nov', 'Dec'
    ]

    # Determine the min and max count values for setting the y-axis range
    min_count = monthly_sex_counts['count'].min()
    max_count = monthly_sex_counts['count'].max()
    range_margin = (max_count - min_count) * 0.2  # Add some margin around the lines

    # Create a scatter plot with lines for each year and gender using Plotly
    fig = go.Figure()

    # Define color scales for male and female
    male_colors = pc.sequential.Blues[::-1]  # Shades of blue
    female_colors = pc.sequential.Reds[::-1]  # Shades of pink

    # Sort years in descending order to show recent years first
    years_sorted = sorted(monthly_sex_counts['Annee'].unique(), reverse=True)

    # Add scatter plot points for each year and sex (Male and Female)
    sexes = ['M', 'F']
    for i, year in enumerate(years_sorted):
        for j, sex in enumerate(sexes):
            df_year_sex = monthly_sex_counts[(monthly_sex_counts['Annee'] == year) & (monthly_sex_counts['sexe'] == sex)]
            df_year_sex = df_year_sex.set_index('mois').reindex(months).reset_index()
            df_year_sex['count'] = df_year_sex['count'].fillna(0)
            
            # Determine color based on gender
            if sex == 'M':
                color = male_colors[i % len(male_colors)]
            else:
                color = female_colors[i % len(female_colors)]

            fig.add_trace(go.Scatter(
                x=df_year_sex['mois'],
                y=df_year_sex['count'],
                mode='lines+markers',
                name=f"{int(year)} - {'Homme' if sex == 'M' else 'Femme'}",  # Ensure year and sex are displayed
                marker=dict(size=8, color=color),  # Use color from the gradient
                line=dict(width=2),
                visible="legendonly" if year < 2021 else True  # Show only the first 4 years initially
            ))

    # Define background colors for each season and corresponding text
    season_backgrounds = {
        'Fahavratra (pluie)': (12, 3, 'rgba(186, 225, 255, 0.3)', 'rgb(186, 225, 255)'),
        'Fararano (automne)': (3.5, 6, 'rgba(255, 186, 186, 0.3)', 'rgb(255, 186, 186)'),
        'Ritinina (hiver)': (6.5, 9, 'rgba(186, 255, 201, 0.3)', 'rgb(186, 255, 201)'),
        'Lohataona (été)': (9.5, 11.5, 'rgba(255, 223, 186, 0.3)', 'rgb(255, 223, 186)')
    }

    shapes = []
    annotations = []

    # Add season backgrounds to match the x-axis labels
    for season, (start_month, end_month, color, text_color) in season_backgrounds.items():
        if end_month < start_month:
            shapes.append(dict(
                type='rect',
                x0=start_month - 1,
                x1=11,  # Extend to December
                y0=min_count - range_margin,
                y1=max_count + range_margin,
                fillcolor=color,
                line=dict(width=0),
                layer='below'
            ))
            shapes.append(dict(
                type='rect',
                x0=1 - 1,  # Start from January
                x1=end_month - 0.5,
                y0=min_count - range_margin,
                y1=max_count + range_margin,
                fillcolor=color,
                line=dict(width=0),
                layer='below'
            ))
        else:
            shapes.append(dict(
                type='rect',
                x0=start_month - 1,
                x1=end_month - 0.5,
                y0=min_count - range_margin,
                y1=max_count + range_margin,
                fillcolor=color,
                line=dict(width=0),
                layer='below'
            ))

        # Add season text inside the colored rectangles
        annotations.append(dict(
            x=(start_month) / 10 if end_month < start_month else (start_month + end_month - 1) / 2,
            y=min_count - range_margin,  # Position text inside the rectangle
            text=season,
            showarrow=False,
            font=dict(size=15, color=text_color),
            xanchor="center",
            yanchor="bottom"
        ))

    # Update layout to fit data and include the season text in rectangles
    fig.update_layout(
        shapes=shapes,
        annotations=annotations,
        xaxis=dict(
            tickvals=months,
            ticktext=month_names,
            title='Mois',
            type='category',
            range=[-0.5, 12]  # Set x-axis range to fit all months
        ),
        yaxis=dict(
            title='Nombre de patients venus à IPM',
            range=[min_count - range_margin, max_count + range_margin]  # Set y-axis to include all data
        ),
        title={
            'text': "Affluence des patients venus au CTAR IPM sur période saisonnière d'une année",
            'x': 0.5,
            'xanchor': 'center'
        },
        height=700,  # Increase figure height
        width=7400,  # Increase figure width for better visibility
        legend_title='Légende'
    )

    # Remove the seasons from the legend
    fig.for_each_trace(lambda trace: trace.update(showlegend=False) if trace.name in season_backgrounds else None)


    # Show the plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)

def plot_saison_peripheral(df):

    df['date_de_consultation']=pd.to_datetime(df['date_de_consultation'])
    # Apply the function to create the 'season' column
    df['season'] = df['date_de_consultation'].apply(get_season)

    # Create new columns for month and year
    df['mois'] = df['date_de_consultation'].dt.month
    df['Annee'] = df['date_de_consultation'].dt.year
    df=df[df['Annee']<=2024]

    # Group by month, year, and sexe to count the number of patients for each sex
    monthly_sex_counts = df.groupby(['mois', 'Annee', 'sexe']).size().reset_index(name='count')

    # Define the month order for consistent x-axis labeling (January to December)
    months = list(range(1, 13))  # January to December
    month_names = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
        'Sep', 'Oct', 'Nov', 'Dec'
    ]

    # Determine the min and max count values for setting the y-axis range
    min_count = monthly_sex_counts['count'].min()
    max_count = monthly_sex_counts['count'].max()
    range_margin = (max_count - min_count) * 0.2  # Add some margin around the lines

    # Create a scatter plot with lines for each year and gender using Plotly
    fig = go.Figure()

    # Define color scales for male and female
    male_colors = pc.sequential.Blues[::-1]  # Shades of blue
    female_colors = pc.sequential.Reds[::-1]  # Shades of pink

    # Sort years in descending order to show recent years first
    years_sorted = sorted(monthly_sex_counts['Annee'].unique(), reverse=True)

    # Add scatter plot points for each year and sex (Male and Female)
    sexes = ['M', 'F']
    for i, year in enumerate(years_sorted):
        for j, sex in enumerate(sexes):
            df_year_sex = monthly_sex_counts[(monthly_sex_counts['Annee'] == year) & (monthly_sex_counts['sexe'] == sex)]
            df_year_sex = df_year_sex.set_index('mois').reindex(months).reset_index()
            df_year_sex['count'] = df_year_sex['count'].fillna(0)
            
            # Determine color based on gender
            if sex == 'M':
                color = male_colors[i % len(male_colors)]
            else:
                color = female_colors[i % len(female_colors)]

            fig.add_trace(go.Scatter(
                x=df_year_sex['mois'],
                y=df_year_sex['count'],
                mode='lines+markers',
                name=f"{int(year)} - {'Homme' if sex == 'M' else 'Femme'}",  # Ensure year and sex are displayed
                marker=dict(size=8, color=color),  # Use color from the gradient
                line=dict(width=2),
                visible="legendonly" if year < 2021 else True  # Show only the first 4 years initially
            ))

    # Define background colors for each season and corresponding text
    season_backgrounds = {
        'Fahavratra (pluie)': (12, 3, 'rgba(186, 225, 255, 0.3)', 'rgb(186, 225, 255)'),
        'Fararano (automne)': (3.5, 6, 'rgba(255, 186, 186, 0.3)', 'rgb(255, 186, 186)'),
        'Ritinina (hiver)': (6.5, 9, 'rgba(186, 255, 201, 0.3)', 'rgb(186, 255, 201)'),
        'Lohataona (été)': (9.5, 11.5, 'rgba(255, 223, 186, 0.3)', 'rgb(255, 223, 186)')
    }

    shapes = []
    annotations = []

    # Add season backgrounds to match the x-axis labels
    for season, (start_month, end_month, color, text_color) in season_backgrounds.items():
        if end_month < start_month:
            shapes.append(dict(
                type='rect',
                x0=start_month - 1,
                x1=11,  # Extend to December
                y0=min_count - range_margin,
                y1=max_count + range_margin,
                fillcolor=color,
                line=dict(width=0),
                layer='below'
            ))
            shapes.append(dict(
                type='rect',
                x0=1 - 1,  # Start from January
                x1=end_month - 0.5,
                y0=min_count - range_margin,
                y1=max_count + range_margin,
                fillcolor=color,
                line=dict(width=0),
                layer='below'
            ))
        else:
            shapes.append(dict(
                type='rect',
                x0=start_month - 1,
                x1=end_month - 0.5,
                y0=min_count - range_margin,
                y1=max_count + range_margin,
                fillcolor=color,
                line=dict(width=0),
                layer='below'
            ))

        # Add season text inside the colored rectangles
        annotations.append(dict(
            x=(start_month) / 10 if end_month < start_month else (start_month + end_month - 1) / 2,
            y=min_count - range_margin,  # Position text inside the rectangle
            text=season,
            showarrow=False,
            font=dict(size=15, color=text_color),
            xanchor="center",
            yanchor="bottom"
        ))

    # Update layout to fit data and include the season text in rectangles
    fig.update_layout(
        shapes=shapes,
        annotations=annotations,
        xaxis=dict(
            tickvals=months,
            ticktext=month_names,
            title='Mois',
            type='category',
            range=[-0.5, 12]  # Set x-axis range to fit all months
        ),
        yaxis=dict(
            title='Nombre de patients venus au CTAR',
            range=[min_count - range_margin, max_count + range_margin]  # Set y-axis to include all data
        ),
        title={
            'text': "Affluence des patients venus au CTAR périphérique sur période saisonnière d'une année",
            'x': 0.5,
            'xanchor': 'center'
        },
        height=700,  # Increase figure height
        width=7400,  # Increase figure width for better visibility
        legend_title='Légende'
    )

    # Remove the seasons from the legend
    fig.for_each_trace(lambda trace: trace.update(showlegend=False) if trace.name in season_backgrounds else None)


    # Show the plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)

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
            plot_saison_morsure_ipm(df)

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
                    plot_saison_peripheral(df)
            elif all_ctars_selected:  
                plot_saison_peripheral(df)
           

else:
    st.error("Aucun fichier n'a été téléchargé. Veuillez retourner à la page d'accueil pour télécharger un fichier.")


# Sidebar container with fixed width
with st.sidebar.container():
    st.image("Logo-CORAMAD.jpg", use_column_width=True, width=250, caption="FSPI Rage")