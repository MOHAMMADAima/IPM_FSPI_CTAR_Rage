import streamlit as st
import pandas as pd
import plotly.express as px

# Streamlit page
st.title("Nombre de sérothérapie prescrite par tranche d'âge et année.")

# Check if any dataframes have been uploaded in the session state
if 'dataframes' in st.session_state and st.session_state['dataframes']:
    # Get the first dataframe uploaded
    df_name, ipm = next(iter(st.session_state['dataframes'].items()))

    # Filter the data for ages between 0 and 100
    ipm = ipm[(ipm['age'] >= 0) & (ipm['age'] <= 100)]
    # Convert the date column if not already converted
    ipm['dat_consu'] = pd.to_datetime(ipm['dat_consu'], format='%d/%m/%Y', errors='coerce')

    # Extract the year from the date column
    ipm['year'] = ipm['dat_consu'].dt.year

    # Group age into intervals of 5 years
    age_bins = list(range(0, 105, 5))
    age_labels = [f"{i}-{i+4}" for i in age_bins[:-1]]
    ipm['age_group'] = pd.cut(ipm['age'], bins=age_bins, labels=age_labels, right=False)

    # Filter for 'OUI' values in the serother column
    ipm_oui = ipm[ipm['serother'] == 'OUI']

    # Group by year and age group to count 'OUI'
    counts = ipm_oui.groupby(['year', 'age_group']).size().reset_index(name='count')

    # Pivot the data for better visualization
    counts_pivot = counts.pivot_table(index=['year', 'age_group'], values='count', fill_value=0).reset_index()

    # Generate a list of unique colors for each age group
    unique_age_groups = counts_pivot['age_group'].unique()
    colors = px.colors.qualitative.Plotly  # You can use other color scales if you prefer
    color_map = dict(zip(unique_age_groups, colors))

    # Plot the data using Plotly
    fig = px.bar(
        counts_pivot,
        x='year',
        y='count',
        color='age_group',
        color_discrete_map=color_map,
        barmode='group',
        title="Nombre de sérothérapie prescrite par tranche d'âge et année.",
        labels={'count': 'Count', 'year': 'Year', 'age_group': 'Age Group'},
    )

    # Show the plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Veuillez d'abord télécharger les fichiers CSV sur la page d'accueil.")

# Sidebar container with fixed width
with st.sidebar.container():
    st.image("Logo-CORAMAD.jpg", use_column_width=True, width=250, caption="FSPI Rage")
