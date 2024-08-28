import streamlit as st
import pandas as pd

# Set page title and icon
st.set_page_config(
    page_title="API Cleaning",
    page_icon="🌐"
)

# Custom colors for the theme
primary_color = "#4c8dc1"  # Blue
secondary_color = "#ffffff"  # White

# Set theme using markdown
st.markdown(
    f"""
    <style>
        .reportview-container {{
            background-color: {secondary_color};
            color: #000000;
        }}
        .stButton > button {{
            background-color: {primary_color};
            color: {secondary_color};
        }}
        .stTextInput > div > div > input {{
            background-color: {secondary_color};
            color: #000000;
        }}
        .stDataFrame > div > div > div > div > table {{
            background-color: {secondary_color};
        }}
        .custom-background {{
            background-color: {primary_color};
            padding: 10px;
            border-radius: 10px;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
st.title("Bienvenue sur CTAR Indicateurs 🌐")
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("###### Une application d'analyse des indicateurs de performance des CTAR de Madagascar, à l'initiative de IPM.")
st.markdown("#### Instructions :")
st.markdown("1. **Téléchargez votre fichier CSV :**")
st.markdown("   - Sélectionnez et téléchargez les fichiers CSV contenant les données à analyser.")
st.markdown("2. **Vérifiez les Pays :**")

def main():
    st.markdown("<h3 style='text-align: left; margin-top: 20px;'>1. Téléchargez vos fichiers :</h3>", unsafe_allow_html=True)

    # Allow multiple CSV files to be uploaded
    uploaded_files = st.file_uploader("Sélectionnez les fichiers CSV", type=["csv"], accept_multiple_files=True)

    # Provide an option for the user to specify the encoding
    encoding = st.sidebar.selectbox(
        "Sélectionnez l'encodage du fichier",
        options=["utf-8", "ISO-8859-1", "cp1252", "latin1", "utf-16"],
        index=0
    )

    # Check if any files have been uploaded
    if uploaded_files:
        # Create an empty dictionary to hold the dataframes
        dataframes = {}

        # Loop through uploaded files and read them into pandas dataframes
        for uploaded_file in uploaded_files:
            try:
                df = pd.read_csv(uploaded_file, encoding=encoding, sep=';')
                dataframes[uploaded_file.name] = df
            except UnicodeDecodeError as e:
                st.error(f"Erreur de décodage pour le fichier {uploaded_file.name}: {e}")
                continue

        # Sidebar for main page selection
        page_selection = st.sidebar.selectbox('Sélectionnez une Page (Fichier)', list(dataframes.keys()))

        # Display main page content
        st.header(f"Contenu du fichier: {page_selection}")
        st.dataframe(dataframes[page_selection].head())

        # Display the sub-page table content based on selected main page (if needed)
        sub_page_options = dataframes[page_selection].columns.tolist()
        sub_page_selection = st.sidebar.selectbox('Sélectionnez une Colonne', sub_page_options)

        st.subheader(f"Contenu de la colonne: {sub_page_selection}")
        st.write(dataframes[page_selection][sub_page_selection])

if __name__ == '__main__':
    main()

# Footer
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.write("Pour toute question/information : aima.mohammad.pro@gmail.com ")
st.markdown("---")
st.write("Created by MOHAMMAD Aima")
st.write("IPM © 2024")

# Sidebar container with fixed width
with st.sidebar.container():
    st.image("Logo-CORAMAD.jpg", use_column_width=True, width=250, caption="FSPI Rage")
