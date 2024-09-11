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
    7: ("Ambatondrazaka", (-17.8324, 48.4086), [200, 0, 200, 50, 100, 100, 100, 300, 0, 0, 0, 0]),
    30: ("Ambositra", (-20.5300, 47.2441),[100, 100, 0, 50, 100, 100, 0, 0, 100, 0, 100, 0]),
    100: ("Ambatomainty", (-17.1884, 44.5947),[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    13: ("Antsirabe", (-19.8659, 47.0333),[100, 100, 200, 100, 225, 70, 140, 200, 200, 100, 200, 100]),
    10: ("Antsiranana", (-12.2795, 49.2913),[150, 0, 0, 100, 0, 100, 225, 70, 140, 200, 200, 100]),
    14: ("Antsohihy", (-14.8667, 47.9833),[0, 150, 0, 75, 125, 100, 230, 150, 0, 150, 200, 0]),
    12: ("Bekily", (-24.2333, 45.3833),[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 70]),

    1: ("Soanierana Ivongo", (-16.9167, 49.5833),[150, 150, 150, 100, 25, 150, 220, 200, 0, 200, 200, 200]),

    2: ("Fianarantsoa", (-21.4545, 47.0833),[75, 0, 75, 50, 0, 0, 60, 0, 0, 0, 80, 0]),
    16: ("Ihosy", (-22.4021, 46.1253),[0, 100, 0, 0, 100, 0, 100, 0, 100, 0, 100,0]),
    17: ("Maevatanana", (-16.9333, 46.8333),[100, 0, 0, 0, 100, 0, 0, 100,0, 0, 100,0]),
    18: ("Mahajanga", (-15.7167, 46.3167),[120, 120, 0, 60, 115, 120, 80, 120, 160, 100, 0, 100]),
    19: ("Maintirano", (-18.0566, 44.0297),[0, 0, 0, 0, 20, 0, 50, 0, 0, 0, 0, 50]),
    31: ("Manakara", (-22.1451, 48.0115),[100, 100, 100, 0, 0, 100, 100, 0, 100, 100, 0, 100]),
    15: ("Mandritsara", (-15.8333, 48.8333),[150, 0, 0, 0, 150, 0, 0, 0, 0, 150, 0, 0]),
    23: ("Manja", (-21.4167, 44.8667),[50, 0, 0, 0, 0, 0, 0, 30, 0, 0, 0, 0]),
    4: ("Maroantsetra", (-15.4333, 49.7500),[0, 0, 0, 0, 40, 0, 0, 0, 0, 0, 40, 0]),
    21: ("Miarinarivo", (-19.0010, 46.7334),[0, 100, 200, 50, 100, 70, 0, 100, 100, 100, 100, 100]),
    8: ("Moramanga", (-18.9333, 48.2000),[0, 0, 250, 0, 150, 0, 100, 150, 200, 200, 0, 200]),
    22: ("Morondava", (-20.2833, 44.2833),[0, 100, 0, 0, 125, 0, 0, 100, 0, 100, 0, 100]),
    9: ("Nosy Be", (-13.3333, 48.2667),[0, 0, 100, 0, 100, 0, 0, 0, 0, 0, 100, 0]),
    24: ("Sambava", (-14.2667, 50.1667),[140, 50, 130, 75, 100, 70, 0, 100, 100, 100, 100, 100]),
    101: ("Sainte Marie", (-17.0000, 49.8500),[0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 0, 0]),
    25: ("Taolagnaro", (-25.0314, 46.9821),[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 75, 0]),
    28: ("Toamasina", (-18.1492, 49.4023),[0, 240, 240, 100, 240, 200, 0, 200, 300, 300, 0, 300]),
    26: ("Toliara", (-23.3568, 43.6917),[0, 0, 100, 0, 0, 0, 100, 0, 0, 100, 0, 100]),
    27: ("Tsiroanomandidy", (-18.7713, 46.0520),[100, 0, 0, 25, 200, 100, 0, 0, 100, 80, 0, 0]),
    3: ("Vangaindrano", (-23.3479, 47.5972),[100, 0, 100, 0, 100, 0, 100, 80, 100, 0, 100, 100]),
    97: ("Mananjary", (-21.2300, 48.3439),[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 30, 0]),
    102: ("Fort Dauphin", (-25.0347, 46.9883),[200, 0, 0, 0, 0, 0, 150, 0, 0, 150, 0, 0]),
    103: ("Ambovombe", (-25.1744, 46.0876),[0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0])

}

# Convert the dictionary to a DataFrame
df = pd.DataFrame.from_dict(towns_info_test, orient='index', columns=['Town', 'Coordinates', 'Monthly Data'])
df[['Latitude', 'Longitude']] = pd.DataFrame(df['Coordinates'].tolist(), index=df.index)

def create_histogram(monthly_data, town_name):
    fig, ax = plt.subplots(figsize=(20, 17))
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ax.bar(months, monthly_data, color='#66b3ff', label='Monthly Data')

    # Adding title and labels
    ax.set_title('Distribution vaccins mensuelle dans le CTAR', fontsize=16, weight='bold')
    ax.set_xlabel('Months', fontsize=12)
    ax.set_ylabel('Data Value', fontsize=12)

    # Adding a legend
    ax.legend(loc='upper right', fontsize=10)

    # Adding grid lines for better readability
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Save histogram to a base64 string
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode()

    plt.close(fig)

    return img_str

# Initialize the map centered on Madagascar
m = folium.Map(location=[-18.8792, 47.5079], zoom_start=5)

# Add town markers with histogram popups and town names
for idx, row in df.iterrows():
    hist_img = create_histogram(row['Monthly Data'], row['Town'])
    html = f'<h4 style="text-align: center;">{row["Town"]}</h4><img src="data:image/png;base64,{hist_img}" style="width: 350px; height: 250px;">'
    iframe = folium.IFrame(html=html, width=500, height=350)
    popup = folium.Popup(iframe, max_width=400)

    folium.Marker(location=[row['Latitude'], row['Longitude']],
                  popup=popup, tooltip=row['Town']).add_to(m)


# Display the map in Streamlit
st.title("Distribution mensuelles des vaccins dans les CTARs de Madagascar.")
folium_static(m)
