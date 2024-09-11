import streamlit as st
import pandas as pd
import plotly.express as px

# Streamlit page
st.title("Comparaison des valeurs de 'ref_mordu' selon 'serother'")

# Check if any dataframes have been uploaded in the session state
if 'dataframes' in st.session_state and st.session_state['dataframes']:
    # Get the first dataframe uploaded
    df_name, ipm = next(iter(st.session_state['dataframes'].items()))

    # Filter the dataframe for 'OUI' and 'NON' in 'serother' column
    df_oui = ipm[ipm['serother'] == 'OUI']
    df_non = ipm[ipm['serother'] == 'NON']

    # Count the occurrences of each 'ref_mordu' value for both 'OUI' and 'NON'
    count_oui = df_oui['ref_mordu'].value_counts().reset_index()
    count_non = df_non['ref_mordu'].value_counts().reset_index()

    # Rename columns for better readability
    count_oui.columns = ['ref_mordu', 'count_OUI']
    count_non.columns = ['ref_mordu', 'count_NON']

    # Merge the counts into a single DataFrame for comparison
    comparison_df = pd.merge(count_oui, count_non, on='ref_mordu', how='outer').fillna(0)

    # Plot the counts using Plotly
    fig = px.bar(
        comparison_df,
        x='ref_mordu',
        y=['count_OUI', 'count_NON'],
        barmode='group',
        labels={'value': 'Nombre de cas', 'ref_mordu': 'Ref Mordu'},
        title="Nombre de 'ref_mordu' selon la valeur de 'serother' ('OUI' vs 'NON')"
    )

    # Update layout for better readability
    fig.update_layout(
        xaxis_title='Référence du mordu',
        yaxis_title='Nombre de cas',
        legend_title='Sérotherapie',
        height=600,
        width=900,
    )

    # Show the plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Veuillez d'abord télécharger les fichiers CSV sur la page d'accueil.")

# Sidebar container with fixed width
with st.sidebar.container():
    st.image("Logo-CORAMAD.jpg", use_column_width=True, width=250, caption="FSPI Rage")
