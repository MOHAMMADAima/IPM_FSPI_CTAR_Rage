import streamlit as st
import pandas as pd
import plotly.express as px

# Streamlit page
st.title("Nombre de cas selon la valeur de 'serother'")

# Check if any dataframes have been uploaded in the session state
if 'dataframes' in st.session_state and st.session_state['dataframes']:
    # Get the first dataframe uploaded
    df_name, ipm = next(iter(st.session_state['dataframes'].items()))

    # Count the number of rows for each value in 'serother'
    serother_counts = ipm['serother'].value_counts().reset_index()
    serother_counts.columns = ['serother', 'count']

    # Plot the counts using Plotly
    fig = px.bar(
        serother_counts,
        x='serother',
        y='count',
        labels={'serother': 'Valeur de serother', 'count': 'Nombre de cas'},
        title="Nombre de cas avec 'OUI' et 'NON' dans la colonne 'serother'",
        color='serother'
    )

    # Update layout for better readability
    fig.update_layout(
        xaxis_title='Valeur de serother',
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
