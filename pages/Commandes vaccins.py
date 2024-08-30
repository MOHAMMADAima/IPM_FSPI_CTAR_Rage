import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# Define the CTAR locations and corresponding histogram data
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

# Extracting data for the map
city_names = [info[0] for info in towns_info.values()]
latitudes = [info[1][0] for info in towns_info.values()]
longitudes = [info[1][1] for info in towns_info.values()]
histogram_data = [info[2] for info in towns_info.values()]

# Create a scatter mapbox plot with histograms as popups
fig = go.Figure()

for i, city in enumerate(city_names):
    # Add CTAR location as a marker
    fig.add_trace(go.Scattermapbox(
        lat=[latitudes[i]],
        lon=[longitudes[i]],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=12,
            color='darkorange',
        ),
        name=city,
        customdata=[histogram_data[i]],  # Pass the histogram data
        hoverinfo='text',
        hovertext=f"{city}",
        showlegend=False
    ))

# Update layout with the map settings
fig.update_layout(
    width=1200,  # Set the desired width
    height=900,  # Set the desired height
    mapbox=dict(
        style="open-street-map",
        center=dict(lat=-19, lon=47),
        zoom=5
    ),
    title="CTAR les plus fréquentés de Madagascar",
    showlegend=False
)

# Display the map in Streamlit
st.plotly_chart(fig)

# Logic to display the histogram when a marker is clicked
if 'last_click' in st.session_state:
    last_click = st.session_state['last_click']
    city_index = city_names.index(last_click['hovertext'])
    st.write(f"Histogram for {city_names[city_index]}")
    hist_fig = px.histogram(histogram_data[city_index], nbins=5, title=f"Histogram for {city_names[city_index]}")
    st.plotly_chart(hist_fig)

# Set up a click callback to capture click events
def click_callback(trace, points, state):
    st.session_state['last_click'] = points[0]

# Attach the callback to each marker
for trace in fig.data:
    trace.on_click(click_callback)

# Display the map with clickable markers
st.plotly_chart(fig)
