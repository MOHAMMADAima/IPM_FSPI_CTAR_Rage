import streamlit as st
import pandas as pd
import folium
from folium import plugins
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from streamlit_folium import folium_static

# Sample data for Madagascar towns with 12 monthly values
towns_info_test = {
    7: ("Ambatondrazaka", (-17.8324, 48.4086), [100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650]),
    30: ("Ambositra", (-20.5300, 47.2441), [120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230]),
    100: ("Ambatomainty", (-17.1884, 44.5947), [80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135]),
    # Add more towns similarly
}

# Convert the dictionary to a DataFrame
df = pd.DataFrame.from_dict(towns_info_test, orient='index', columns=['Town', 'Coordinates', 'Monthly Data'])
df[['Latitude', 'Longitude']] = pd.DataFrame(df['Coordinates'].tolist(), index=df.index)

# Function to create a histogram and return it as a base64 encoded image
def create_histogram(monthly_data):
    fig, ax = plt.subplots()
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ax.bar(months, monthly_data, color='#66b3ff')

    # Save histogram to a base64 string
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode()

    plt.close(fig)

    return img_str

# Initialize the map centered on Madagascar
m = folium.Map(location=[-18.8792, 47.5079], zoom_start=6)

# Add town markers with histogram popups
for idx, row in df.iterrows():
    hist_img = create_histogram(row['Monthly Data'])
    html = f'<img src="data:image/png;base64,{hist_img}" style="width: 300px; height: 200px;">'
    iframe = folium.IFrame(html=html, width=300, height=200)
    popup = folium.Popup(iframe, max_width=300)

    folium.Marker(location=[row['Latitude'], row['Longitude']],
                  popup=popup, tooltip=row['Town']).add_to(m)

# Display the map in Streamlit
st.title("Madagascar Towns Map with Monthly Data Histograms")
folium_static(m)
