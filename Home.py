import streamlit as st
import pandas as pd

# Set page title and icon
st.set_page_config(
    page_title="API Cleaning",
    page_icon="🌐",  # You can use a different icon here
)

# Custom colors
primary_color = "#4c8dc1"  # Blue
secondary_color = "#ffffff"  # White

# Set theme
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
st.markdown("1. **Téléchargez votre fichier :**")
st.markdown("   - Sélectionnez et téléchargez le fichier Excel contenant les données à analyser.")
st.markdown("2. **Vérifiez les Pays :**")

def main():
    st.markdown("<h3 style='text-align: left; margin-top: 20px;'>1. Télécharger votre fichier :</h3>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Sélectionnez un fichier Excel (.xlsx ou .xls)", type=["xlsx", "xls"], key="file")


    if uploaded_file is not None:
        st.session_state.uploaded_data = pd.read_excel(uploaded_file)

        st.write("Aperçu des données :")
        st.dataframe(st.session_state.uploaded_data.head())
        st.markdown("<br>", unsafe_allow_html=True)

        # Instruct the user to go to the Pays page
        st.markdown("<p style='font-size: large;'>Le fichier a été téléchargé avec succès.</p>", unsafe_allow_html=True)
        st.markdown("<p> Pour vérifier les pays, aller à la page <b>Etape1 (Pays)</b>.</p>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()

# Main content

# Footer
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.write("Pour toute question/information : aima.mohammad.pro@gmail.com ")
st.markdown("---")
st.write("Created by MOHAMMAD Aima")
st.write("IPM © 2024")

# Sidebar container with fixed width
with st.sidebar.container():
    st.image("Logo-CORAMAD.jpg", use_column_width=True, width=250, caption="FSPI Rage")
