import streamlit as st
import pandas as pd
import plotly.express as px

# Streamlit page
st.title("Sérothérapie prescrite par le CTAR.")

# Check if any dataframes have been uploaded in the session state
if 'dataframes' in st.session_state and st.session_state['dataframes']:
    # Get the first dataframe uploaded
    df_name, ipm = next(iter(st.session_state['dataframes'].items()))

    # Convert the date column if not already converted
    ipm['dat_consu'] = pd.to_datetime(ipm['dat_consu'], format='%d/%m/%Y', errors='coerce')

    # Extract the year from the date column
    ipm['year'] = ipm['dat_consu'].dt.year

    # Count the number of rows for each value in 'serother' grouped by year
    serother_counts = ipm.groupby(['year', 'serother']).size().reset_index(name='count')

    # Plot the counts using Plotly
    fig = px.bar(
        serother_counts,
        x='year',
        y='count',
        color='serother',
        labels={'year': 'Année', 'count': 'Nombre de patients', 'serother': 'Serotherapie prescrite'},
        title="Nombre de cas avec sérothérapie prescrite par année au CTAR IPM",
        barmode='group'
    )

    # Update layout for better readability
    fig.update_layout(
        xaxis_title='Année',
        yaxis_title='Nombre de cas',
        height=500,
        width=700,
    )

    # Show the plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Veuillez d'abord télécharger les fichiers CSV sur la page d'accueil.")

# Sidebar container with fixed width
with st.sidebar.container():
    st.image("Logo-CORAMAD.jpg", use_column_width=True, width=250, caption="FSPI Rage")
