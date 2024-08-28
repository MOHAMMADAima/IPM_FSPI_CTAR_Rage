import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set Streamlit page configuration
st.set_page_config(page_title="Affluence des patients au CTAR IPM", layout="wide")

# Retrieve the 'ipm' DataFrame from the session state
if 'dataframes' in st.session_state:
    ipm = st.session_state['dataframes']
else:
    st.error("Le DataFrame 'ipm' n'est pas chargé dans l'état de session.")
    st.stop()

# Ensure 'new_date_column' is in the DataFrame
if 'new_date_column' not in ipm.columns:
    st.error("'new_date_column' is missing in the DataFrame. Please ensure it is correctly loaded.")
    st.stop()

# Create new columns for month and year
ipm['new_date_column'] = pd.to_datetime(ipm['new_date_column'], errors='coerce')  # Ensure datetime format
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
        x1=end_month if end_month > start_month else end_month + 12,  # Adjust for year wrap-around
        y0=0,
        y1=monthly_counts_all_years['count'].max(),
        fillcolor=color,
        line=dict(width=0),
        layer='below'  # Ensure the background is below the lines
    ))

# Add dummy traces for each season to include them in the legend
for season, (start_month, end_month, color) in season_backgrounds.items():
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        marker=dict(size=10, color=color),
        name=season,
        legendgroup='seasons',
        showlegend=True
    ))

# Sort years in descending order for the legend
sorted_years = sorted(monthly_counts['year'].unique(), reverse=True)

# Add scatter plot points for each year
for year in sorted_years:
    df_year = monthly_counts[monthly_counts['year'] == year]
    # Reindex month to ensure order
    df_year = df_year.set_index('month').reindex(months).reset_index()
    # Handle missing months
    df_year['count'] = df_year['count'].fillna(0)
    visible = True if year >= 2018 else 'legendonly'
    fig.add_trace(go.Scatter(
        x=df_year['month'],
        y=df_year['count'],
        mode='lines+markers',
        name=str(year),
        marker=dict(size=8),
        line=dict(width=2),
        visible=visible,
        legendgroup='years'
    ))

# Update layout to fit data and zoom on lines
fig.update_layout(
    shapes=shapes,
    xaxis_title='Mois',
    yaxis_title='Nombre de patients venus à IPM',
    xaxis=dict(
        tickvals=months,
        ticktext=month_names,
        title='Mois',
        type='category',
        range=[-0.5, 12]
    ),
    yaxis=dict(
        title='Nombre de patients venus à IPM',
        range=[0, monthly_counts_all_years['count'].max() * 1.1]
    ),
    title='Affluence de patients au CTAR IPM par an',
    legend_title='Légende',
    legend=dict(
        title='Légende',
        tracegroupgap=15
    ),
    clickmode='event+select'
)

# Display the plot in Streamlit
st.plotly_chart(fig)
