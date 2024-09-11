import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import io
import base64

# Sample data for Madagascar towns
towns_info_test = {
    7: ("Ambatondrazaka", (-17.8324, 48.4086), 6288, 2332, 323, 243),
    30: ("Ambositra", (-20.5300, 47.2441), 3239, 2332, 323, 243),
    100: ("Ambatomainty", (-17.1884, 44.5947), 94, 2332, 323, 243),
    13: ("Antsirabe", (-19.8659, 47.0333), 9547, 2332, 323, 243),
    10: ("Antsiranana", (-12.2795, 49.2913), 1, 2332, 323, 243),
    14: ("Antsohihy", (-14.8667, 47.9833), 4412, 2332, 323, 243),
    12: ("Bekily", (-24.2333, 45.3833), 178, 2332, 323, 243),
    1: ("Soanierana Ivongo", (-16.9167, 49.5833), 5541, 2332, 323, 243),
    2: ("Fianarantsoa", (-21.4545, 47.0833), 1045, 2332, 323, 243),
    16: ("Ihosy", (-22.4021, 46.1253), 1844, 2332, 323, 243),
    17: ("Maevatanana", (-16.9333, 46.8333), 1593, 2332, 323, 243),
    18: ("Mahajanga", (-15.7167, 46.3167), 3751, 2332, 323, 243),
    19: ("Maintirano", (-18.0566, 44.0297), 498, 2332, 323, 243),
    31: ("Manakara", (-22.1451, 48.0115), 2987, 2332, 323, 243),
    15: ("Mandritsara", (-15.8333, 48.8333), 220, 2332, 323, 243),
    23: ("Manja", (-21.4167, 44.8667), 108, 2332, 323, 243),
    4: ("Maroantsetra", (-15.4333, 49.7500), 190, 2332, 323, 243),
    21: ("Miarinarivo", (-19.0010, 46.7334), 2159, 2332, 323, 243),
    8: ("Moramanga", (-18.9333, 48.2000), 4311, 2332, 323, 243),
    22: ("Morondava", (-20.2833, 44.2833), 1465, 2332, 323, 243),
    9: ("Nosy Be", (-13.3333, 48.2667), 600, 2332, 323, 243),
    24: ("Sambava", (-14.2667, 50.1667), 1856, 2332, 323, 243),
    101: ("Sainte Marie", (-17.0000, 49.8500), 116, 2332, 323, 243),
    25: ("Taolagnaro", (-25.0314, 46.9821), 175, 2332, 323, 243),
    28: ("Toamasina", (-18.1492, 49.4023), 19317, 2332, 323, 243),
    26: ("Toliara", (-23.3568, 43.6917), 2584, 2332, 323, 243),
    27: ("Tsiroanomandidy", (-18.7713, 46.0520), 361, 2332, 323, 243),
    3: ("Vangaindrano", (-23.3479, 47.5972), 2571, 2332, 323, 243),
    97: ("Mananjary", (-21.2300, 48.3439), 47, 2332, 323, 243),
    102: ("Fort Dauphin", (-25.0347, 46.9883), 1, 2332, 323, 243),
    103: ("Ambovombe", (-25.1744, 46.0876), 343, 2332, 323, 243)
}

# Convert the dictionary to a DataFrame
df = pd.DataFrame.from_dict(towns_info_test, orient='index',
                            columns=['Town', 'Coordinates', 'Population', 'Val1', 'Val2', 'Val3'])
df[['Latitude', 'Longitude']] = pd.DataFrame(df['Coordinates'].tolist(), index=df.index)

# Function to create a pie chart as a base64 image
def create_pie_chart(val1, val2, val3):
    labels = ['Value 1', 'Value 2', 'Value 3']
    sizes = [val1, val2, val3]
    colors = ['#ff9999', '#66b3ff', '#99ff99']
    explode = (0.1, 0, 0)  # explode 1st slice

    fig, ax = plt.subplots(figsize=(4, 3))
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.tight_layout()

    # Save pie chart to a base64 string
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode()

    # Close the figure to prevent memory leak
    plt.close(fig)

    return img_str

# Streamlit page title
st.title("Interactive Madagascar Towns Map with Pie Charts")

# Create the map with Plotly Express
fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", hover_name="Town",
                        hover_data=["Population", "Val1", "Val2", "Val3"], zoom=4, height=600)

fig.update_layout(mapbox_style="open-street-map")

# Show map on Streamlit
st.plotly_chart(fig)

# Check if a town has been clicked and show a pie chart
selected_point = st.session_state.get('selected_point', None)

if selected_point:
    town_name = selected_point['points'][0]['hovertext']
    town_data = df[df['Town'] == town_name]
    val1, val2, val3 = town_data[['Val1', 'Val2', 'Val3']].values[0]

    st.write(f"## Pie Chart for {town_name}")
    pie_chart = create_pie_chart(val1, val2, val3)
    st.image(f"data:image/png;base64,{pie_chart}")

# Capture click event on the map
st.session_state['selected_point'] = st.plotly_chart(fig, use_container_width=True).click()

