import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from io import BytesIO
import base64
import matplotlib.pyplot as plt



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

# Function to create a pie chart as base64 image
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
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode()
    
    # Close the figure to prevent memory leak
    plt.close(fig)

    return img_str

# Streamlit app with pages
def home_page():
    st.title("Upload Data Files")
    
    # File uploader for the home page
    uploaded_file = st.file_uploader("Upload an Excel file named 'verorab'", type="xlsx")
    
    if uploaded_file is not None:
        # Load the dataframe into session state
        df = pd.read_excel(uploaded_file)
        
        # Save to session state
        if 'dataframes' not in st.session_state:
            st.session_state['dataframes'] = {}
        
        st.session_state['dataframes']['verorab'] = df
        
        st.success("File uploaded successfully! Now go to the analysis page.")

def analysis_page():
    st.title("CTAR Analysis: Map and Quality Histogram")

    # Check if dataframes are available in session state
    if 'dataframes' in st.session_state:
        dataframes = st.session_state['dataframes']
        
        # Load the selected dataframe
        verorab = dataframes.get('verorab')
        
        if verorab is not None:
            # Rename columns for consistency
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
                
                # Create a scatter mapbox plot with pie chart popups
                fig_map = go.Figure()
                
                for idx, (lat, lon, quality_metric) in enumerate(zip(latitudes, longitudes, quality_metrics)):
                    pie_chart_img = create_pie_chart(quality_metric, 0, 0)  # Placeholder values for other metrics
                    
                    # Create the marker with the popup
                    fig_map.add_trace(go.Scattermapbox(
                        lat=[lat],
                        lon=[lon],
                        mode='markers',
                        marker=dict(size=10, color='darkorange', opacity=0.8),
                        text=[f"<b>{selected_ctar}</b><br>Quality Metric: {quality_metric:.2f}<br><img src='data:image/png;base64,{pie_chart_img}'>"],
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
                    title=f"Quality Metrics per Month for {selected_ctar}",
                    xaxis_title="Quality Metric",
                    yaxis_title="Count"
                )
                
                st.plotly_chart(fig_hist)
            else:
                st.error("The uploaded file is missing required columns.")
        else:
            st.error("No file available for analysis.")

# Main page selection
page = st.sidebar.selectbox("Select Page", ["Home", "Analysis"])

if page == "Home":
    home_page()
elif page == "Analysis":
    analysis_page()
