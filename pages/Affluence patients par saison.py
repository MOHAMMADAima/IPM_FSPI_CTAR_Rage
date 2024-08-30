# Graph.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

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

    # Define the month order for consistent x-axis labeling (January to December)
    months = list(range(1, 13))  # January to December
    month_names = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 
        'Sep', 'Oct', 'Nov', 'Dec'
    ]

    # Determine the min and max count values for setting the y-axis range
    min_count = monthly_counts['count'].min()
    max_count = monthly_counts['count'].max()
    range_margin = (max_count - min_count) * 0.2  # Add some margin around the lines

    # Create a scatter plot with lines for each year using Plotly
    fig = go.Figure()

    # Use a color map to ensure unique colors for each year
    color_map = px.colors.qualitative.Plotly  # A set of distinct colors

    # Sort years in descending order to show recent years first
    years_sorted = sorted(monthly_counts['year'].unique(), reverse=True)

    # Add scatter plot points for each year
    for i, year in enumerate(years_sorted):
        df_year = monthly_counts[monthly_counts['year'] == year].set_index('month').reindex(months).reset_index()
        df_year['count'] = df_year['count'].fillna(0)
        fig.add_trace(go.Scatter(
            x=df_year['month'],
            y=df_year['count'],
            mode='lines+markers',
            name=int(year),  # Ensure year is displayed as integer
            marker=dict(size=8, color=color_map[i % len(color_map)]),  # Ensure unique color
            line=dict(width=2),
            visible="legendonly" if year < 2020 else True  # Show only the first 5 years initially
        ))

    # Define background colors for each season and corresponding text
    season_backgrounds = {
        'Lohataona (été)': (9.5, 11.5, 'rgba(255, 223, 186, 0.3)', 'rgb(255, 223, 186)'),
        'Fahavratra (pluie)': (12, 3, 'rgba(186, 225, 255, 0.3)', 'rgb(186, 225, 255)'),
        'Fararano (automne)': (3.5, 6, 'rgba(255, 186, 186, 0.3)', 'rgb(255, 186, 186)'),
        'Ritinina (hiver)': (6.5, 9, 'rgba(186, 255, 201, 0.3)', 'rgb(186, 255, 201)')
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
            x=(start_month + end_month-1) / 2 if end_month > start_month else (start_month + end_month + 11) / 2,
            y=min_count - range_margin - 0.5,  # Position text inside the rectangle
            text=season,
            showarrow=False,
            font=dict(size=14, color=text_color),
            xanchor="left",
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
            range=[-1, 11]  # Set x-axis range to fit all months
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
        width=1400,  # Increase figure width for better visibility
        legend_title='Légende'
    )

    # Remove the seasons from the legend
    fig.for_each_trace(lambda trace: trace.update(showlegend=False) if trace.name in season_backgrounds else None)

    # Show the plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Veuillez d'abord télécharger les fichiers CSV sur la page d'accueil.")
