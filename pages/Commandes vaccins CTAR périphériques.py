import streamlit as st
import folium
import base64
import io
import matplotlib.pyplot as plt
import pandas as pd
from streamlit_folium import st_folium

# Define the updated dictionary for town names and GPS coordinates
towns_info = {
    7: ("Ambatondrazaka", (-17.8324, 48.4086)),
    30: ("Ambositra", (-20.5300, 47.2441)),
    100: ("Ambatomainty", (-17.1884, 44.5947)),
    13: ("Antsirabe", (-19.8659, 47.0333)),
    10: ("Antsiranana", (-12.2795, 49.2913)),
    14: ("Antsohihy", (-14.8667, 47.9833)),
    12: ("Bekily", (-24.2333, 45.3833)),
    1: ("Soanierana Ivongo", (-16.9167, 49.5833)),
    2: ("Fianarantsoa", (-21.4545, 47.0833)),
    16: ("Ihosy", (-22.4021, 46.1253)),
    17: ("Maevatanana", (-16.9333, 46.8333)),
    18: ("Mahajanga", (-15.7167, 46.3167)),
    19: ("Maintirano", (-18.0566, 44.0297)),
    31: ("Manakara", (-22.1451, 48.0115)),
    15: ("Mandritsara", (-15.8333, 48.8333)),
    23: ("Manja", (-21.4167, 44.8667)),
    4: ("Maroantsetra", (-15.4333, 49.7500)),
    21: ("Miarinarivo", (-19.0010, 46.7334)),
    8: ("Moramanga", (-18.9333, 48.2000)),
    22: ("Morondava", (-20.2833, 44.2833)),
    9: ("Nosy Be", (-13.3333, 48.2667)),
    24: ("Sambava", (-14.2667, 50.1667)),
    101: ("Sainte Marie", (-17.0000, 49.8500)),
    25: ("Taolagnaro", (-25.0314, 46.9821)),
    28: ("Toamasina", (-18.1492, 49.4023)),
    26: ("Toliara", (-23.3568, 43.6917)),
    27: ("Tsiroanomandidy", (-18.7713, 46.0520)),
    3: ("Vangaindrano", (-23.3479, 47.5972)),
    97: ("Mananjary", (-21.2300, 48.3439)),
    102: ("Fort Dauphin", (-25.0347, 46.9883)),
    103: ("Ambovombe", (-25.1744, 46.0876))
}

# Function to create a histogram as a base64 image
def create_histogram(data):
    months = ['JANV', 'FEV', 'MARS', 'AVRIL', 'MAI', 'JUIN', 'JUILL', 'AOUT', 'SEPT', 'OCT', 'NOV', 'DEC']
    values = [data.get(month, 0) for month in months]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(months, values, color='skyblue')
    ax.set_xlabel('Month')
    ax.set_ylabel('Value')
    ax.set_title('Monthly Values')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save histogram to a base64 string
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode()
    
    # Close the figure to prevent memory leak
    plt.close(fig)

    return img_str

# Streamlit app
st.title("Interactive Map with Monthly Histograms")

# File uploader
uploaded_file = st.file_uploader("Upload the Excel file", type=["xlsx"])

if uploaded_file:
    # Load the Excel file
    df = pd.read_excel(uploaded_file)
    
    # Ensure 'ID_CTAR' column is of integer type
    df['ID_CTAR'] = pd.to_numeric(df['ID_CTAR'], errors='coerce').fillna(0).astype(int)
    
    # Initialize the map
    m = folium.Map(location=[-18.5, 47], zoom_start=5.5, tiles='OpenStreetMap')

    # Create markers for each town
    for key, (town_name, (lat, lon)) in towns_info.items():
        # Find the row corresponding to the town
        town_row = df[int(df['ID_CTAR']) == key]
        if not town_row.empty:
            # Extract monthly values
            town_data = town_row.iloc[0].drop(['CTAR', 'TOTAUX', 'ID_CTAR']).to_dict()
            
            # Create HTML content for the popup
            popup_html = f"<b>{town_name}</b><br>" \
                         f"<br><b>Monthly Values:</b><br>" \
                         f"<img src='data:image/png;base64,{create_histogram(town_data)}'>"

            # Create the marker with the popup
            folium.Marker([lat, lon], popup=popup_html).add_to(m)

    # Save the map to an HTML file and display it in Streamlit
    map_html = 'map.html'
    m.save(map_html)

    # Display the map using Streamlit
    st_folium(m, width=800, height=600)
