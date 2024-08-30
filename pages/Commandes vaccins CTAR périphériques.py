import pandas as pd
import folium
import matplotlib.pyplot as plt
import io
import base64
from streamlit_folium import st_folium
import streamlit as st

# Data Preparation
towns = [
    'AMBATOMAINTY', 'AMBATONDRAZAKA', 'AMBOSITRA', 'AMBOVOMBE ANDROY', 'ANTSIRABE',
    'ANTSIRANANA', 'ANTSOHIHY', 'BEKILY', 'FIANARANTSOA', 'FORT DAUPHIN', 'IHOSY',
    'MAEVATANANA', 'MAHAJANGA', 'MAINTIRANO', 'MANAKARA', 'MANANJARY', 'MANDRITSARA',
    'MANJA', 'MAROANTSETRA', 'MAROLAMBO', 'MIARINARIVO ITASY', 'MORAMANGA', 'MORONDAVA',
    'NOSY BE', 'SAMBAVA', 'SOANIERANA IVONGO', 'STE MARIE', 'TOAMASINA', 'TOLIARY',
    'TSIROANOMANDIDY', 'VANGAINDRANO', None
]

data = {
    'JANV': [float('nan'), 200.0, 100.0, float('nan'), 100.0, 150.0, float('nan'), float('nan'), 75.0, 200.0, float('nan'), 100.0, 120.0, float('nan'), 100.0, float('nan'), 150.0, 50.0, float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 140.0, 150.0, float('nan'), float('nan'), float('nan'), 100.0, 100.0, float('nan')],
    'FEV': [float('nan'), float('nan'), 100.0, float('nan'), 100.0, float('nan'), 150.0, float('nan'), float('nan'), float('nan'), 100.0, float('nan'), 120.0, float('nan'), 100.0, float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 100.0, float('nan'), 100.0, float('nan'), 50.0, 150.0, float('nan'), 240.0, float('nan'), float('nan'), float('nan'), float('nan')],
    'MARS': [float('nan'), 200.0, float('nan'), float('nan'), 200.0, float('nan'), float('nan'), float('nan'), 75.0, float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 100.0, float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 200.0, 250.0, float('nan'), 100.0, 130.0, 150.0, float('nan'), 240.0, 100.0, float('nan'), 100.0, float('nan')],
    'AVRIL': [float('nan'), 50.0, 50.0, float('nan'), 100.0, 100.0, 75.0, float('nan'), 50.0, float('nan'), float('nan'), float('nan'), 60.0, float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 50.0, float('nan'), float('nan'), float('nan'), 75.0, 100.0, float('nan'), 100.0, float('nan'), 25.0, float('nan'), float('nan')],
    'MAI': [float('nan'), 100.0, 100.0, float('nan'), 225.0, float('nan'), 125.0, float('nan'), float('nan'), float('nan'), 100.0, 100.0, 115.0, 20.0, float('nan'), float('nan'), 150.0, float('nan'), 40.0, float('nan'), 100.0, 150.0, 125.0, 100.0, 100.0, 25.0, float('nan'), 240.0, float('nan'), 200.0, 100.0, float('nan')],
    'JUIN': [float('nan'), 100.0, 100.0, float('nan'), 70.0, 100.0, 100.0, float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 120.0, float('nan'), 100.0, float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 70.0, float('nan'), float('nan'), float('nan'), 100.0, 150.0, float('nan'), 200.0, float('nan'), 100.0, float('nan'), float('nan')],
    'JUILL': [float('nan'), 100.0, float('nan'), float('nan'), 140.0, float('nan'), 230.0, float('nan'), 60.0, 150.0, 100.0, float('nan'), 80.0, 50.0, 100.0, float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 100.0, float('nan'), float('nan'), 100.0, 220.0, float('nan'), float('nan'), 100.0, float('nan'), 100.0, float('nan')],
    'AOUT': [float('nan'), 300.0, float('nan'), float('nan'), 200.0, 100.0, 150.0, float('nan'), float('nan'), float('nan'), float('nan'), 100.0, 120.0, float('nan'), float('nan'), float('nan'), float('nan'), 30.0, float('nan'), float('nan'), 100.0, 150.0, 100.0, float('nan'), 100.0, 200.0, float('nan'), 200.0, float('nan'), float('nan'), 80.0, float('nan')],
    'SEPT': [float('nan'), float('nan'), 100.0, 100.0, 200.0, float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 100.0, float('nan'), 160.0, float('nan'), 100.0, float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 100.0, 200.0, float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 300.0, float('nan'), 100.0, 100.0, float('nan')],
    'OCT': [float('nan'), 100.0, float('nan'), float('nan'), 100.0, 200.0, 150.0, float('nan'), float('nan'), 150.0, float('nan'), float('nan'), 100.0, float('nan'), 100.0, float('nan'), 150.0, float('nan'), float('nan'), float('nan'), 100.0, 200.0, 100.0, float('nan'), float('nan'), 200.0, float('nan'), 300.0, 100.0, float('nan'), 100.0, float('nan')],
    'NOV': [float('nan'), 200.0, 100.0, float('nan'), 200.0, float('nan'), 200.0, float('nan'), 80.0, float('nan'), 100.0, 100.0, float('nan'), float('nan'), float('nan'), 30.0, float('nan'), float('nan'), 40.0, 75.0, 100.0, float('nan'), float('nan'), 100.0, 150.0, 200.0, float('nan'), float('nan'), float('nan'), float('nan'), 100.0, float('nan')],
    'DEC': [float('nan'), 200.0, float('nan'), float('nan'), 100.0, float('nan'), float('nan'), 70.0, float('nan'), float('nan'), float('nan'), float('nan'), 100.0, 50.0, 100.0, float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 100.0, 200.0, 100.0, float('nan'), float('nan'), 200.0, float('nan'), 300.0, 100.0, float('nan'), 100.0, float('nan')],
}

df = pd.DataFrame(data, index=towns)

# Folium Map Setup
map_center = [18.7669, 46.8691]  # Approximate center of Madagascar
m = folium.Map(location=map_center, zoom_start=6)

# Create Popups with Histograms
for town in df.index:
    town_data = df.loc[town]
    town_data = town_data.dropna()  # Remove NaN values for the histogram
    if not town_data.empty:
        # Create a histogram
        fig, ax = plt.subplots()
        ax.hist(town_data, bins=10, edgecolor='black')
        ax.set_title(f'Histogram for {town}')
        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')

        # Save the histogram to a BytesIO object
        img_stream = io.BytesIO()
        plt.savefig(img_stream, format='png')
        plt.close(fig)
        img_stream.seek(0)

        # Convert image to base64
        img_base64 = base64.b64encode(img_stream.read()).decode('utf-8')
        img_html = f'<img src="data:image/png;base64,{img_base64}"/>'

        # Add marker with popup
        folium.Marker(
            location=[-20, 45],  # Placeholder coordinates, adjust as needed
            popup=folium.Popup(html=img_html, max_width=500)
        ).add_to(m)

# Display Map in Streamlit
st.title("Monthly Data Histograms for Towns")
st_folium(m, width=700, height=500)
