import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import base64
import io
import matplotlib.pyplot as plt

# Define CTAR locations and data
towns_info = {
    7: ("Ambatondrazaka", (-17.8324, 48.4086), [10, 20, 30, 40, 50]),
    30: ("Ambositra", (-20.5300, 47.2441), [15, 25, 35, 45, 55]),
    100: ("Ambatomainty", (-17.1884, 44.5947), [5, 10, 15, 20, 25]),
    13: ("Antsirabe", (-19.8659, 47.0333), [12, 22, 32, 42, 52]),
    10: ("Antsiranana", (-12.2795, 49.2913), [14, 24, 34, 44, 54]),
    14: ("Antsohihy", (-14.8667, 47.9833), [16, 26, 36, 46, 56]),
    12: ("Bekily", (-24.2333, 45.3833), [18, 28, 38, 48, 58]),
    1: ("Soanierana Ivongo", (-16.9167, 49.5833), [20, 30, 40, 50, 60]),
    2: ("Fianarantsoa", (-21.4545, 47.0833), [22, 32, 42, 52, 62]),
    16: ("Ihosy", (-22.4021, 46.1253), [24, 34, 44, 54, 64]),
    17: ("Maevatanana", (-16.9333, 46.8333), [26, 36, 46, 56, 66]),
    18: ("Mahajanga", (-15.7167, 46.3167), [28, 38, 48, 58, 68]),
    19: ("Maintirano", (-18.0566, 44.0297), [30, 40, 50, 60, 70]),
    31: ("Manakara", (-22.1451, 48.0115), [32, 42, 52, 62, 72]),
    15: ("Mandritsara", (-15.8333, 48.8333), [34, 44, 54, 64, 74]),
    23: ("Manja", (-21.4167, 44.8667), [36, 46, 56, 66, 76]),
    4: ("Maroantsetra", (-15.4333, 49.7500), [38, 48, 58, 68, 78]),
    21: ("Miarinarivo", (-19.0010, 46.7334), [40, 50, 60, 70, 80]),
    8: ("Moramanga", (-18.9333, 48.2000), [42, 52, 62, 72, 82]),
    22: ("Morondava", (-20.2833, 44.2833), [44, 54, 64, 74, 84]),
    9: ("Nosy Be", (-13.3333, 48.2667), [46, 56, 66, 76, 86]),
    24: ("Sambava", (-14.2667, 50.1667), [48, 58, 68, 78, 88]),
    101: ("Sainte Marie", (-17.0000, 49.8500), [50, 60, 70, 80, 90]),
    25: ("Taolagnaro", (-25.0314, 46.9821), [52, 62, 72, 82, 92]),
    28: ("Toamasina", (-18.1492, 49.4023), [54, 64, 74, 84, 94]),
    26: ("Toliara", (-23.3568, 43.6917), [56, 66, 76, 86, 96]),
    27: ("Tsiroanomandidy", (-18.7713, 46.0520), [58, 68, 78, 88, 98]),
    3: ("Vangaindrano", (-23.3479, 47.5972), [60, 70, 80, 90, 100]),
    97: ("Mananjary", (-21.2300, 48.3439), [62, 72, 82, 92, 102]),
    102: ("Fort Dauphin", (-25.0347, 46.9883), [64, 74, 84, 94, 104]),
    103: ("Ambovombe", (-25.1744, 46.0876), [66, 76, 86, 96, 106])
}

# Function to create a histogram as base64 image
def create_histogram(data):
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.hist(data, bins=10, color='blue', edgecolor='black')
    ax.set_xlabel('Value')
    ax.set_ylabel('Frequency')
    ax.set_title('Histogram')

    # Save histogram to a base64 string
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode()
    
    # Close the figure to prevent memory leak
    plt.close(fig)

    return img_str

# Streamlit app
st.title("CTAR Map with Interactive Histograms")

# Create a map figure
fig = go.Figure()

# Add CTAR markers to the map
for key, (city_name, (lat, lon), population) in towns_info.items():
    # Add CTAR location marker
    fig.add_trace(go.Scattermapbox(
        lat=[lat],
        lon=[lon],
        mode='markers+text',
        marker=go.scattermapbox.Marker(
            size=10 + (sum(population) / 500),  # Adjust size based on population data
            color='darkorange',
        ),
        text=[f"CTAR {city_name}"],
        textposition='top center',
        customdata=[population],
        hovertemplate=f"CTAR {city_name}<br>Population: {sum(population)}<br><extra></extra>",
        name=city_name
    ))

# Update layout for the map
fig.update_layout(
    mapbox=dict(
        style="open-street-map",
        center=dict(lat=-19, lon=47),
        zoom=5
    ),
    title="CTAR les plus fréquentés de Madagascar",
    showlegend=False,
    height=800
)

# Display the map in Streamlit
selected_ctar = st.selectbox("Select a CTAR to see its histogram", options=list(towns_info.keys()))

# Display histogram for the selected CTAR
if selected_ctar:
    city_name, (lat, lon), population = towns_info[selected_ctar]
    histogram_img = create_histogram(population)
    st.image(f"data:image/png;base64,{histogram_img}", caption=f'Histogram for {city_name}', use_column_width=True)

st.plotly_chart(fig)
