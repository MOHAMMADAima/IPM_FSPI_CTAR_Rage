import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

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

# Streamlit page
st.title("CTAR Analysis: Map and Quality Histogram")

# File uploader for data
uploaded_file = st.file_uploader("Upload the CSV file named 'verorab'", type="csv")

if uploaded_file is not None:
    # Load the dataframe
    verorab = pd.read_csv(uploaded_file)
    
    # Rename columns to avoid confusion
    verorab.rename(columns={'ID_CTAR': 'id_ctar'}, inplace=True)
    
    # Check for necessary columns
    required_columns = ['id_ctar', 'JANV', 'FEV', 'MARS', 'AVRIL', 'MAI', 'JUIN', 'JUILL', 'AOUT', 'SEPT', 'OCT', 'NOV', 'DEC', 'TOTAUX']
    if all(col in verorab.columns for col in required_columns):
        # Melt the DataFrame to long format for easier plotting
        melted_verorab = verorab.melt(id_vars=['id_ctar'], value_vars=['JANV', 'FEV', 'MARS', 'AVRIL', 'MAI', 'JUIN', 'JUILL', 'AOUT', 'SEPT', 'OCT', 'NOV', 'DEC'],
                                      var_name='Month', value_name='Quality_Metric')
        
        # Replace NaN with 0 for the quality metrics
        melted_verorab['Quality_Metric'].fillna(0, inplace=True)
        
        # Map id_ctar to town names and coordinates
        melted_verorab['town_name'] = melted_verorab['id_ctar'].map(lambda x: towns_info.get(x, ("Unknown", (0, 0)))[0])
        melted_verorab['gps_coordinates'] = melted_verorab['id_ctar'].map(lambda x: towns_info.get(x, ("Unknown", (0, 0)))[1])
        
        # Select CTAR to analyze
        selected_ctar = st.selectbox("Select CTAR", options=melted_verorab['town_name'].unique())

        # Filter data for the selected CTAR
        filtered_data = melted_verorab[melted_verorab['town_name'] == selected_ctar]
        
        # Extract data for map
        latitudes = [coord[0] for coord in filtered_data['gps_coordinates']]
        longitudes = [coord[1] for coord in filtered_data['gps_coordinates']]
        quality_metrics = filtered_data['Quality_Metric']
        
        # Create a scatter mapbox plot
        fig_map = go.Figure(go.Scattermapbox(
            lat=latitudes,
            lon=longitudes,
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=10,
                color='darkorange',
                opacity=0.8
            ),
            text=[f"CTAR {selected_ctar}: {value:.2f}" for value in quality_metrics],
            hoverinfo='text'
        ))
        
        fig_map.update_layout(
            width=1200,
            height=900,
            mapbox=dict(
                style="open-street-map",
                center=dict(lat=np.mean(latitudes), lon=np.mean(longitudes)),
                zoom=5
            ),
            title=f"CTAR {selected_ctar} Locations",
            showlegend=False
        )
        
        st.plotly_chart(fig_map)
        
        # Histogram of quality metrics per month
        fig_hist = go.Figure()
        
        for month in filtered_data['Month'].unique():
            month_data = filtered_data[filtered_data['Month'] == month]
            fig_hist.add_trace(go.Histogram(
                x=month_data['Quality_Metric'],
                name=month,
                opacity=0.75
            ))
        
        fig_hist.update_layout(
            barmode='overlay',
            title=f"Histogram of Quality Metrics for CTAR {selected_ctar}",
            xaxis_title="Quality Metric",
            yaxis_title="Frequency",
            xaxis=dict(type='category')
        )
        
        st.plotly_chart(fig_hist)
        
    else:
        st.error(f"Uploaded file must contain the following columns: {', '.join(required_columns)}.")
