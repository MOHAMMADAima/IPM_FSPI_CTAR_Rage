import streamlit as st
import pandas as pd

# Streamlit page
st.title("Comptage des valeurs de 'serother' par année et groupe d'âge")

# Check if any dataframes have been uploaded in the session state
if 'dataframes' in st.session_state and st.session_state['dataframes']:
    # Get the first dataframe uploaded
    df_name, ipm = next(iter(st.session_state['dataframes'].items()))



    # Create new columns for year and age groups
    ipm['year'] = ipm['dat_consu'].dt.year
    ipm['age_group'] = (ipm['age'] // 5) * 5  # Grouping ages by 5-year intervals

    # Group the data by 'year', 'age_group', and 'serother' and count occurrences
    count_df = ipm.groupby(['year', 'age_group', 'serother']).size().reset_index(name='count')

    # Pivot the dataframe for easier plotting
    pivot_df = count_df.pivot_table(index=['year', 'age_group'], columns='serother', values='count', fill_value=0).reset_index()

    # Display the dataframe
    st.dataframe(pivot_df)

    # Plotting the counts
    st.subheader("Graphique du comptage des valeurs 'OUI' et 'NON' par année et groupe d'âge")

    for age_group in sorted(pivot_df['age_group'].unique()):
        df_group = pivot_df[pivot_df['age_group'] == age_group]
        st.write(f"Groupe d'âge: {age_group}-{age_group + 4} ans")

        st.bar_chart(df_group.set_index('year')[['OUI', 'NON']])

else:
    st.warning("Veuillez d'abord télécharger les fichiers CSV sur la page d'accueil.")

# Sidebar container with fixed width
with st.sidebar.container():
    st.image("Logo-CORAMAD.jpg", use_column_width=True, width=250, caption="FSPI Rage")
