import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Streamlit page
st.title("Affluence des patients venus au CTAR IPM sur période saisonnière d'une année.")
# Check if any dataframes have been uploaded in the session state
if 'dataframes' in st.session_state and st.session_state['dataframes']:
    # Get the first dataframe uploaded
    df_name, ipm = next(iter(st.session_state['dataframes'].items()))

    # Convert date columns
    ipm['dat_consu'] = pd.to_datetime(ipm['dat_consu'], format='%d/%m/%Y', errors='coerce')
    ipm['vacc_vero_date'] = pd.to_datetime(ipm['vacc_vero_date'], format='%d/%m/%Y', errors='coerce')
    ipm['vacc_sour_date'] = pd.to_datetime(ipm['vacc_sour_date'], format='%d/%m/%Y', errors='coerce')

    # Create the new date column with the required logic
    ipm['new_date_column'] = ipm['dat_consu'].fillna(ipm['vacc_vero_date']).fillna(ipm['vacc_sour_date'])

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

    # Define month names
    month_names = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 
        'Sep', 'Oct', 'Nov', 'Dec'
    ]

    # Define the month order based on the actual data
    months_present = monthly_counts['month'].unique()  # Only the months present in the data
    month_names_present = [month_names[m-1] for m in months_present]  # Map to month names

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
        df_year = monthly_counts[monthly_counts['year'] == year].set_index('month').reindex(months_present).reset_index()
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

    # Update layout to fit data
    fig.update_layout(
        xaxis=dict(
            tickvals=months_present,
            ticktext=month_names_present,
            title='Mois',
            type='category',
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

    # Show the plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Veuillez d'abord télécharger les fichiers CSV sur la page d'accueil.")

# Sidebar container with fixed width
with st.sidebar.container():
    st.image("Logo-CORAMAD.jpg", use_column_width=True, width=250, caption="FSPI Rage")
