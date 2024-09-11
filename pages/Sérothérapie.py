import streamlit as st
import pandas as pd
import plotly.express as px

# Streamlit page
st.title("Counts of 'OUI' and 'NON' in Serotherapy by Year and Age Group")

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

    # Group by year, age group, and serother to count 'OUI' and 'NON'
    counts = ipm.groupby(['year', 'age_group', 'serother']).size().reset_index(name='count')

    # Pivot the data for better visualization
    counts_pivot = counts.pivot_table(index=['year', 'age_group'], columns='serother', values='count', fill_value=0).reset_index()

    # Plot the data using Plotly
    fig = px.bar(
        counts_pivot,
        x='year',
        y=['OUI', 'NON'],
        color='age_group',
        barmode='group',
        title="Counts of 'OUI' and 'NON' in Serotherapy by Year and Age Group",
        labels={'value': 'Count', 'year': 'Year', 'variable': 'Serotherapy'},
    )

    # Show the plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Veuillez d'abord télécharger les fichiers CSV sur la page d'accueil.")
