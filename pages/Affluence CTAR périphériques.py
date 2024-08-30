import streamlit as st
import plotly.graph_objs as go

# Towns information (provided by the user)
towns_info = {
    7: ("Ambatondrazaka", (-17.8324, 48.4086), 6288),
    30: ("Ambositra", (-20.5300, 47.2441), 3239),
    100: ("Ambatomainty", (-17.1884, 44.5947), 94),
    13: ("Antsirabe", (-19.8659, 47.0333), 9547),
    10: ("Antsiranana", (-12.2795, 49.2913), 1),
    14: ("Antsohihy", (-14.8667, 47.9833), 4412),
    12: ("Bekily", (-24.2333, 45.3833), 178),
    1: ("Soanierana Ivongo", (-16.9167, 49.5833), 5541),
    2: ("Fianarantsoa", (-21.4545, 47.0833), 1045),
    16: ("Ihosy", (-22.4021, 46.1253), 1844),
    17: ("Maevatanana", (-16.9333, 46.8333), 1593),
    18: ("Mahajanga", (-15.7167, 46.3167), 3751),
    19: ("Maintirano", (-18.0566, 44.0297), 498),
    31: ("Manakara", (-22.1451, 48.0115), 2987),
    15: ("Mandritsara", (-15.8333, 48.8333), 220),
    23: ("Manja", (-21.4167, 44.8667), 108),
    4: ("Maroantsetra", (-15.4333, 49.7500), 190),
    21: ("Miarinarivo", (-19.0010, 46.7334), 2159),
    8: ("Moramanga", (-18.9333, 48.2000), 4311),
    22: ("Morondava", (-20.2833, 44.2833), 1465),
    9: ("Nosy Be", (-13.3333, 48.2667), 600),
    24: ("Sambava", (-14.2667, 50.1667), 1856),
    101: ("Sainte Marie", (-17.0000, 49.8500), 116),
    25: ("Taolagnaro", (-25.0314, 46.9821), 175),
    28: ("Toamasina", (-18.1492, 49.4023), 19317),
    26: ("Toliara", (-23.3568, 43.6917), 2584),
    27: ("Tsiroanomandidy", (-18.7713, 46.0520), 361),
    3: ("Vangaindrano", (-23.3479, 47.5972), 2571),
    97: ("Mananjary", (-21.2300, 48.3439), 47),
    102: ("Fort Dauphin", (-25.0347, 46.9883), 1),
    103: ("Ambovombe", (-25.1744, 46.0876), 343)
}

# Streamlit app
st.title("CTAR Les Plus Fréquentés de Madagascar")

# Extracting the data for the map
city_names = [info[0] for info in towns_info.values()]
latitudes = [info[1][0] for info in towns_info.values()]
longitudes = [info[1][1] for info in towns_info.values()]
populations = [info[2] for info in towns_info.values()]

# Create a scatter mapbox plot
fig = go.Figure(go.Scattermapbox(
    lat=latitudes,
    lon=longitudes,
    mode='markers+text',
    marker=go.scattermapbox.Marker(
        size=[10 + (pop / 500) for pop in populations],  # Adjust size based on town values
        color='darkorange',
    ),
    text=[f"CTAR {name}: {value} patients" for name, value in zip(city_names, populations)],
    textposition='top center',
))

fig.update_layout(
    width=1200,  # Set the desired width
    height=900,  # Set the desired height
    mapbox=dict(
        style="open-street-map",
        center=dict(lat=-19, lon=47),
        zoom=5
    ),
    title="CTAR les plus fréquentés de Madagascar",
    showlegend=True
)

# Display the map in Streamlit
st.plotly_chart(fig)
