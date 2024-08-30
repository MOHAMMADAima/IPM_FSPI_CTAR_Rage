import pandas as pd
import folium
import matplotlib.pyplot as plt
import io
import base64
from streamlit_folium import st_folium
import streamlit as st

# Corrected Data Preparation
data = {
    'CTAR': [
        'AMBATOMAINTY', 'AMBATONDRAZAKA', 'AMBOSITRA', 'AMBOVOMBE ANDROY',
        'ANTSIRABE', 'ANTSIRANANA', 'ANTSOHIHY', 'BEKILY', 'FIANARANTSOA',
        'FORT DAUPHIN', 'IHOSY', 'MAEVATANANA', 'MAHAJANGA', 'MAINTIRANO',
        'MANAKARA', 'MANANJARY', 'MANDRITSARA', 'MANJA', 'MAROANTSETRA',
        'MAROLAMBO', 'MIARINARIVO ITASY', 'MORAMANGA', 'MORONDAVA', 'NOSY BE',
        'SAMBAVA', 'SOANIERANA IVONGO', 'STE MARIE', 'TOAMASINA', 'TOLIARY',
        'TSIROANOMANDIDY', 'VANGAINDRANO'
    ],
    'JANV': [None, 200, 100, None, 100, 150, None, None, 75, 200, None, 100, 120, None, 100, None, 150, 50, None, None, None, None, None, None, 140, 150, None, 240, None, 100],
    'FEV': [None, None, 100, None, 100, None, 150, None, None, None, 100, None, 120, 100, 100, None, None, None, None, None, None, None, 100, None, None, 50, 100, None, 240, None, None],
    'MARS': [None, 200, None, None, 200, None, 75, None, 50, None, 100, 100, 60, 20, 100, None, 150, None, 40, None, 75, 200, 125, 100, 130, 150, 100, 100, None, 100, 25],
    'AVRIL': [None, 50, 50, None, 100, None, 125, None, None, 150, 100, 100, 115, None, None, None, None, None, None, None, 100, None, None, 75, 100, None, 100, 200, None, 100],
    'MAI': [None, 100, 100, None, 225, 100, 100, 70, None, None, 100, 100, 120, 50, 100, 100, None, None, None, 80, 75, 50, 100, None, 25, 100, None, 240, 100, 100],
    'JUIN': [None, 100, None, None, 140, None, 150, 70, None, None, 100, None, 80, None, None, None, None, None, None, None, 100, 150, None, None, 100, None, None, 200, None, None],
    'JUILL': [None, 100, None, None, 200, None, None, None, None, None, None, 100, 120, None, 100, 30, 150, 80, None, None, None, 100, 200, None, 100, None, None, 300, None, 100],
    'AOUT': [None, 300, None, None, 200, None, 200, None, None, None, None, 100, 160, None, 100, 30, 150, 80, None, None, None, 100, 200, None, 100, None, 300, None, None, 100],
    'SEPT': [None, None, 100, None, 200, None, 200, None, None, None, None, 100, 100, None, 100, None, None, None, None, None, 200, None, 100, None, None, None, 300, None, None, 100],
    'OCT': [None, 100, None, None, 100, None, 200, None, None, 150, 100, 100, 100, None, 100, None, None, 80, None, 80, 100, None, 100, 80, 100, None, 300, None, None, 100],
    'NOV': [None, 200, 100, 100, 100, None, 150, None, None, 150, 500, 100, 100, None, 100, None, None, 80, None, 80, 100, None, None, 150, 200, None, 100, None, None, 100],
    'DEC': [None, 200, None, 103, 100, 200, 200, 12, 340, 500, 16, 400, 100, 120, 50, None, 450, 80, 80, 25, 1020, 1250, 525, 300, 1065, 1745, 101, 2120, 400, 605, 780],
    'TOTAUX': [None, 1550, 650, 103, 1735, 650, 1180, 12, 340, 500, 500, 400, 1095, 120, 800, 30, 450, 80, 80, 25, 1020, 1250, 525, 300, 1065, 1745, 101, 2120, 400, 605, 780],
    'ID_CTAR': [100, 7, 30, 103, 13, 10, 14, 12, 2, 102, 16, 17, 18, 19, 31, 97, 15, 23, 4, 21, 8, 22, 9, 24, 1, 101, 28, 26, 27, 3]
}

df = pd.DataFrame(data)

# Function to create histogram image
def create_histogram_image(values):
    values = [v for v in values if pd.notna(v) and v != 0]

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.hist(values, bins=range(0, int(max(values)) + 10, 10), color='skyblue', edgecolor='black')
    ax.set_title('Monthly Distribution')
    ax.set_xlabel('Value')
    ax.set_ylabel('Frequency')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode()
    plt.close(fig)

    return img_str

# Define town information with coordinates
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

# Create the map
m = folium.Map(location=[-19, 47], zoom_start=5.5, tiles='OpenStreetMap')

# Add markers with histograms to the map
for key, (town_name, (lat, lon)) in towns_info.items():
    # Get the town data
    town_data = df[df['ID_CTAR'] == key].iloc[0]
    monthly_values = [
        town_data['JANV'], town_data['FEV'], town_data['MARS'], town_data['AVRIL'],
        town_data['MAI'], town_data['JUIN'], town_data['JUILL'], town_data['AOUT'],
        town_data['SEPT'], town_data['OCT'], town_data['NOV'], town_data['DEC']
    ]
    
    # Create histogram image
    histogram_img = create_histogram_image(monthly_values)
    
    # HTML content for popup
    popup_html = f"""
    <b>{town_name}</b><br>
    <img src='data:image/png;base64,{histogram_img}' width='400'>
    """
    
    # Add marker to the map
    folium.Marker([lat, lon], popup=folium.Popup(popup_html, max_width=500)).add_to(m)

# Save the map to an HTML file
m.save('map_with_histograms.html')

# Display the map in Streamlit
st.title("Town Histogram Map")
st_folium(m, width=800, height=600)
