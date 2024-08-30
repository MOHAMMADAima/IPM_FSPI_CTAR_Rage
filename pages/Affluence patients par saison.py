# Graph.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Check if any dataframes have been uploaded in the session state
if 'dataframes' in st.session_state and st.session_state['dataframes']:
    # Get the first dataframe uploaded
    df_name, ipm = next(iter(st.session_state['dataframes'].items()))

    # Convert date columns
    ipm['vacc_sour_date'] = pd.to_datetime(ipm['vacc_sour_date'], errors='coerce')
    ipm['vacc_vero_date'] = pd.to_datetime(ipm['vacc_vero_date'], errors='coerce')

    # Create the new date column with the required logic
    ipm['new_date_column'] = ipm['vacc_sour_date'].combine_first(ipm['vacc_vero_date'])
    ipm['new_date_column'] = ipm['new_date_column'].dt.strftime('%Y-%m-%d')
    ipm['new_date_column'] = pd.to_datetime(ipm['new_date_column'], format='%Y-%m-%d', errors='coerce')

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

    # Apply the function to create the 'season' column
    ipm['season'] = ipm['new_date_column'].apply(get_season)

    # Create new columns for month and year
    ipm['month'] = ipm['new_date_column'].dt.month
    ipm['year'] = ipm['new_date_column'].dt.year

    # Group by month and year, and count the number of lines in each group
    monthly_counts = ipm.groupby(['month', 'year']).size().reset_index(name='count')

    # Aggregate counts across years for each month
    monthly_counts_all_years = ipm.groupby(['month']).size().reset_index(name='count')

    # Define the month order for consistent x-axis labeling
    months = list(range(1, 13))
    month_names = [pd.to_datetime(f'2022-{i:02d}-01').strftime('%b') for i in months]

    # Create a scatter plot with lines for each year using Plotly
    fig = go.Figure()

    # Add scatter plot points for each year
    for year in sorted(monthly_counts['year'].unique()):
        df_year = monthly_counts[monthly_counts['year'] == year].set_index('month').reindex(months).reset_index()
        df_year['count'] = df_year['count'].fillna(0)
        fig.add_trace(go.Scatter(
            x=df_year['month'],
            y=df_year['count'],
            mode='lines+markers',
            name=str(round(year)),
            marker=dict(size=8),
            line=dict(width=2)
        ))

    # Define background colors for each season
    season_backgrounds = {
        'été-Lohataona': (9, 12, 'rgba(255, 223, 186, 0.3)'),
        'pluie-Fahavratra': (12, 3, 'rgba(186, 225, 255, 0.3)'),
        'automne-Fararano': (3, 6, 'rgba(255, 186, 186, 0.3)'),
        'hiver-Ritinina': (6, 9, 'rgba(186, 255, 201, 0.3)')
    }

    # Add background rectangles for each season
    shapes = []
    for season, (start_month, end_month, color) in season_backgrounds.items():
        shapes.append(dict(
            type='rect',
            x0=start_month,
            x1=end_month if end_month > start_month else end_month + 12,
            y0=0,
            y1=monthly_counts_all_years['count'].max(),
            fillcolor=color,
            line=dict(width=0),
            layer='below'
        ))

    # Construct season subtitles
    season_subtitle = ', '.join(season for season in season_backgrounds.keys())

    # Update layout to fit data, center graph, and set autoscale
    fig.update_layout(
        shapes=shapes,
        xaxis=dict(
            tickvals=months,
            ticktext=month_names,
            title='Mois',
            type='category',
            range=[-0.5, 12]
        ),
        yaxis=dict(
            title='Nombre de patients venus à IPM',
            autorange=True  # Autoscale Y-axis to fit data
        ),
        title={
            'text': f"Affluence des patients venus au CTAR IPM sur période saisonnière d'une année<br><sup>{season_subtitle}</sup>",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        legend_title='Année',
        margin=dict(l=40, r=40, t=40, b=40)
    )

    # Show the plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)  # Adjust to container width to center graph

else:
    st.warning("Veuillez d'abord télécharger les fichiers CSV sur la page d'accueil.")
