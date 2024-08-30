import streamlit as st
import folium
import base64
import io
import matplotlib.pyplot as plt
import pandas as pd
from streamlit_folium import st_folium

# Function to create a pie chart as a base64 image
def create_pie_chart(val1, val2, val3):
    labels = ['Value 1', 'Value 2', 'Value 3']
    sizes = [val1, val2, val3]
    colors = ['#ff9999', '#66b3ff', '#99ff99']
    explode = (0.1, 0, 0)  # explode 1st slice

    fig, ax = plt.subplots(figsize=(4, 3))
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    ax.axis('equal')
    plt.tight_layout()

    # Save pie chart to a base64 string
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode()
    
    # Close the figure to prevent memory leak
    plt.close(fig)

    return img_str

# Sample data for towns
towns_info_test = {
    'town1': ('Town 1', (-19.0, 47.0), 1000, 10, 20, 30),
    'town2': ('Town 2', (-18.0, 46.0), 1500, 15, 25, 35),
    'town3': ('Town 3', (-17.0, 45.0), 2000, 20, 30, 40)
}

# Initialize the map
m = folium.Map(location=[-19, 47], zoom_start=5.5, tiles='OpenStreetMap')

# Create markers for each town
for key, (town_name, (lat, lon), pop, val1, val2, val3) in towns_info_test.items():
    # Create HTML content for the popup
    popup_html = f"<b>{town_name}</b><br>" \
                 f"Population: {pop}<br>" \
                 f"Value 1: {val1}<br>" \
                 f"Value 2: {val2}<br>" \
                 f"Value 3: {val3}<br>" \
                 f"<br><b>Pie Chart:</b><br>" \
                 f"<img src='data:image/png;base64,{create_pie_chart(val1, val2, val3)}'>"

    # Create the marker with the popup
    folium.Marker([lat, lon], popup=popup_html).add_to(m)

# Save the map to a HTML file and display it in Streamlit
map_html = 'map.html'
m.save(map_html)

# Streamlit page configuration
st.set_page_config(page_title="Map with Pie Charts", layout="wide")

# Display the map using Streamlit
st.title("Map with Pie Charts in Popups")
st_folium(m, width=800, height=600)

